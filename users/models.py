import random
from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.db import models


def _generate_display_id():
    """Vygeneruje náhodný unikátny 6-miestny verejný identifikátor používateľa.
    Slúži na anonymné zobrazenie v appke (iní používatelia vidia len toto číslo,
    nikdy reálne meno) - napr. #482913."""
    while True:
        candidate = f'{random.randint(0, 999999):06d}'
        if not User.objects.filter(display_id=candidate).exists():
            return candidate


class User(AbstractUser):
    """Custom user model so we can extend it later (KYC, phone, role...)."""

    class Role(models.TextChoices):
        BORROWER = 'borrower', 'Žiadateľ o pôžičku'
        LENDER = 'lender', 'Veriteľ'
        BOTH = 'both', 'Žiadateľ aj veriteľ'

    #: Verejný anonymný identifikátor (6-miestne číslo) - zobrazuje sa ostatným
    #: používateľom namiesto mena/username. Reálne meno vidí len majiteľ účtu
    #: a administrátor.
    display_id = models.CharField(max_length=6, unique=True, blank=True)

    phone_number = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.BOTH)
    is_verified = models.BooleanField(
        default=False,
        help_text='Overená identita (KYC) - potrebné pred vytvorením aukcie alebo ponuky.',
    )
    date_of_birth = models.DateField(null=True, blank=True)

    # KYC / citlivé údaje - vyžadované pri žiadosti o prvú pôžičku
    id_card_number = models.CharField('Číslo občianskeho preukazu', max_length=20, blank=True)
    birth_number = models.CharField('Rodné číslo', max_length=15, blank=True)
    street_address = models.CharField('Ulica a číslo', max_length=120, blank=True)
    city = models.CharField('Mesto', max_length=80, blank=True)
    postal_code = models.CharField('PSČ', max_length=10, blank=True)
    bank_account_iban = models.CharField('IBAN pre výplatu pôžičky', max_length=34, blank=True)
    kyc_completed = models.BooleanField(
        default=False,
        help_text='Žiadateľ vyplnil citlivé údaje (OP, rodné číslo, adresa) pri prvej žiadosti.',
    )

    # Investorská peňaženka - voľné prostriedky na investovanie/vyplatenie.
    wallet_balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('0'),
        help_text='Voľný zostatok investora na účte (pripravený na investíciu alebo výplatu).',
    )

    def save(self, *args, **kwargs):
        if not self.display_id:
            self.display_id = _generate_display_id()
        super().save(*args, **kwargs)

    @property
    def display_name(self):
        """Verejné zobrazenie používateľa - vždy len anonymné číslo #123456,
        nikdy reálne meno ani username. Použiť všade, kde jeden používateľ
        vidí informácie o inom používateľovi (napr. v zozname žiadostí,
        ponúk na sekundárnom trhu a pod.)."""
        return f'#{self.display_id}'

    def __str__(self):
        return self.username
