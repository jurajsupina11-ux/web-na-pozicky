from django.contrib import admin

from .models import Auction


@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'borrower', 'amount_requested', 'max_interest_rate',
        'duration_days', 'status', 'ends_at',
    )
    list_filter = ('status',)
    search_fields = ('title', 'borrower__username')

