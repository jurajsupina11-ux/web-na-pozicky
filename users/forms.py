from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
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


def validate_sk_iban(value):
    """Peniaze sa dajú posielať iba na slovenské bankové účty (SK IBAN)."""
    cleaned = (value or '').replace(' ', '').upper()
    if not cleaned.startswith('SK'):
        raise ValidationError('Peniaze je možné posielať iba na slovenský bankový účet (IBAN musí začínať SK).')
    if len(cleaned) != 24:
        raise ValidationError('Slovenský IBAN musí mať presne 24 znakov (napr. SK89 0900 0000 0000 0000 0000).')


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
    """Registrácia investora (veriteľa). Obsahuje aj KYC údaje (overenie identity)
    a IBAN pre výplatu peňazí - keďže investor posiela aj prijíma reálne peniaze,
    musíme vedieť, komu skutočne patrí účet (rovnako prísne ako u dlžníka).
    Dlžníci tento formulár nepoužívajú - žiadajú rovno o úver cez BorrowerApplicationForm.

    Obsahuje aj honeypot pole (website) proti jednoduchým registračným botom -
    skutoční používatelia ho nikdy nevyplnia, keďže je v UI skrytý."""

    # Honeypot - skryté pole, ktoré vypĺňajú len boty. Ak je vyplnené, žiadosť sa tíško zahodí.
    website = forms.CharField(label='Webstránka', required=False, widget=forms.TextInput(attrs={
        'autocomplete': 'off', 'tabindex': '-1', 'style': 'position:absolute;left:-9999px;',
    }))

    # Osobné / KYC údaje - rovnaký rozsah ako u dlžníka (meno osoby, ktorej skutočne
    # patria peniaze na účte).
    first_name = forms.CharField(label='Meno', max_length=150)
    last_name = forms.CharField(label='Priezvisko', max_length=150)
    date_of_birth = forms.DateField(
        label='Dátum narodenia', widget=forms.DateInput(attrs={'type': 'date'}),
    )
    id_card_number = forms.CharField(label='Číslo občianskeho preukazu', max_length=20)
    birth_number = forms.CharField(label='Rodné číslo (bez lomítka)', max_length=15)
    street_address = forms.CharField(label='Ulica a číslo', max_length=120)
    city = forms.CharField(label='Mesto', max_length=80)
    postal_code = forms.CharField(label='PSČ', max_length=10)
    bank_account_iban = forms.CharField(
        label='IBAN pre výplatu peňazí (voliteľné, dá sa doplniť aj neskôr)',
        max_length=34, required=False,
    )

    gdpr_consent = forms.BooleanField(
        label='Súhlasím so spracovaním osobných údajov (GDPR) a s obchodnými podmienkami.',
        required=True,
        error_messages={'required': 'Pre registráciu je potrebné udeliť súhlas so spracovaním osobných údajov.'},
    )

    field_order = [
        'website', 'username', 'email', 'phone_number',
        'first_name', 'last_name', 'date_of_birth', 'id_card_number', 'birth_number',
        'street_address', 'city', 'postal_code', 'bank_account_iban',
        'password1', 'password2', 'gdpr_consent',
    ]

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'phone_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _apply_autocomplete_and_classes(self)
        # Honeypot pole nemá dostať bootstrap/placeholder štýlovanie typické pre reálne polia.
        self.fields['website'].widget.attrs.pop('placeholder', None)
        self.fields['website'].widget.attrs['class'] = ''

    def clean_website(self):
        value = self.cleaned_data.get('website', '')
        if value:
            raise ValidationError('Registrácia sa nepodarila.')
        return value

    def clean_birth_number(self):
        value = normalize_birth_number(self.cleaned_data['birth_number'])
        if not value.isdigit() or len(value) not in (9, 10):
            raise ValidationError('Zadaj rodné číslo bez lomítka (9 alebo 10 číslic).')
        if User.objects.filter(birth_number=value).exists():
            raise ValidationError('S týmto rodným číslom je už evidovaný iný účet.')
        return value

    def clean_bank_account_iban(self):
        value = self.cleaned_data.get('bank_account_iban', '')
        if value:
            validate_sk_iban(value)
            return value.replace(' ', '').upper()
        return value

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.LENDER
        user.gdpr_consent_given = True
        user.gdpr_consent_at = timezone.now()
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.date_of_birth = self.cleaned_data['date_of_birth']
        user.id_card_number = self.cleaned_data['id_card_number']
        user.birth_number = self.cleaned_data['birth_number']
        user.street_address = self.cleaned_data['street_address']
        user.city = self.cleaned_data['city']
        user.postal_code = self.cleaned_data['postal_code']
        user.bank_account_iban = self.cleaned_data.get('bank_account_iban', '')
        user.kyc_completed = True
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

    def clean_bank_account_iban(self):
        value = self.cleaned_data['bank_account_iban']
        validate_sk_iban(value)
        return value.replace(' ', '').upper()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.kyc_completed = True
        if commit:
            user.save()
        return user


class BankAccountForm(forms.ModelForm):
    """Zmena bankového účtu (IBAN), na ktorý sa vyplácajú peniaze - pre
    investora aj dlžníka, dostupné v Nastaveniach účtu. Peniaze sa posielajú
    iba na slovenské bankové účty (SK IBAN). Zmena IBAN u investora vyžaduje
    zadanie bezpečnostného kódu, ktorý dostal e-mailom pri registrácii."""

    security_code = forms.CharField(
        label='Bezpečnostný kód (z e-mailu pri registrácii)',
        max_length=20, required=False,
    )

    class Meta:
        model = User
        fields = ('bank_account_iban',)
        labels = {'bank_account_iban': 'IBAN pre výplatu peňazí (len SK účty)'}

    def __init__(self, *args, **kwargs):
        self.user = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        _apply_autocomplete_and_classes(self)
        # Bezpečnostný kód sa vyžaduje len pre investorov (majú ho z registrácie);
        # dlžníci kód nedostávajú, ich IBAN sa overuje inak (osobné údaje pri KYC).
        if not self.user or self.user.role != User.Role.LENDER:
            self.fields.pop('security_code', None)

    def clean_bank_account_iban(self):
        value = self.cleaned_data['bank_account_iban']
        validate_sk_iban(value)
        return value.replace(' ', '').upper()

    def clean_security_code(self):
        code = self.cleaned_data.get('security_code', '').strip()
        if self.user and self.user.role == User.Role.LENDER:
            if not code or code != self.user.security_code:
                raise ValidationError('Nesprávny bezpečnostný kód.')
        return code


class SecurityCodePasswordChangeForm(PasswordChangeForm):
    """Zmena hesla vyžaduje zadanie bezpečnostného kódu (z e-mailu pri registrácii),
    rovnako ako žiadosť o výber peňazí a zmena IBAN - ochrana pred zneužitím účtu."""

    security_code = forms.CharField(
        label='Bezpečnostný kód (z e-mailu pri registrácii)',
        max_length=20,
    )

    field_order = ['old_password', 'new_password1', 'new_password2', 'security_code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _apply_autocomplete_and_classes(self)

    def clean_security_code(self):
        code = self.cleaned_data.get('security_code', '').strip()
        if not code or code != self.user.security_code:
            raise ValidationError('Nesprávny bezpečnostný kód.')
        return code


def normalize_birth_number(value):
    """Odstráni lomítko a medzery z rodného čísla (napr. '900101/1234' -> '9001011234')."""
    return (value or '').replace('/', '').replace(' ', '').strip()


class BorrowerApplicationForm(forms.Form):
    """Jediný formulár pre dlžníka: vytvorenie účtu + KYC údaje + parametre žiadosti
    o pôžičku. Dlžník si nevolí vlastné prihlasovacie údaje - používateľské meno je
    jeho rodné číslo (bez lomítka) a heslo sa vygeneruje automaticky a pošle e-mailom
    až po schválení žiadosti administrátorom (posúdenie registra dlžníkov/úverov)."""

    DEFAULT_INTEREST_RATE = 24.00

    # Prístupové údaje - bez voľby username/hesla, len kontakt.
    email = forms.EmailField(label='E-mail')
    phone_number = forms.CharField(label='Telefónne číslo', max_length=20)

    # Osobné / KYC údaje
    first_name = forms.CharField(label='Meno', max_length=150)
    last_name = forms.CharField(label='Priezvisko', max_length=150)
    date_of_birth = forms.DateField(
        label='Dátum narodenia', widget=forms.DateInput(attrs={'type': 'date'}),
    )
    id_card_number = forms.CharField(label='Číslo občianskeho preukazu', max_length=20)
    birth_number = forms.CharField(
        label='Rodné číslo (bez lomítka)', max_length=15,
        help_text='Slúži zároveň ako tvoje používateľské meno na prihlásenie.',
    )
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
    gdpr_consent = forms.BooleanField(
        label='Súhlasím so spracovaním osobných údajov (GDPR) a s obchodnými podmienkami.',
        required=True,
        error_messages={'required': 'Pre odoslanie žiadosti je potrebné udeliť súhlas so spracovaním osobných údajov.'},
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

    def clean_birth_number(self):
        value = normalize_birth_number(self.cleaned_data['birth_number'])
        if not value.isdigit() or len(value) not in (9, 10):
            raise ValidationError('Zadaj rodné číslo bez lomítka (9 alebo 10 číslic).')
        if User.objects.filter(username=value).exists():
            raise ValidationError('S týmto rodným číslom je už evidovaná žiadosť/účet.')
        return value

    def clean_bank_account_iban(self):
        value = self.cleaned_data['bank_account_iban']
        validate_sk_iban(value)
        return value.replace(' ', '').upper()

    def create_user(self):
        """Vytvorí účet dlžníka - username = rodné číslo, heslo sa vygeneruje
        náhodne a uloží sa do self.generated_password (treba ho poslať e-mailom
        až po schválení žiadosti, nie tu)."""
        from .models import _generate_password

        self.generated_password = _generate_password()
        user = User(
            username=self.cleaned_data['birth_number'],
            email=self.cleaned_data['email'],
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
            gdpr_consent_given=True,
            gdpr_consent_at=timezone.now(),
        )
        user.set_password(self.generated_password)
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
            status=Auction.Status.PENDING_REVIEW,
            ends_at=timezone.now() + timezone.timedelta(days=duration),
        )


class RepeatLoanApplicationForm(forms.Form):
    """Zjednodušený formulár na opakovanú žiadosť pre už overeného dlžníka
    (kyc_completed=True) - osobné údaje sa znova nevypĺňajú, stačia parametre
    novej pôžičky. Žiadosť znova ide k administrátorovi na posúdenie."""

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

    def create_auction(self, user):
        amount = self.cleaned_data['amount_requested']
        duration = self.cleaned_data['duration_days']
        return Auction.objects.create(
            borrower=user,
            title=f'Žiadosť o pôžičku {amount} € na {duration} dní',
            description=self.cleaned_data['purpose'],
            amount_requested=amount,
            max_interest_rate=BorrowerApplicationForm.DEFAULT_INTEREST_RATE,
            duration_days=duration,
            status=Auction.Status.PENDING_REVIEW,
            ends_at=timezone.now() + timezone.timedelta(days=duration),
        )

