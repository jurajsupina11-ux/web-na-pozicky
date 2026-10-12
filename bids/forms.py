from django import forms

from .models import Bid


class BidForm(forms.ModelForm):
    """Pôžičky sa financujú vždy len celé naraz (all-or-nothing) - investor
    nezadáva sumu ani úrok, len potvrdí financovanie za podmienok žiadosti
    (celá suma, úrok podľa max_interest_rate aukcie). Formulár tu zostáva len
    kvôli CSRF/potvrdzovaciemu tlačidlu, reálne hodnoty dopĺňa view."""

    class Meta:
        model = Bid
        fields = []
