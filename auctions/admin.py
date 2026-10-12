from django.contrib import admin
from django.utils import timezone

from .models import Auction, WalletTransaction


@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    """Posudzovanie žiadostí o pôžičku - admin najprv overí dlžníka (napr. v
    registri dlžníkov/úverov) a potom žiadosť schváli, zamietne, alebo pošle
    protiponuku na nižšiu sumu. Až po schválení sa žiadosť zobrazí investorom."""
    list_display = (
        'title', 'borrower', 'amount_requested', 'max_interest_rate',
        'duration_days', 'status', 'ends_at', 'bought_back',
    )
    list_filter = ('status', 'bought_back')
    search_fields = ('title', 'borrower__username')
    list_editable = ()
    fields = (
        'borrower', 'title', 'description', 'amount_requested', 'max_interest_rate',
        'duration_days', 'status', 'ends_at', 'rejection_reason', 'counter_offer_amount',
        'bought_back',
    )
    actions = ['approve_applications', 'reject_applications', 'send_counter_offer']

    @admin.action(description='Schváliť žiadosť (žiadosť pôjde medzi ponuky pre investorov)')
    def approve_applications(self, request, queryset):
        from core.emails import send_loan_application_approved

        for auction in queryset.filter(status__in=[Auction.Status.PENDING_REVIEW, Auction.Status.COUNTER_OFFER]):
            auction.status = Auction.Status.ACTIVE
            auction.reviewed_at = timezone.now()
            auction.save(update_fields=['status', 'reviewed_at'])
            send_loan_application_approved(auction.borrower, auction)

    @admin.action(description='Zamietnuť žiadosť (vyplň najprv dôvod zamietnutia v detaile žiadosti)')
    def reject_applications(self, request, queryset):
        from core.emails import send_loan_application_rejected

        for auction in queryset.filter(status=Auction.Status.PENDING_REVIEW):
            auction.status = Auction.Status.REJECTED
            auction.reviewed_at = timezone.now()
            auction.save(update_fields=['status', 'reviewed_at'])
            send_loan_application_rejected(auction.borrower, auction)

    @admin.action(description='Poslať protiponuku (vyplň najprv nižšiu sumu v detaile žiadosti)')
    def send_counter_offer(self, request, queryset):
        from django.contrib import messages as dj_messages
        from core.emails import send_loan_application_counter_offer

        for auction in queryset.filter(status=Auction.Status.PENDING_REVIEW):
            if not auction.counter_offer_amount:
                dj_messages.warning(
                    request,
                    f'Žiadosť #{auction.pk}: najprv ulož nižšiu sumu do poľa "Counter offer amount".',
                )
                continue
            auction.status = Auction.Status.COUNTER_OFFER
            auction.reviewed_at = timezone.now()
            auction.save(update_fields=['status', 'reviewed_at'])
            send_loan_application_counter_offer(auction.borrower, auction)


@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):
    """Evidencia manuálnych bankových prevodov - tu admin potvrdzuje vklady
    (po prijatí platby na firemný účet) a označuje výbery ako vybavené
    (po odoslaní peňazí investorovi)."""
    list_display = ('user', 'kind', 'amount', 'status', 'iban', 'created_at', 'completed_at')
    list_filter = ('kind', 'status')
    search_fields = ('user__username', 'user__display_id', 'iban')
    actions = ['mark_completed', 'mark_rejected']

    @admin.action(description='Označiť ako vybavené (platba odoslaná/prijatá)')
    def mark_completed(self, request, queryset):
        from django.utils import timezone

        for tx in queryset.filter(status=WalletTransaction.Status.PENDING):
            if tx.kind == WalletTransaction.Kind.DEPOSIT:
                tx.user.wallet_balance += tx.amount
                tx.user.save(update_fields=['wallet_balance'])
            tx.status = WalletTransaction.Status.COMPLETED
            tx.completed_at = timezone.now()
            tx.save(update_fields=['status', 'completed_at'])

    @admin.action(description='Zamietnuť (napr. platba neprišla / chybný VS)')
    def mark_rejected(self, request, queryset):
        from django.utils import timezone

        for tx in queryset.filter(status=WalletTransaction.Status.PENDING):
            if tx.kind == WalletTransaction.Kind.WITHDRAWAL:
                # Výber bol už odpísaný z peňaženky pri vytvorení žiadosti - pri zamietnutí sumu vrátime.
                tx.user.wallet_balance += tx.amount
                tx.user.save(update_fields=['wallet_balance'])
            tx.status = WalletTransaction.Status.REJECTED
            tx.completed_at = timezone.now()
            tx.save(update_fields=['status', 'completed_at'])

