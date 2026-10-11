from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils import timezone

from auctions.models import Auction

from .models import User


#: mapovanie meno poľa -> HTML autocomplete hodnota, aby prehliadač (vrátane
#: automatického doplnenia údajov z prihláseného Google účtu v Chrome) mohol
#: formuláre vyplniť automaticky.
AUTOCOMPLETE_MAP = {
    'username': 'username',
    'email': 'email',
    'phone_number': 'tel',
    'password1': 'new-password',
    'password2': 'new-password',
    'first_name': 'given-name',
    'last_name': 'family-name',
    'date_of_birth': 'bday',
    'id_card_number': 'off',
    'birth_number': 'off',
    'street_address': 'street-address',
    'city': 'address-level2',
    'postal_code': 'postal-code',
    'bank_account_iban': 'off',
    'amount_requested': 'off',
    'duration_days': 'off',
    'purpose': 'off',
}


def _apply_autocomplete_and_classes(form):
    """Pridá Bootstrap triedy a autocomplete atribúty na všetky polia formulára,
    aby sa dali pekne naštýlovať a aby prehliadač (Google účet v Chrome) mohol
    údaje doplniť automaticky."""
    for name, field in form.fields.items():
        css_class = 'form-check-input' if isinstance(field.widget, forms.CheckboxInput) else 'form-control'
        existing = field.widget.attrs.get('class', '')
        field.widget.attrs['class'] = f'{existing} {css_class}'.strip()
        autocomplete = AUTOCOMPLETE_MAP.get(name)
        if autocomplete:
            field.widget.attrs['autocomplete'] = autocomplete
        field.widget.attrs.setdefault('placeholder', field.label)


class SignUpForm(UserCreationForm):
    """Registrácia investora (veriteľa). Dlžníci tento formulár nepoužívajú -
    žiadajú rovno o úver cez BorrowerApplicationForm."""

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'phone_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _apply_autocomplete_and_classes(self)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.LENDER
        if commit:
            user.save()
        return user


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _apply_autocomplete_and_classes(self)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.kyc_completed = True
        if commit:
            user.save()
        return user


class BankAccountForm(forms.ModelForm):
    """Zmena bankového účtu (IBAN), na ktorý sa vyplácajú peniaze - pre
    investora aj dlžníka, dostupné v Nastaveniach účtu."""

    class Meta:
        model = User
        fields = ('bank_account_iban',)
        labels = {'bank_account_iban': 'IBAN pre výplatu peňazí'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _apply_autocomplete_and_classes(self)


class BorrowerApplicationForm(forms.Form):
    """Jediný formulár pre dlžníka: vytvorenie účtu + KYC údaje + parametre žiadosti
    o pôžičku. Dlžník sa takto nikdy neregistruje klasicky - rovno žiada o úver."""

    DEFAULT_INTEREST_RATE = 24.00

    # Prístupové údaje
    username = forms.CharField(label='Používateľské meno', max_length=150)
    email = forms.EmailField(label='E-mail', required=False)
    password1 = forms.CharField(label='Heslo', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Heslo (znova)', widget=forms.PasswordInput)
    phone_number = forms.CharField(label='Telefónne číslo', max_length=20)

    # Osobné / KYC údaje
    first_name = forms.CharField(label='Meno', max_length=150)
    last_name = forms.CharField(label='Priezvisko', max_length=150)
    date_of_birth = forms.DateField(
        label='Dátum narodenia', widget=forms.DateInput(attrs={'type': 'date'}),
    )
    id_card_number = forms.CharField(label='Číslo občianskeho preukazu', max_length=20)
    birth_number = forms.CharField(label='Rodné číslo', max_length=15)
    street_address = forms.CharField(label='Ulica a číslo', max_length=120)
    city = forms.CharField(label='Mesto', max_length=80)
    postal_code = forms.CharField(label='PSČ', max_length=10)
    bank_account_iban = forms.CharField(label='IBAN pre výplatu pôžičky', max_length=34)

    # Parametre žiadosti o pôžičku
    amount_requested = forms.DecimalField(
        label='Požadovaná suma (€)', min_value=50, max_value=500,
        max_digits=10, decimal_places=2,
    )
    duration_days = forms.IntegerField(label='Splatnosť (dni)', min_value=1, max_value=30)
    purpose = forms.CharField(
        label='Účel pôžičky', widget=forms.Textarea(attrs={'rows': 3}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _apply_autocomplete_and_classes(self)
        self.fields['amount_requested'].widget.attrs.update({
            'placeholder': 'napr. 200', 'min': 50, 'max': 500, 'step': 10,
        })
        self.fields['duration_days'].widget.attrs.update({
            'placeholder': 'napr. 14', 'min': 1, 'max': 30,
        })

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError('Toto používateľské meno je už obsadené.')
        return username

    def clean(self):
        cleaned = super().clean()
        p1, p2 = cleaned.get('password1'), cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', 'Heslá sa nezhodujú.')
        return cleaned

    def create_user(self):
        user = User(
            username=self.cleaned_data['username'],
            email=self.cleaned_data.get('email', ''),
            phone_number=self.cleaned_data['phone_number'],
            role=User.Role.BORROWER,
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            date_of_birth=self.cleaned_data['date_of_birth'],
            id_card_number=self.cleaned_data['id_card_number'],
            birth_number=self.cleaned_data['birth_number'],
            street_address=self.cleaned_data['street_address'],
            city=self.cleaned_data['city'],
            postal_code=self.cleaned_data['postal_code'],
            bank_account_iban=self.cleaned_data['bank_account_iban'],
            kyc_completed=True,
        )
        user.set_password(self.cleaned_data['password1'])
        user.save()
        return user

    def create_auction(self, user):
        amount = self.cleaned_data['amount_requested']
        duration = self.cleaned_data['duration_days']
        return Auction.objects.create(
            borrower=user,
            title=f'Žiadosť o pôžičku {amount} € na {duration} dní',
            description=self.cleaned_data['purpose'],
            amount_requested=amount,
            max_interest_rate=self.DEFAULT_INTEREST_RATE,
            duration_days=duration,
            status=Auction.Status.ACTIVE,
            ends_at=timezone.now() + timezone.timedelta(days=duration),
        )

