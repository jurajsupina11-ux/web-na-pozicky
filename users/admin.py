from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Doplňujúce údaje', {'fields': ('phone_number', 'role', 'is_verified', 'date_of_birth')}),
    )
    list_display = ('username', 'email', 'role', 'is_verified', 'is_staff', 'referral_code')
    list_filter = UserAdmin.list_filter + ('role', 'is_verified')
    search_fields = UserAdmin.search_fields + ('referral_code', 'display_id')

