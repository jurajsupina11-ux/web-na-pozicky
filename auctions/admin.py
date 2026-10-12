from django.contrib import admin

from .models import Auction, WalletTransaction


@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'borrower', 'amount_requested', 'max_interest_rate',
        'duration_days', 'status', 'ends_at', 'bought_back',
    )
    list_filter = ('status', 'bought_back')
    search_fields = ('title', 'borrower__username')


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

