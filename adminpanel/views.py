"""Vlastné admin prostredie (štýlované v appke) pre bežnú dennú prevádzku -
schvaľovanie žiadostí, potvrdzovanie platieb, správa používateľov. Holý Django
admin (/admin/) zostáva naďalej dostupný pre technickejšie zásahy."""
from decimal import Decimal, InvalidOperation
from functools import wraps

from django.contrib import messages
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from auctions.models import Auction, WalletTransaction
from bids.models import Bid
from core.emails import (
    send_loan_application_approved, send_loan_application_counter_offer,
    send_loan_application_rejected,
)
from users.models import User

from .models import AuditLog, log_action


def admin_required(view_func):
    """Dekorátor - vpustí len prihláseného superusera (rovnaká podmienka ako
    pri impersonácii v users.views._is_admin_request)."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.is_superuser):
            return redirect('users:login')
        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def dashboard(request):
    """Súhrnné čísla na prvý pohľad - čo čaká na vybavenie, aké je portfólio."""
    pending_applications = Auction.objects.filter(status=Auction.Status.PENDING_REVIEW).count()
    counter_offers = Auction.objects.filter(status=Auction.Status.COUNTER_OFFER).count()
    pending_wallet = WalletTransaction.objects.filter(status=WalletTransaction.Status.PENDING)
    pending_deposits = pending_wallet.filter(kind=WalletTransaction.Kind.DEPOSIT).count()
    pending_withdrawals = pending_wallet.filter(kind=WalletTransaction.Kind.WITHDRAWAL).count()

    active_loans = Auction.objects.filter(status=Auction.Status.FUNDED)
    overdue_loans = [loan for loan in active_loans if loan.computed_due_date < timezone.now()]

    total_invested = Bid.objects.aggregate(total=Sum('amount'))['total'] or Decimal('0')
    total_wallet_balance = User.objects.aggregate(total=Sum('wallet_balance'))['total'] or Decimal('0')

    week_ago = timezone.now() - timezone.timedelta(days=7)
    new_users_week = User.objects.filter(date_joined__gte=week_ago, is_superuser=False).count()

    context = {
        'pending_applications': pending_applications,
        'counter_offers': counter_offers,
        'pending_deposits': pending_deposits,
        'pending_withdrawals': pending_withdrawals,
        'active_loans_count': active_loans.count(),
        'overdue_loans_count': len(overdue_loans),
        'total_invested': total_invested,
        'total_wallet_balance': total_wallet_balance,
        'new_users_week': new_users_week,
        'recent_audit': AuditLog.objects.all()[:8],
    }
    return render(request, 'adminpanel/dashboard.html', context)


@admin_required
def applications_list(request):
    """Zoznam žiadostí o pôžičku s filtrom podľa stavu."""
    status_filter = request.GET.get('status', 'pending_review')
    applications = Auction.objects.select_related('borrower').all()
    if status_filter and status_filter != 'all':
        applications = applications.filter(status=status_filter)
    return render(request, 'adminpanel/applications_list.html', {
        'applications': applications,
        'status_filter': status_filter,
        'status_choices': Auction.Status.choices,
    })


@admin_required
def application_detail(request, pk):
    """Detail žiadosti - KYC údaje dlžníka a história jeho predošlých žiadostí."""
    application = get_object_or_404(Auction.objects.select_related('borrower'), pk=pk)
    borrower_history = Auction.objects.filter(borrower=application.borrower).exclude(pk=pk)
    return render(request, 'adminpanel/application_detail.html', {
        'application': application,
        'borrower': application.borrower,
        'borrower_history': borrower_history,
    })


@admin_required
def application_approve(request, pk):
    application = get_object_or_404(
        Auction, pk=pk, status__in=[Auction.Status.PENDING_REVIEW, Auction.Status.COUNTER_OFFER],
    )
    if request.method == 'POST':
        application.status = Auction.Status.ACTIVE
        application.reviewed_at = timezone.now()
        application.save(update_fields=['status', 'reviewed_at'])
        send_loan_application_approved(application.borrower, application)
        log_action(
            request.user, 'Schválil žiadosť o pôžičku',
            f'#{application.pk} - {application.amount_requested} € ({application.borrower.username})',
            target_model='Auction', target_id=application.pk,
        )
        messages.success(request, f'Žiadosť #{application.pk} bola schválená.')
    return redirect('adminpanel:application_detail', pk=pk)


@admin_required
def application_reject(request, pk):
    application = get_object_or_404(
        Auction, pk=pk, status__in=[Auction.Status.PENDING_REVIEW, Auction.Status.COUNTER_OFFER],
    )
    if request.method == 'POST':
        reason = request.POST.get('reason', '').strip()
        application.status = Auction.Status.REJECTED
        application.rejection_reason = reason
        application.reviewed_at = timezone.now()
        application.save(update_fields=['status', 'rejection_reason', 'reviewed_at'])
        send_loan_application_rejected(application.borrower, application)
        log_action(
            request.user, 'Zamietol žiadosť o pôžičku',
            f'#{application.pk} - dôvod: {reason or "neuvedený"}',
            target_model='Auction', target_id=application.pk,
        )
        messages.info(request, f'Žiadosť #{application.pk} bola zamietnutá.')
    return redirect('adminpanel:application_detail', pk=pk)


@admin_required
def application_counter_offer(request, pk):
    application = get_object_or_404(Auction, pk=pk, status=Auction.Status.PENDING_REVIEW)
    if request.method == 'POST':
        try:
            amount = Decimal(request.POST.get('amount', '0'))
        except InvalidOperation:
            amount = Decimal('0')
        if amount <= 0 or amount >= application.amount_requested:
            messages.error(request, 'Protiponuka musí byť kladná suma nižšia ako pôvodne požadovaná.')
            return redirect('adminpanel:application_detail', pk=pk)
        application.counter_offer_amount = amount
        application.status = Auction.Status.COUNTER_OFFER
        application.reviewed_at = timezone.now()
        application.save(update_fields=['counter_offer_amount', 'status', 'reviewed_at'])
        send_loan_application_counter_offer(application.borrower, application)
        log_action(
            request.user, 'Poslal protiponuku k žiadosti',
            f'#{application.pk} - ponúknuté {amount} € namiesto {application.amount_requested} €',
            target_model='Auction', target_id=application.pk,
        )
        messages.success(request, f'Protiponuka {amount} € bola odoslaná dlžníkovi.')
    return redirect('adminpanel:application_detail', pk=pk)


@admin_required
def wallet_list(request):
    """Čakajúce aj vybavené vklady/výbery peňazí."""
    status_filter = request.GET.get('status', 'pending')
    transactions = WalletTransaction.objects.select_related('user').all()
    if status_filter and status_filter != 'all':
        transactions = transactions.filter(status=status_filter)
    return render(request, 'adminpanel/wallet_list.html', {
        'transactions': transactions,
        'status_filter': status_filter,
    })


@admin_required
def wallet_confirm(request, pk):
    tx = get_object_or_404(WalletTransaction, pk=pk, status=WalletTransaction.Status.PENDING)
    if request.method == 'POST':
        if tx.kind == WalletTransaction.Kind.DEPOSIT:
            tx.user.wallet_balance += tx.amount
            tx.user.save(update_fields=['wallet_balance'])
        tx.status = WalletTransaction.Status.COMPLETED
        tx.completed_at = timezone.now()
        tx.save(update_fields=['status', 'completed_at'])
        log_action(
            request.user, f'Potvrdil {tx.get_kind_display().lower()}',
            f'{tx.amount} € - {tx.user.username}',
            target_model='WalletTransaction', target_id=tx.pk,
        )
        messages.success(request, f'{tx.get_kind_display()} {tx.amount} € bol(a) potvrdený(á).')
    return redirect('adminpanel:wallet_list')


@admin_required
def wallet_reject(request, pk):
    tx = get_object_or_404(WalletTransaction, pk=pk, status=WalletTransaction.Status.PENDING)
    if request.method == 'POST':
        if tx.kind == WalletTransaction.Kind.WITHDRAWAL:
            tx.user.wallet_balance += tx.amount
            tx.user.save(update_fields=['wallet_balance'])
        tx.status = WalletTransaction.Status.REJECTED
        tx.completed_at = timezone.now()
        tx.save(update_fields=['status', 'completed_at'])
        log_action(
            request.user, f'Zamietol {tx.get_kind_display().lower()}',
            f'{tx.amount} € - {tx.user.username}',
            target_model='WalletTransaction', target_id=tx.pk,
        )
        messages.info(request, f'{tx.get_kind_display()} {tx.amount} € bol(a) zamietnutý(á).')
    return redirect('adminpanel:wallet_list')


@admin_required
def loans_list(request):
    """Prehľad aktívnych pôžičiek, zvýraznené tie po splatnosti."""
    loans = Auction.objects.filter(status=Auction.Status.FUNDED).select_related('borrower')
    now = timezone.now()
    for loan in loans:
        loan.is_overdue = loan.computed_due_date < now
    loans = sorted(loans, key=lambda loan: loan.computed_due_date)
    return render(request, 'adminpanel/loans_list.html', {'loans': loans})


@admin_required
def users_list(request):
    """Vyhľadávanie v používateľoch podľa mena/rodného čísla/display_id."""
    query = request.GET.get('q', '').strip()
    role_filter = request.GET.get('role', '')
    users = User.objects.filter(is_superuser=False).order_by('-date_joined')
    if query:
        users = users.filter(
            Q(username__icontains=query) | Q(display_id__icontains=query) |
            Q(first_name__icontains=query) | Q(last_name__icontains=query) |
            Q(email__icontains=query) | Q(birth_number__icontains=query),
        )
    if role_filter:
        users = users.filter(role=role_filter)
    return render(request, 'adminpanel/users_list.html', {
        'users': users[:200],
        'query': query,
        'role_filter': role_filter,
    })


@admin_required
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk, is_superuser=False)
    applications = Auction.objects.filter(borrower=user)
    investments = Bid.objects.filter(lender=user).select_related('auction')
    return render(request, 'adminpanel/user_detail.html', {
        'target': user,
        'applications': applications,
        'investments': investments,
    })


@admin_required
def user_toggle_block(request, pk):
    user = get_object_or_404(User, pk=pk, is_superuser=False)
    if request.method == 'POST':
        user.is_blocked = not user.is_blocked
        user.save(update_fields=['is_blocked'])
        action = 'Zablokoval účet' if user.is_blocked else 'Odblokoval účet'
        log_action(request.user, action, user.username, target_model='User', target_id=user.pk)
        messages.success(
            request,
            f'Účet {user.username} bol {"zablokovaný" if user.is_blocked else "odblokovaný"}.',
        )
    return redirect('adminpanel:user_detail', pk=pk)


@admin_required
def marketplace_list(request):
    """Aktuálne ponúkané investície na sekundárnom trhu (len na čítanie)."""
    listings = Bid.objects.filter(for_sale=True).select_related('auction', 'lender')
    return render(request, 'adminpanel/marketplace_list.html', {'listings': listings})


@admin_required
def audit_log(request):
    entries = AuditLog.objects.select_related('admin').all()[:300]
    return render(request, 'adminpanel/audit_log.html', {'entries': entries})
