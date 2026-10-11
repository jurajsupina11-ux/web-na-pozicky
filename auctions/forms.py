from django import forms
from django.utils import timezone

from .models import Auction


class AuctionForm(forms.ModelForm):
    duration_days = forms.IntegerField(min_value=1, max_value=365, label='Splatnosť (dni)')

    class Meta:
        model = Auction
        fields = [
            'title', 'description', 'amount_requested',
            'max_interest_rate', 'duration_days', 'ends_at',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'ends_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_ends_at(self):
        ends_at = self.cleaned_data['ends_at']
        if ends_at <= timezone.now():
            raise forms.ValidationError('Koniec aukcie musí byť v budúcnosti.')
        return ends_at
