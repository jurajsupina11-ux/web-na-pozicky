import random
import string
from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.db import models


def _generate_security_code():
    """Vygeneruje náhodný 8-miestny bezpečnostný kód (číslice) - posiela sa
    investorovi e-mailom po úspešnej registrácii a slúži na potvrdenie žiadosti
    o výber peňazí a na zmenu bankového účtu (IBAN)."""
    return ''.join(random.choices(string.digits, k=8))


def _generate_password():
    """Vygeneruje náhodné 5-miestne číselné heslo pre dlžníka - posiela sa
    e-mailom spolu s používateľským menom (rodné číslo) po schválení žiadosti."""
    return ''.join(random.choices(string.digits, k=5))


def _generate_email_verification_token():
    """Vygeneruje náhodný token na overenie e-mailovej adresy (odkaz v e-maile)."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(random.choices(alphabet, k=32))


def _generate_referral_code():
    """Vygeneruje náhodný unikátny 8-miestny odporúčací kód (písmená+čísla)."""
    alphabet = string.ascii_uppercase + string.digits
    while True:
        candidate = ''.join(random.choices(alphabet, k=8))
        if not User.objects.filter(referral_code=candidate).exists():
            return candidate


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

    # GDPR - súhlas so spracovaním osobných údajov, zaznamenaný pri žiadosti
    # o pôžičku alebo registrácii investora.
    gdpr_consent_given = models.BooleanField(
        default=False,
        help_text='Používateľ súhlasil so spracovaním osobných údajov (GDPR).',
    )
    gdpr_consent_at = models.DateTimeField(
        null=True, blank=True,
        help_text='Čas udelenia GDPR súhlasu.',
    )

    # Referral (odporúčací) program - každý používateľ má svoj unikátny kód,
    # ktorý môže zdieľať. Nový používateľ sa zaregistruje cez odkaz s kódom,
    # po splnení podmienky (prvá investícia/splatená pôžička) dostanú obaja bonus.
    referral_code = models.CharField(max_length=10, unique=True, blank=True)
    referred_by = models.ForeignKey(
        'self',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='referrals',
        help_text='Používateľ, ktorý tohto používateľa pozval (odporučil).',
    )
    referral_reward_granted = models.BooleanField(
        default=False,
        help_text='Odmena za toto odporúčanie už bola pripísaná (aby sa nevyplatila dvakrát).',
    )

    # Bezpečnostný (2FA-like) kód pre investorov - zaslaný e-mailom po úspešnej
    # registrácii, vyžaduje sa pri žiadosti o výber peňazí a pri zmene IBAN.
    security_code = models.CharField(max_length=10, blank=True)

    # Overenie e-mailovej adresy - dlžník ju musí overiť pred podpisom zmluvy.
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=32, blank=True)

    @property
    def masked_birth_number(self):
        """Rodné číslo zobrazené len čiastočne (napr. 9001011234 -> 900101****)
        - aj majiteľovi účtu sa v bežnom zobrazení ukazuje maskované, celé
        číslo nie je nikde v appke verejne vypisované."""
        value = self.birth_number or ''
        if len(value) <= 4:
            return value
        return value[:-4] + '*' * 4

    @property
    def masked_id_card_number(self):
        """Číslo OP zobrazené len čiastočne (napr. AB123456 -> AB12****)."""
        value = self.id_card_number or ''
        if len(value) <= 4:
            return value
        return value[:-4] + '*' * 4

    @property
    def masked_bank_account_iban(self):
        """IBAN zobrazený len čiastočne (prvé 4 a posledné 4 znaky)."""
        value = (self.bank_account_iban or '').replace(' ', '')
        if len(value) <= 8:
            return value
        return f'{value[:4]} •••• •••• {value[-4:]}'

    def save(self, *args, **kwargs):
        if not self.display_id:
            self.display_id = _generate_display_id()
        if not self.referral_code:
            self.referral_code = _generate_referral_code()
        if not self.security_code:
            self.security_code = _generate_security_code()
        super().save(*args, **kwargs)

    #: Minimálny investovaný objem (€) na jednotlivé vernostné stupne pre investorov.
    class LoyaltyTier(models.TextChoices):
        BRONZE = 'bronze', 'Bronz'
        SILVER = 'silver', 'Striebro'
        GOLD = 'gold', 'Zlato'
        PLATINUM = 'platinum', 'Platina'

    LOYALTY_THRESHOLDS = (
        (Decimal('20000'), LoyaltyTier.PLATINUM),
        (Decimal('5000'), LoyaltyTier.GOLD),
        (Decimal('1000'), LoyaltyTier.SILVER),
        (Decimal('0'), LoyaltyTier.BRONZE),
    )

    @property
    def total_invested_lifetime(self) -> Decimal:
        """Súčet všetkých investícií (bez ohľadu na stav), použité na vernostný program."""
        from bids.models import Bid
        return Bid.objects.filter(lender=self).aggregate(
            total=models.Sum('amount'),
        )['total'] or Decimal('0')

    @property
    def loyalty_tier(self):
        """Vernostný stupeň investora podľa celkového investovaného objemu."""
        total = self.total_invested_lifetime
        for threshold, tier in self.LOYALTY_THRESHOLDS:
            if total >= threshold:
                return tier
        return self.LoyaltyTier.BRONZE

    @property
    def loyalty_tier_label(self):
        return self.LoyaltyTier(self.loyalty_tier).label

    @property
    def loyalty_next_threshold(self):
        """Suma, ktorú treba doinvestovať do ďalšieho vernostného stupňa (None na maxime)."""
        total = self.total_invested_lifetime
        ordered = sorted(self.LOYALTY_THRESHOLDS, key=lambda item: item[0])
        for threshold, tier in ordered:
            if total < threshold:
                return threshold - total
        return None

    @property
    def display_name(self):
        """Verejné zobrazenie používateľa - vždy len anonymné číslo #123456,
        nikdy reálne meno ani username. Použiť všade, kde jeden používateľ
        vidí informácie o inom používateľovi (napr. v zozname žiadostí,
        ponúk na sekundárnom trhu a pod.)."""
        return f'#{self.display_id}'

    def __str__(self):
        return self.username
