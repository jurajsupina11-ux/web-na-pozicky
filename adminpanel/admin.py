from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'admin', 'target_model', 'target_id', 'created_at')
    list_filter = ('target_model',)
    search_fields = ('action', 'details', 'admin__username')
    readonly_fields = ('admin', 'action', 'details', 'target_model', 'target_id', 'created_at')

    def has_add_permission(self, request):
        return False
