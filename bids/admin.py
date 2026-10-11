from django.contrib import admin

from .models import Bid


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('auction', 'lender', 'amount', 'interest_rate', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('auction__title', 'lender__username')

