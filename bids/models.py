from django.conf import settings
from django.db import models


class Bid(models.Model):
    """A lender's offer on a given auction."""

    class Status(models.TextChoices):
        PENDING = 'pending', 'Čaká sa'
        ACCEPTED = 'accepted', 'Prijatá'
        REJECTED = 'rejected', 'Zamietnutá'
        WITHDRAWN = 'withdrawn', 'Stiahnutá'

    auction = models.ForeignKey(
        'auctions.Auction',
        on_delete=models.CASCADE,
        related_name='bids',
    )
    lender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bids',
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text='Navrhovaný úrok (% p.a.).',
    )
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Sekundárny trh - investor môže svoju aktívnu investíciu (podiel na pôžičke)
    # ponúknuť na predaj inému investorovi, napr. ak potrebuje peniaze skôr.
    for_sale = models.BooleanField(
        default=False,
        help_text='Investor ponúka svoj podiel na tejto pôžičke na predaj inému investorovi.',
    )
    for_sale_since = models.DateTimeField(
        null=True, blank=True,
        help_text='Kedy bola investícia ponúknutá na predaj - 5 minút od tohto času je možné predaj ešte zastaviť.',
    )

    class Meta:
        ordering = ['interest_rate', '-amount']
        constraints = [
            models.UniqueConstraint(
                fields=['auction', 'lender'],
                name='unique_bid_per_lender_per_auction',
            )
        ]

    def __str__(self):
        return f'{self.lender} -> {self.auction} ({self.amount} € @ {self.interest_rate}%)'

    #: Počet sekúnd, počas ktorých je možné zastaviť predaj investície po jej
    #: ponúknutí na sekundárnom trhu.
    SALE_CANCEL_WINDOW_SECONDS = 5 * 60

    @property
    def sale_cancel_deadline(self):
        if not self.for_sale or not self.for_sale_since:
            return None
        from datetime import timedelta
        return self.for_sale_since + timedelta(seconds=self.SALE_CANCEL_WINDOW_SECONDS)

    @property
    def can_cancel_sale(self):
        from django.utils import timezone
        deadline = self.sale_cancel_deadline
        return bool(deadline and timezone.now() < deadline)

