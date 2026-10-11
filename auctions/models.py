from decimal import Decimal

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Auction(models.Model):
    """A short-term loan request put up for auction by a borrower."""

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Koncept'
        ACTIVE = 'active', 'Aktívna'
        CLOSED = 'closed', 'Uzavretá'
        CANCELLED = 'cancelled', 'Zrušená'
        FUNDED = 'funded', 'Vyfinancovaná'

    borrower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='auctions',
    )
    title = models.CharField(max_length=140)
    description = models.TextField(blank=True)
    amount_requested = models.DecimalField(max_digits=10, decimal_places=2)
    max_interest_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text='Maximálny úrok (% p.a.), ktorý je žiadateľ ochotný zaplatiť.',
    )
    duration_days = models.PositiveIntegerField(help_text='Splatnosť pôžičky v dňoch.')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    starts_at = models.DateTimeField(default=timezone.now)
    ends_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Správa splácania dlžníkom - odklad splátky a nahlásenie úhrady.
    postponed_days = models.PositiveIntegerField(
        default=0,
        help_text='Počet dní, o ktoré bola splatnosť predĺžená na žiadosť dlžníka.',
    )
    payment_reported = models.BooleanField(
        default=False,
        help_text='Dlžník nahlásil úhradu pôžičky - čaká na overenie platby.',
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} ({self.amount_requested} €)'

    def get_absolute_url(self):
        return reverse('auctions:detail', kwargs={'pk': self.pk})

    @property
    def is_open(self):
        return self.status == self.Status.ACTIVE and self.ends_at > timezone.now()

    @property
    def total_bid_amount(self) -> Decimal:
        return sum((bid.amount for bid in self.bids.all()), Decimal('0'))

    @property
    def funding_progress(self) -> Decimal:
        if not self.amount_requested:
            return Decimal('0')
        return min(
            Decimal('100'),
            (self.total_bid_amount / self.amount_requested) * Decimal('100'),
        )

