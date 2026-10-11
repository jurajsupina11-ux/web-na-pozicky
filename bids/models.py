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

