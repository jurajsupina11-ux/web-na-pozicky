from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from bids.forms import BidForm
from bids.models import Bid

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

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.kyc_completed:
            return redirect(f"{reverse_lazy('users:kyc')}?next={request.path}")
        return super().dispatch(request, *args, **kwargs)

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
            # Keď je žiadosť plne vyfinancovaná, pôžička sa automaticky schváli -
            # dlžník sa odblokuje do prostredia pre dlžníkov (Moje pôžičky).
            if auction.funding_progress >= 100:
                auction.status = Auction.Status.FUNDED
                auction.save(update_fields=['status'])
                messages.success(request, 'Žiadosť bola plne vyfinancovaná a pôžička bola schválená.')
        else:
            messages.error(request, 'Ponuku sa nepodarilo odoslať, skontrolujte údaje.')
    return redirect(auction.get_absolute_url())


@login_required
def investor_dashboard(request):
    """Prostredie pre investora - prehľad portfólia (čo investor dal) a miesto,
    kde môže získať ďalšie pôžičky (otvorené aktívne žiadosti)."""
    my_bids = Bid.objects.filter(lender=request.user).select_related('auction')
    total_invested = sum((b.amount for b in my_bids), Decimal('0'))
    active_bids = my_bids.filter(auction__status=Auction.Status.ACTIVE)
    funded_bids = my_bids.filter(auction__status__in=[Auction.Status.FUNDED, Auction.Status.CLOSED])
    expected_yield = sum(
        (b.amount * (b.interest_rate / Decimal('100')) * (b.auction.duration_days / Decimal('365')) for b in funded_bids),
        Decimal('0'),
    )
    open_auctions = Auction.objects.filter(status=Auction.Status.ACTIVE).exclude(
        bids__lender=request.user,
    ).distinct()
    context = {
        'my_bids': my_bids,
        'active_bids': active_bids,
        'funded_bids': funded_bids,
        'total_invested': total_invested,
        'active_count': active_bids.count(),
        'expected_yield': round(expected_yield, 2),
        'open_auctions': open_auctions,
    }
    return render(request, 'auctions/investor_dashboard.html', context)

