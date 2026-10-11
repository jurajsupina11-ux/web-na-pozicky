from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'phone_number', 'role')


class KYCForm(forms.ModelForm):
    """Formulár s citlivými údajmi, vyplní sa pri žiadosti o prvú pôžičku."""

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'date_of_birth',
            'id_card_number', 'birth_number',
            'street_address', 'city', 'postal_code',
            'bank_account_iban',
        )
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'first_name': 'Meno',
            'last_name': 'Priezvisko',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.kyc_completed = True
        if commit:
            user.save()
        return user
