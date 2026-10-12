from decimal import Decimal

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Auction(models.Model):
    """A short-term loan request put up for auction by a borrower.

    Pôžičky sa financujú vždy len celé naraz (all-or-nothing) - jedna pôžička
    = jeden investor = jedna ponuka (Bid). Čiastočné spolufinancovanie viacerými
    investormi nie je podporované."""

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Koncept'
        ACTIVE = 'active', 'Aktívna'
        CLOSED = 'closed', 'Uzavretá'
        CANCELLED = 'cancelled', 'Zrušená'
        SIGNING = 'signing', 'Čaká na podpis zmluvy'
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

    # Podpis zmluvy o pôžičke dlžníkom - až po podpise sa peniaze vyplácajú
    # (pôžička prejde zo stavu SIGNING do FUNDED).
    contract_signed_at = models.DateTimeField(
        null=True, blank=True,
        help_text='Kedy dlžník podpísal Zmluvu o pôžičke - predtým sa peniaze nevyplácajú.',
    )

    # Garancia odkúpenia - ak dlžník nesplatí do BUYBACK_DAYS dní po splatnosti,
    # platforma automaticky odkúpi pohľadávku od investora (investor dostane
    # istinu + dohodnutý úrok späť na peňaženku, platforma preberá vymáhanie).
    bought_back = models.BooleanField(
        default=False,
        help_text='Pôžička bola automaticky odkúpená platformou od investora (garancia odkúpenia po 90 dňoch).',
    )
    bought_back_at = models.DateTimeField(null=True, blank=True)

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
    def computed_due_date(self):
        """Termín splatnosti pôžičky vrátane prípadných odkladov."""
        from datetime import timedelta
        return self.starts_at + timedelta(days=self.duration_days + self.postponed_days)

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


class WalletTransaction(models.Model):
    """Evidencia vkladov a výberov investorskej peňaženky. Platforma nemá
    napojenú platobnú bránu - investor pošle peniaze na náš bankový účet,
    administrátor manuálne potvrdí príjem a pripíše sumu na peňaženku
    (DEPOSIT); pri výbere investor požiada o výber (vyžaduje bezpečnostný
    kód), suma sa mu okamžite odpíše z peňaženky a administrátor manuálne
    zrealizuje bankový prevod a označí transakciu ako vybavenú."""

    class Kind(models.TextChoices):
        DEPOSIT = 'deposit', 'Vklad'
        WITHDRAWAL = 'withdrawal', 'Výber'

    class Status(models.TextChoices):
        PENDING = 'pending', 'Čaká sa'
        COMPLETED = 'completed', 'Vybavené'
        REJECTED = 'rejected', 'Zamietnuté'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wallet_transactions',
    )
    kind = models.CharField(max_length=10, choices=Kind.choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    iban = models.CharField(
        max_length=34, blank=True,
        help_text='IBAN, na ktorý sa má suma odoslať (pri výbere) - kópia z profilu v čase žiadosti.',
    )
    note = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.get_kind_display()} {self.amount} € - {self.user} ({self.get_status_display()})'

