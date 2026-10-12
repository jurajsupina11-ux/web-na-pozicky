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
from core.emails import (
    send_email_verification, send_investor_welcome, send_loan_application_received,
    send_loan_approved, send_repayment_reported,
)

from .forms import (
    BankAccountForm, BorrowerApplicationForm, KYCForm, RepeatLoanApplicationForm,
    SecurityCodePasswordChangeForm, SignUpForm,
)
from .models import User, _generate_email_verification_token


#: Maximálny počet registrácií z jednej IP adresy za hodinu - jednoduchá
#: ochrana pred automatizovaným hromadným vytváraním účtov (napr. kvôli
#: zneužitiu referral bonusov).
SIGNUP_RATE_LIMIT = 5
SIGNUP_RATE_LIMIT_WINDOW = 60 * 60


def _client_ip(request):
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', 'unknown')


class SignUpView(CreateView):
    """Registrácia - len pre investorov (veriteľov). Podporuje odporúčací
    (referral) program cez ?ref=KOD v URL - uloží sa referred_by na nového
    používateľa, odmena sa pripíše po jeho prvej investícii. Obsahuje
    jednoduchú ochranu pred hromadnými registráciami z jednej IP adresy."""

    form_class = SignUpForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('auctions:investor_dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ref_code'] = self.request.GET.get('ref', '')
        return context

    def post(self, request, *args, **kwargs):
        from django.core.cache import cache

        cache_key = f'signup_rate_{_client_ip(request)}'
        attempts = cache.get(cache_key, 0)
        if attempts >= SIGNUP_RATE_LIMIT:
            messages.error(
                request,
                'Príliš veľa pokusov o registráciu z tejto siete. Skús to prosím neskôr.',
            )
            return redirect('users:signup')
        cache.set(cache_key, attempts + 1, SIGNUP_RATE_LIMIT_WINDOW)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        ref_code = self.request.GET.get('ref') or self.request.POST.get('ref_code')
        if ref_code:
            referrer = User.objects.filter(referral_code=ref_code).exclude(pk=None).first()
            if referrer:
                form.instance.referred_by = referrer
        response = super().form_valid(form)
        login(self.request, self.object)
        send_investor_welcome(self.object)
        return response


class CustomLoginView(LoginView):
    """Spoločná prihlasovacia logika - šablóna sa líši podľa toho, z ktorej
    stránky sa používateľ prihlasuje (investor/dlžník/admin), presmerovanie
    po prihlásení je vždy podľa reálnej role používateľa."""
    template_name = 'users/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.role == User.Role.BORROWER:
            return reverse_lazy('users:my_applications')
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
    """Zmena hesla - vyžaduje zadanie bezpečnostného kódu (z e-mailu pri registrácii),
    šablóna sa líši podľa role prihláseného používateľa."""
    success_url = reverse_lazy('users:password_change_done')
    form_class = SecurityCodePasswordChangeForm

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
    """Žiadosť o pôžičku. Nový žiadateľ vyplní jeden formulár, ktorý naraz
    vytvorí účet (username = rodné číslo, heslo sa vygeneruje automaticky
    a pošle e-mailom) a podá žiadosť (osobné/KYC údaje + parametre úveru).
    Už overený dlžník (kyc_completed=True) vyplní len zjednodušený formulár
    s parametrami novej pôžičky - osobné údaje sa znova nepýtajú. Žiadosť
    v oboch prípadoch ide najprv k administrátorovi na posúdenie (stav
    PENDING_REVIEW) - do schválenia nemá dlžník prístup do menu, len na
    stránku so stavom žiadosti."""
    if request.user.is_authenticated and request.user.role == User.Role.BORROWER:
        # Už existujúci (overený) dlžník - zjednodušená opakovaná žiadosť.
        if request.method == 'POST':
            form = RepeatLoanApplicationForm(request.POST)
            if form.is_valid():
                auction = form.create_auction(request.user)
                send_loan_application_received(request.user, auction)
                messages.success(request, 'Žiadosť o pôžičku bola odoslaná - čaká sa na posúdenie.')
                return redirect('users:application_status')
        else:
            form = RepeatLoanApplicationForm()
        return render(request, 'users/loan_application_repeat.html', {'form': form})

    if request.user.is_authenticated:
        messages.info(request, 'Si prihlásený ako investor. Odhlás sa, ak chceš žiadať o pôžičku.')
        return redirect('auctions:list')

    if request.method == 'POST':
        form = BorrowerApplicationForm(request.POST)
        if form.is_valid():
            user = form.create_user()
            auction = form.create_auction(user)
            login(request, user)
            send_loan_application_received(user, auction, password=form.generated_password)
            messages.success(
                request,
                'Žiadosť o pôžičku bola odoslaná. Prihlasovacie údaje sme ti poslali e-mailom.',
            )
            return redirect('users:application_status')
    else:
        form = BorrowerApplicationForm()
    return render(request, 'users/loan_application.html', {'form': form})


@login_required
def application_status(request):
    """Stránka, ktorú dlžník vidí, kým jeho žiadosť čaká na posúdenie,
    bola zamietnutá, alebo dostal protiponuku - do schválenia žiadosti
    (stav ACTIVE a vyššie) nemá prístup do zvyšku menu pre dlžníkov."""
    if request.user.role != User.Role.BORROWER:
        return redirect('auctions:investor_dashboard')
    latest = Auction.objects.filter(borrower=request.user).order_by('-created_at').first()
    if latest and latest.status not in (
        Auction.Status.PENDING_REVIEW, Auction.Status.COUNTER_OFFER, Auction.Status.REJECTED,
    ):
        return redirect('users:my_applications')
    return render(request, 'users/application_status.html', {'application': latest})


@login_required
def accept_counter_offer(request, loan_id):
    """Dlžník prijme protiponuku platformy (nižšia suma) - žiadosť sa upraví
    na ponúknutú sumu a vráti sa k administrátorovi na finálne schválenie."""
    auction = get_object_or_404(
        Auction, pk=loan_id, borrower=request.user, status=Auction.Status.COUNTER_OFFER,
    )
    if request.method == 'POST' and auction.counter_offer_amount:
        auction.amount_requested = auction.counter_offer_amount
        auction.status = Auction.Status.PENDING_REVIEW
        auction.save(update_fields=['amount_requested', 'status'])
        messages.success(request, 'Protiponuka bola prijatá, žiadosť opäť čaká na finálne posúdenie.')
    return redirect('users:application_status')


@login_required
def reject_counter_offer(request, loan_id):
    """Dlžník odmietne protiponuku platformy - žiadosť sa uzavrie ako zamietnutá."""
    auction = get_object_or_404(
        Auction, pk=loan_id, borrower=request.user, status=Auction.Status.COUNTER_OFFER,
    )
    if request.method == 'POST':
        auction.status = Auction.Status.REJECTED
        auction.save(update_fields=['status'])
        messages.info(request, 'Protiponuka bola odmietnutá.')
    return redirect('users:application_status')


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


#: Stavy žiadosti, ktoré znamenajú, že bola aspoň raz administrátorom schválená
#: (dlžník teda má prístup do zvyšku menu, nielen na stránku so stavom žiadosti).
_APPROVED_STATUSES = [
    Auction.Status.ACTIVE, Auction.Status.SIGNING, Auction.Status.FUNDED, Auction.Status.CLOSED,
]


def _borrower_has_menu_access(user):
    """True, ak mal dlžník aspoň raz žiadosť schválenú administrátorom - predtým
    má prístup len na stránku so stavom žiadosti (users:application_status)."""
    return Auction.objects.filter(borrower=user, status__in=_APPROVED_STATUSES).exists()


def _require_borrower_menu_access(request):
    """Spoločná kontrola pre všetky stránky menu pre dlžníkov - ak žiadosť
    ešte nebola schválená (čaká sa, zamietnutá, protiponuka), presmeruje na
    stránku so stavom žiadosti. Vráti None, ak je prístup povolený."""
    if request.user.role == User.Role.BORROWER and not _borrower_has_menu_access(request.user):
        return redirect('users:application_status')
    return None


@login_required
def my_applications(request):
    """Hlavná vstupná stránka prostredia pre dlžníkov - prehľad stavu účtu,
    aktuálneho dlhu, najbližšej splatnosti a zoznamu vlastných žiadostí.
    Ak má dlžník všetky pôžičky splatené (alebo zatiaľ žiadnu žiadosť),
    "Požičať si znova"/"Požiadať o pôžičku" ho vráti na kalkulačku parametrov
    novej pôžičky (users:loan_application)."""
    gate = _require_borrower_menu_access(request)
    if gate:
        return gate
    applications = Auction.objects.filter(borrower=request.user)
    active_loans = applications.filter(status=Auction.Status.FUNDED)
    closed_loans = applications.filter(status=Auction.Status.CLOSED)
    pending_applications = applications.filter(status=Auction.Status.ACTIVE)
    has_approved = active_loans.exists() or closed_loans.exists()

    for loan in active_loans:
        _annotate_loan(loan)

    total_debt = sum((loan.repay_amount for loan in active_loans), Decimal('0'))
    next_due_loan = min(active_loans, key=lambda loan: loan.due_date, default=None)

    return render(request, 'users/my_applications.html', {
        'applications': applications,
        'has_approved': has_approved,
        'active_loans': active_loans,
        'closed_loans_count': closed_loans.count(),
        'pending_applications': pending_applications,
        'total_debt': total_debt,
        'next_due_loan': next_due_loan,
        'has_any_application': applications.exists(),
    })


@login_required
def my_loans(request):
    """Prostredie pre dlžníkov - prístupné až keď má aspoň jednu schválenú (vyfinancovanú,
    alebo čakajúcu na podpis zmluvy) pôžičku. Obsahuje aktuálny stav pôžičky aj údaje,
    ako a kam ju zaplatiť."""
    loans = Auction.objects.filter(
        borrower=request.user,
        status__in=[Auction.Status.SIGNING, Auction.Status.FUNDED, Auction.Status.CLOSED],
    )
    if not loans.exists():
        messages.warning(
            request,
            'Do prostredia pre dlžníkov sa dostaneš, až keď investor financuje aspoň jednu tvoju žiadosť.',
        )
        return redirect('users:my_applications')

    for loan in loans.filter(status=Auction.Status.FUNDED):
        _annotate_loan(loan)

    return render(request, 'users/my_loans.html', {
        'loans': loans,
        'bank_details': REPAYMENT_BANK_DETAILS,
        'postpone_fee': POSTPONE_FEE,
    })


@login_required
def sign_loan_contract(request, loan_id):
    """Dlžník podpíše Zmluvu o pôžičke priamo vo svojom účte - až po podpise
    sa pôžička považuje za schválenú (FUNDED) a peniaze mu vyplácame. Pred
    podpisom musí mať dlžník overenú e-mailovú adresu - ak nie je, zobrazí
    sa mu najprv výzva na overenie (odkaz v e-maile)."""
    loan = get_object_or_404(Auction, pk=loan_id, borrower=request.user, status=Auction.Status.SIGNING)
    bid = loan.bids.select_related('lender').first()
    if not request.user.email_verified:
        return redirect('users:verify_email_request')
    if request.method == 'POST':
        from django.utils import timezone
        loan.contract_signed_at = timezone.now()
        loan.status = Auction.Status.FUNDED
        loan.save(update_fields=['contract_signed_at', 'status'])
        send_loan_approved(loan.borrower, loan)
        messages.success(
            request,
            'Zmluva bola podpísaná. Peniaze ti pošleme na tvoj bankový účet v pracovné dni od 8:00 do 16:00.',
        )
        return redirect('users:my_loans')
    return render(request, 'users/sign_loan_contract.html', {'loan': loan, 'bid': bid})


def _post_verify_redirect(user):
    """Kam používateľa presmerovať po úspešnom overení e-mailu - podľa role."""
    if user.role == User.Role.BORROWER:
        return redirect('users:my_loans')
    return redirect('auctions:investor_dashboard')


@login_required
def verify_email_request(request):
    """Stránka na overenie e-mailu - u dlžníka sa zobrazí pred podpisom zmluvy,
    u investora pred prvým vkladom/výberom peňazí (vyžaduje overený e-mail, aby
    bezpečnostný kód a platobné údaje chodili naozaj majiteľovi účtu)."""
    if request.user.email_verified:
        return _post_verify_redirect(request.user)
    if request.method == 'POST':
        if not request.user.email_verification_token:
            request.user.email_verification_token = _generate_email_verification_token()
            request.user.save(update_fields=['email_verification_token'])
        verify_url = request.build_absolute_uri(
            reverse_lazy('users:verify_email_confirm', kwargs={'token': request.user.email_verification_token}),
        )
        send_email_verification(request.user, verify_url)
        messages.success(request, f'Overovací odkaz sme poslali na {request.user.email}.')
    template = (
        'users/verify_email_request.html'
        if request.user.role == User.Role.BORROWER
        else 'users/verify_email_request_investor.html'
    )
    return render(request, template)


def verify_email_confirm(request, token):
    """Potvrdenie e-mailu kliknutím na odkaz z e-mailu."""
    user = User.objects.filter(email_verification_token=token).exclude(email_verification_token='').first()
    if user:
        user.email_verified = True
        user.save(update_fields=['email_verified'])
        messages.success(request, 'E-mail bol úspešne overený.')
        if request.user.is_authenticated and request.user.pk == user.pk:
            return _post_verify_redirect(user)
    else:
        messages.error(request, 'Neplatný alebo už použitý overovací odkaz.')
    return redirect('core:landing')


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


#: Jednorazový bonus (€) pre pozývateľa aj pozvaného po prvej investícii pozvaného.
REFERRAL_BONUS = Decimal('10')


@login_required
def referral(request):
    """Odporúčací program - vlastný odkaz na pozvanie, prehľad pozvaných a
    (pre investorov) vernostný program podľa celkového investovaného objemu.
    Šablóna sa líši podľa role prihláseného používateľa."""
    gate = _require_borrower_menu_access(request)
    if gate:
        return gate
    referral_url = request.build_absolute_uri(
        f"{reverse_lazy('users:signup')}?ref={request.user.referral_code}",
    )
    referrals = request.user.referrals.all()
    context = {
        'referral_code': request.user.referral_code,
        'referral_url': referral_url,
        'referrals': referrals,
        'referral_bonus': REFERRAL_BONUS,
        'rewarded_count': referrals.filter(referral_reward_granted=True).count(),
        'total_referral_bonus': referrals.filter(referral_reward_granted=True).count() * REFERRAL_BONUS,
    }
    if request.user.role == User.Role.BORROWER:
        return render(request, 'users/referral_borrower.html', context)

    context.update({
        'loyalty_tier': request.user.loyalty_tier,
        'loyalty_tier_label': request.user.loyalty_tier_label,
        'loyalty_next_threshold': request.user.loyalty_next_threshold,
        'total_invested_lifetime': request.user.total_invested_lifetime,
        'loyalty_tiers': User.LoyaltyTier,
    })
    return render(request, 'users/referral_investor.html', context)


@login_required
def my_offers(request):
    """Ponuky pre dlžníka - po úspešnom splatení pôžičky sem chodia ponuky
    na novú pôžičku, spolu s platobnými údajmi aktuálnej aktívnej pôžičky
    (rovnako ako v časti Moje pôžičky)."""
    gate = _require_borrower_menu_access(request)
    if gate:
        return gate
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
    gate = _require_borrower_menu_access(request)
    if gate:
        return gate
    return render(request, 'users/my_profile.html')


@login_required
def my_contracts(request):
    """Moje zmluvy - prehľad zmluvných dokumentov k pôžičkám dlžníka."""
    contracts = Auction.objects.filter(
        borrower=request.user,
        status__in=[Auction.Status.SIGNING, Auction.Status.FUNDED, Auction.Status.CLOSED],
    )
    return render(request, 'users/my_contracts.html', {'contracts': contracts})


def _get_contract_loan_and_bid(request, loan_id):
    """Spoločná pomocná funkcia - nájde pôžičku dlžníka a jej financujúcu investíciu (Bid)."""
    loan = get_object_or_404(
        Auction, pk=loan_id, borrower=request.user,
        status__in=[Auction.Status.SIGNING, Auction.Status.FUNDED, Auction.Status.CLOSED],
    )
    bid = loan.bids.select_related('lender').first()
    return loan, bid


@login_required
def contract_loan_agreement_pdf(request, loan_id):
    """Stiahnutie Zmluvy o pôžičke (PDF) dlžníkom."""
    from core.contracts import generate_loan_agreement_pdf
    loan, bid = _get_contract_loan_and_bid(request, loan_id)
    if not bid:
        messages.error(request, 'K tejto pôžičke zatiaľ nie je priradený žiadny investor.')
        return redirect('users:my_contracts')
    return generate_loan_agreement_pdf(loan, bid)


@login_required
def contract_payment_notice_pdf(request, loan_id):
    """Stiahnutie Predpisu k úhrade (PDF) dlžníkom."""
    from core.contracts import generate_payment_notice_pdf
    loan, bid = _get_contract_loan_and_bid(request, loan_id)
    if not bid:
        messages.error(request, 'K tejto pôžičke zatiaľ nie je priradený žiadny investor.')
        return redirect('users:my_contracts')
    return generate_payment_notice_pdf(loan, bid)


@login_required
def contract_debt_discharge_pdf(request, loan_id):
    """Stiahnutie Potvrdenia o zániku dlhu (PDF) - len pre splatené pôžičky."""
    from core.contracts import generate_debt_discharge_certificate_pdf
    loan = get_object_or_404(Auction, pk=loan_id, borrower=request.user, status=Auction.Status.CLOSED)
    bid = loan.bids.select_related('lender').first()
    if not bid:
        messages.error(request, 'K tejto pôžičke zatiaľ nie je priradený žiadny investor.')
        return redirect('users:my_contracts')
    return generate_debt_discharge_certificate_pdf(loan, bid)


@login_required
def account_settings(request):
    """Nastavenia účtu - vrátane zmeny bankového účtu (IBAN), na ktorý sa
    vyplácajú peniaze (dostupné pre investora aj dlžníka)."""
    gate = _require_borrower_menu_access(request)
    if gate:
        return gate
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
        return redirect('users:my_applications')
    return redirect('auctions:investor_dashboard')


def impersonate_stop(request):
    if request.session.pop('impersonate_user_id', None):
        messages.info(request, 'Návrat do administrátorského účtu.')
    return redirect('users:impersonate_list')

