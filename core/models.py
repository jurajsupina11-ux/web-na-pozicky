from django.conf import settings
from django.db import models


class Notification(models.Model):
    """Interná notifikácia v appke (zvonček v hlavičke) - nezávislá od e-mailu,
    funguje aj kým nie je nastavené SMTP. Zobrazuje sa v investorskom aj
    dlžníckom prostredí."""

    class Kind(models.TextChoices):
        INFO = 'info', 'Informácia'
        SUCCESS = 'success', 'Úspech'
        WARNING = 'warning', 'Upozornenie'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
    )
    kind = models.CharField(max_length=10, choices=Kind.choices, default=Kind.INFO)
    title = models.CharField(max_length=140)
    message = models.TextField(blank=True)
    url = models.CharField(max_length=200, blank=True, help_text='Voliteľný odkaz, kam notifikácia smeruje.')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} -> {self.user}'


def notify(user, title, message='', kind=Notification.Kind.INFO, url=''):
    """Helper na vytvorenie internej notifikácie pre používateľa."""
    return Notification.objects.create(
        user=user, title=title, message=message, kind=kind, url=url,
    )
