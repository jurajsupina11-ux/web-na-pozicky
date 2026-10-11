from datetime import timedelta
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from auctions.models import Auction

from .forms import BorrowerApplicationForm, KYCForm, SignUpForm
from .models import User


class SignUpView(CreateView):
    """Registrácia - len pre investorov (veriteľov)."""

    form_class = SignUpForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('auctions:list')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class CustomLoginView(LoginView):
    template_name = 'users/login.html'


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('auctions:list')


@login_required
def kyc_form(request):
    """Citlivé údaje (OP, rodné číslo, adresa) vyplnené pri žiadosti o prvú pôžičku."""
    next_url = request.GET.get('next') or reverse_lazy('auctions:create')
    if request.user.kyc_completed:
        return redirect(next_url)
    if request.method == 'POST':
        form = KYCForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Údaje boli overené. Môžeš pokračovať v žiadosti o pôžičku.')
            return redirect(next_url)
    else:
        form = KYCForm(instance=request.user)
    return render(request, 'users/kyc_form.html', {'form': form, 'next_url': next_url})


def loan_application(request):
    """Dlžník sa neregistruje klasicky - jedným formulárom naraz vytvorí účet
    a požiada o pôžičku (osobné/KYC údaje + parametre úveru)."""
    if request.user.is_authenticated:
        if request.user.role == User.Role.BORROWER:
            return redirect('users:my_applications')
        messages.info(request, 'Si prihlásený ako investor. Odhlás sa, ak chceš žiadať o pôžičku.')
        return redirect('auctions:list')

    if request.method == 'POST':
        form = BorrowerApplicationForm(request.POST)
        if form.is_valid():
            user = form.create_user()
            form.create_auction(user)
            login(request, user)
            messages.success(
                request,
                'Žiadosť o pôžičku bola odoslaná. Hneď ako ju investor financuje, dostaneš sa do prostredia pre dlžníkov.',
            )
            return redirect('users:my_applications')
    else:
        form = BorrowerApplicationForm()
    return render(request, 'users/loan_application.html', {'form': form})


@login_required
def my_applications(request):
    """Prehľad vlastných žiadostí (aukcií) dlžníka - dostupné aj bez schválenej pôžičky."""
    applications = Auction.objects.filter(borrower=request.user)
    has_approved = applications.filter(
        status__in=[Auction.Status.FUNDED, Auction.Status.CLOSED],
    ).exists()
    return render(request, 'users/my_applications.html', {
        'applications': applications,
        'has_approved': has_approved,
    })


#: Údaje platiteľa, na ktorého účet majú dlžníci zasielať splátky.
REPAYMENT_BANK_DETAILS = {
    'bank_name': 'Fio banka, a.s., pobočka zahraničnej banky',
    'iban': 'SK89 8330 0000 0021 0167 2695',
    'swift': 'FIOZSKBA',
    'variable_symbol_hint': 'VS = číslo pôžičky (napr. 101)',
}


def _loan_repayment_amount(loan):
    """Celková suma na splatenie = istina + úrok (24 % p.a. prepočítaný na dni)."""
    interest = loan.amount_requested * Decimal('0.24') * (Decimal(loan.duration_days) / Decimal('365'))
    return round(loan.amount_requested + interest, 2)


@login_required
def my_loans(request):
    """Prostredie pre dlžníkov - prístupné až keď má aspoň jednu schválenú (vyfinancovanú) pôžičku.
    Obsahuje aktuálny stav pôžičky aj údaje, ako a kam ju zaplatiť."""
    loans = Auction.objects.filter(
        borrower=request.user,
        status__in=[Auction.Status.FUNDED, Auction.Status.CLOSED],
    )
    if not loans.exists():
        messages.warning(
            request,
            'Do prostredia pre dlžníkov sa dostaneš, až keď investor financuje aspoň jednu tvoju žiadosť.',
        )
        return redirect('users:my_applications')

    for loan in loans:
        loan.repay_amount = _loan_repayment_amount(loan)
        loan.interest_amount = round(loan.repay_amount - loan.amount_requested, 2)
        loan.due_date = loan.starts_at + timedelta(days=loan.duration_days)

    return render(request, 'users/my_loans.html', {
        'loans': loans,
        'bank_details': REPAYMENT_BANK_DETAILS,
    })


@login_required
def my_profile(request):
    """Moje údaje - osobné a prístupové informácie dlžníka/investora."""
    return render(request, 'users/my_profile.html')


@login_required
def my_contracts(request):
    """Moje zmluvy - prehľad zmluvných dokumentov k pôžičkám dlžníka."""
    contracts = Auction.objects.filter(
        borrower=request.user,
        status__in=[Auction.Status.FUNDED, Auction.Status.CLOSED],
    )
    return render(request, 'users/my_contracts.html', {'contracts': contracts})


@login_required
def account_settings(request):
    """Nastavenia účtu (zobrazenie, do budúcna napr. zmena hesla/notifikácie)."""
    return render(request, 'users/account_settings.html')


def _is_admin_request(request):
    """True ak je prihlásený ako superuser, alebo ak je aktuálne v impersonácii
    (reálny admin je uložený v request.real_admin vďaka ImpersonateMiddleware)."""
    real_admin = getattr(request, 'real_admin', None)
    return (request.user.is_authenticated and request.user.is_superuser) or (
        real_admin is not None and real_admin.is_superuser
    )


def impersonate_list(request):
    """Zoznam používateľov pre admina - vybrať si, koho prostredie chce vidieť."""
    if not _is_admin_request(request):
        return redirect('users:login')
    users = User.objects.filter(is_superuser=False).order_by('-date_joined')
    return render(request, 'users/impersonate_list.html', {'users': users})


def impersonate_start(request, user_id):
    if not _is_admin_request(request):
        return redirect('users:login')
    target = get_object_or_404(User, pk=user_id, is_superuser=False)
    request.session['impersonate_user_id'] = target.pk
    messages.info(request, f'Zobrazuješ prostredie používateľa „{target.username}“.')
    if target.role == User.Role.BORROWER:
        return redirect('users:my_applications')
    return redirect('auctions:list')


def impersonate_stop(request):
    if request.session.pop('impersonate_user_id', None):
        messages.info(request, 'Návrat do administrátorského účtu.')
    return redirect('users:impersonate_list')

