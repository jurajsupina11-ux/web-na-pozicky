from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import KYCForm, SignUpForm


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('auctions:list')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class CustomLoginView(LoginView):
    template_name = 'users/login.html'


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('auctions:list')


@login_required
def kyc_form(request):
    """Citlivé údaje (OP, rodné číslo, adresa) vyplnené pri žiadosti o prvú pôžičku."""
    next_url = request.GET.get('next') or reverse_lazy('auctions:create')
    if request.user.kyc_completed:
        return redirect(next_url)
    if request.method == 'POST':
        form = KYCForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Údaje boli overené. Môžeš pokračovať v žiadosti o pôžičku.')
            return redirect(next_url)
    else:
        form = KYCForm(instance=request.user)
    return render(request, 'users/kyc_form.html', {'form': form, 'next_url': next_url})

