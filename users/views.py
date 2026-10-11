from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
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


@login_required
def my_loans(request):
    """Prostredie pre dlžníkov - prístupné až keď má aspoň jednu schválenú (vyfinancovanú) pôžičku."""
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
    return render(request, 'users/my_loans.html', {'loans': loans})

