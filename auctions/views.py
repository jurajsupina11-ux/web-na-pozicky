from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from bids.forms import BidForm

from .models import Auction
from .forms import AuctionForm


class AuctionListView(ListView):
    model = Auction
    template_name = 'auctions/auction_list.html'
    context_object_name = 'auctions'
    paginate_by = 20

    def get_queryset(self):
        return Auction.objects.filter(status=Auction.Status.ACTIVE)


class AuctionDetailView(DetailView):
    model = Auction
    template_name = 'auctions/auction_detail.html'
    context_object_name = 'auction'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bid_form'] = BidForm()
        context['bids'] = self.object.bids.select_related('lender')
        return context


class AuctionCreateView(LoginRequiredMixin, CreateView):
    model = Auction
    form_class = AuctionForm
    template_name = 'auctions/auction_form.html'

    def form_valid(self, form):
        form.instance.borrower = self.request.user
        form.instance.status = Auction.Status.ACTIVE
        messages.success(self.request, 'Aukcia bola vytvorená.')
        return super().form_valid(form)


@login_required
def place_bid(request, pk):
    auction = get_object_or_404(Auction, pk=pk, status=Auction.Status.ACTIVE)
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.auction = auction
            bid.lender = request.user
            bid.save()
            messages.success(request, 'Vaša ponuka bola odoslaná.')
        else:
            messages.error(request, 'Ponuku sa nepodarilo odoslať, skontrolujte údaje.')
    return redirect(auction.get_absolute_url())

