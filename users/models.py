from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model so we can extend it later (KYC, phone, role...)."""

    class Role(models.TextChoices):
        BORROWER = 'borrower', 'Žiadateľ o pôžičku'
        LENDER = 'lender', 'Veriteľ'
        BOTH = 'both', 'Žiadateľ aj veriteľ'

    phone_number = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.BOTH)
    is_verified = models.BooleanField(
        default=False,
        help_text='Overená identita (KYC) - potrebné pred vytvorením aukcie alebo ponuky.',
    )
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username
