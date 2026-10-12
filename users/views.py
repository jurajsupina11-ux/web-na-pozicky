from datetime import timedelta
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from auctions.models import Auction
from core.emails import send_loan_application_received, send_repayment_reported

from .forms import BankAccountForm, BorrowerApplicationForm, KYCForm, SignUpForm
from .models import User


class SignUpView(CreateView):
    """Registrácia - len pre investorov (veriteľov)."""

    form_class = SignUpForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('auctions:investor_dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class CustomLoginView(LoginView):
    """Spoločná prihlasovacia logika - šablóna sa líši podľa toho, z ktorej
    stránky sa používateľ prihlasuje (investor/dlžník/admin), presmerovanie
    po prihlásení je vždy podľa reálnej role používateľa."""
    template_name = 'users/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.role == User.Role.BORROWER:
            return reverse_lazy('users:dashboard')
        return reverse_lazy('auctions:investor_dashboard')


class InvestorLoginView(CustomLoginView):
    """Prihlásenie pre investorov - vlastná (modrá) vizuálna šablóna."""
    template_name = 'users/login_investor.html'


class BorrowerLoginView(CustomLoginView):
    """Prihlásenie pre žiadateľov/dlžníkov - vlastná (oranžová) vizuálna šablóna."""
    template_name = 'users/login_borrower.html'


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('core:landing')


class CustomPasswordChangeView(PasswordChangeView):
    """Zmena hesla - šablóna sa líši podľa role prihláseného používateľa."""
    success_url = reverse_lazy('users:password_change_done')

    def get_template_names(self):
        if self.request.user.role == User.Role.BORROWER:
            return ['users/password_change_borrower.html']
        return ['users/password_change_investor.html']


class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    """Potvrdenie úspešnej zmeny hesla - šablóna podľa role."""

    def get_template_names(self):
        if self.request.user.role == User.Role.BORROWER:
            return ['users/password_change_done_borrower.html']
        return ['users/password_change_done_investor.html']


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
            return redirect('users:dashboard')
        messages.info(request, 'Si prihlásený ako investor. Odhlás sa, ak chceš žiadať o pôžičku.')
        return redirect('auctions:list')

    if request.method == 'POST':
        form = BorrowerApplicationForm(request.POST)
        if form.is_valid():
            user = form.create_user()
            auction = form.create_auction(user)
            login(request, user)
            send_loan_application_received(user, auction)
            messages.success(
                request,
                'Žiadosť o pôžičku bola odoslaná. Hneď ako ju investor financuje, dostaneš sa do prostredia pre dlžníkov.',
            )
            return redirect('users:dashboard')
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

#: Jednorazový poplatok za odklad splátky o 7 dní.
POSTPONE_FEE = Decimal('15')
POSTPONE_DAYS = 7


def _loan_repayment_amount(loan):
    """Celková suma na splatenie = istina + úrok (24 % p.a. prepočítaný na dni,
    vrátane prípadného odkladu) + poplatky za odklady."""
    total_days = loan.duration_days + loan.postponed_days
    interest = loan.amount_requested * Decimal('0.24') * (Decimal(total_days) / Decimal('365'))
    postpone_fees = Decimal(loan.postponed_days // POSTPONE_DAYS) * POSTPONE_FEE
    return round(loan.amount_requested + interest + postpone_fees, 2)


def _annotate_loan(loan):
    loan.repay_amount = _loan_repayment_amount(loan)
    loan.interest_amount = round(loan.repay_amount - loan.amount_requested, 2)
    loan.due_date = loan.starts_at + timedelta(days=loan.duration_days + loan.postponed_days)
    return loan


@login_required
def dashboard(request):
    """Hlavná vstupná stránka prostredia pre dlžníkov - prehľad stavu účtu,
    aktuálneho dlhu, najbližšej splatnosti a rýchlych akcií."""
    applications = Auction.objects.filter(borrower=request.user)
    active_loans = applications.filter(status=Auction.Status.FUNDED)
    closed_loans = applications.filter(status=Auction.Status.CLOSED)
    pending_applications = applications.filter(status=Auction.Status.ACTIVE)

    for loan in active_loans:
        _annotate_loan(loan)

    total_debt = sum((loan.repay_amount for loan in active_loans), Decimal('0'))
    next_due_loan = min(active_loans, key=lambda loan: loan.due_date, default=None)

    return render(request, 'users/dashboard.html', {
        'active_loans': active_loans,
        'closed_loans_count': closed_loans.count(),
        'pending_applications': pending_applications,
        'total_debt': total_debt,
        'next_due_loan': next_due_loan,
        'has_any_application': applications.exists(),
    })


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
        _annotate_loan(loan)

    return render(request, 'users/my_loans.html', {
        'loans': loans,
        'bank_details': REPAYMENT_BANK_DETAILS,
        'postpone_fee': POSTPONE_FEE,
    })


@login_required
def request_postponement(request, loan_id):
    """Dlžník žiada o odklad splátky o 7 dní za jednorazový poplatok."""
    loan = get_object_or_404(Auction, pk=loan_id, borrower=request.user, status=Auction.Status.FUNDED)
    if request.method == 'POST':
        loan.postponed_days += POSTPONE_DAYS
        loan.save(update_fields=['postponed_days'])
        messages.success(
            request,
            f'Splatnosť bola odložená o {POSTPONE_DAYS} dní za poplatok {POSTPONE_FEE} €.',
        )
    return redirect('users:my_loans')


@login_required
def report_payment(request, loan_id):
    """Dlžník nahlási, že splátku uhradil - pôžička prejde do stavu 'čaká na overenie'."""
    loan = get_object_or_404(Auction, pk=loan_id, borrower=request.user, status=Auction.Status.FUNDED)
    if request.method == 'POST':
        loan.payment_reported = True
        loan.save(update_fields=['payment_reported'])
        for bid in loan.bids.select_related('lender'):
            send_repayment_reported(bid.lender, loan)
        messages.success(
            request,
            'Ďakujeme, nahlásenie úhrady sme zaznamenali. Platbu overíme do 1 pracovného dňa.',
        )
    return redirect('users:my_loans')


@login_required
def my_offers(request):
    """Ponuky pre dlžníka - po úspešnom splatení pôžičky sem chodia ponuky
    na novú pôžičku, spolu s platobnými údajmi aktuálnej aktívnej pôžičky
    (rovnako ako v časti Moje pôžičky)."""
    loans = Auction.objects.filter(borrower=request.user)
    active_loans = loans.filter(status=Auction.Status.FUNDED)
    closed_loans = loans.filter(status=Auction.Status.CLOSED)

    for loan in active_loans:
        _annotate_loan(loan)

    return render(request, 'users/my_offers.html', {
        'active_loans': active_loans,
        'has_closed_loan': closed_loans.exists(),
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
    """Nastavenia účtu - vrátane zmeny bankového účtu (IBAN), na ktorý sa
    vyplácajú peniaze (dostupné pre investora aj dlžníka)."""
    if request.method == 'POST':
        form = BankAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bankový účet pre výplatu peňazí bol aktualizovaný.')
            return redirect('users:account_settings')
    else:
        form = BankAccountForm(instance=request.user)
    template = (
        'users/account_settings_borrower.html'
        if request.user.role == User.Role.BORROWER
        else 'users/account_settings_investor.html'
    )
    return render(request, template, {'bank_form': form})


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
        return redirect('users:dashboard')
    return redirect('auctions:investor_dashboard')


def impersonate_stop(request):
    if request.session.pop('impersonate_user_id', None):
        messages.info(request, 'Návrat do administrátorského účtu.')
    return redirect('users:impersonate_list')

