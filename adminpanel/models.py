from django.conf import settings
from django.db import models


class AuditLog(models.Model):
    """Záznam o akcii, ktorú vykonal administrátor vo vlastnom admin prostredí
    (schválenie/zamietnutie žiadosti, potvrdenie platby, zablokovanie účtu...).
    Dôležité pri viacerých adminoch - vieme spätne dohľadať, kto a kedy čo urobil."""

    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='audit_log_entries',
    )
    action = models.CharField(max_length=140)
    details = models.TextField(blank=True)
    target_model = models.CharField(max_length=50, blank=True)
    target_id = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.action} ({self.admin})'


def log_action(admin, action, details='', target_model='', target_id=''):
    """Helper na zapísanie jedného riadku do audit logu."""
    return AuditLog.objects.create(
        admin=admin, action=action, details=details,
        target_model=target_model, target_id=str(target_id),
    )
