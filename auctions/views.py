from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from bids.forms import BidForm
from bids.models import Bid
from core.emails import send_investment_confirmation, send_loan_approved

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
            amount = form.cleaned_data['amount']
            if amount > request.user.wallet_balance:
                messages.error(
                    request,
                    'Na peňaženke nemáš dostatok voľných prostriedkov na túto investíciu. Najprv vlož peniaze na účet.',
                )
                return redirect(auction.get_absolute_url())

            bid = form.save(commit=False)
            bid.auction = auction
            bid.lender = request.user
            bid.save()

            # Suma investície sa strháva z peňaženky investora hneď pri odoslaní ponuky.
            request.user.wallet_balance -= amount
            request.user.save(update_fields=['wallet_balance'])
            send_investment_confirmation(request.user, bid)

            messages.success(request, 'Vaša ponuka bola odoslaná.')
            # Keď je žiadosť plne vyfinancovaná, pôžička sa automaticky schváli -
            # dlžník sa odblokuje do prostredia pre dlžníkov (Moje pôžičky).
            if auction.funding_progress >= 100:
                auction.status = Auction.Status.FUNDED
                auction.save(update_fields=['status'])
                send_loan_approved(auction.borrower, auction)
                messages.success(request, 'Žiadosť bola plne vyfinancovaná a pôžička bola schválená.')
        else:
            messages.error(request, 'Ponuku sa nepodarilo odoslať, skontrolujte údaje.')
    return redirect(auction.get_absolute_url())


@login_required
def investor_dashboard(request):
    """Prostredie pre investora - stav účtu, prehľad portfólia, štatistiky
    a prístup k ďalším funkciám (vyplatenie, predaj pôžičky, nové príležitosti)."""
    my_bids = Bid.objects.filter(lender=request.user).select_related('auction')
    total_invested = sum((b.amount for b in my_bids), Decimal('0'))
    active_bids = my_bids.filter(auction__status=Auction.Status.ACTIVE)
    funded_bids = my_bids.filter(auction__status=Auction.Status.FUNDED)
    closed_bids = my_bids.filter(auction__status=Auction.Status.CLOSED)
    expected_yield = sum(
        (b.amount * (b.interest_rate / Decimal('100')) * (b.auction.duration_days / Decimal('365')) for b in funded_bids),
        Decimal('0'),
    )
    realized_yield = sum(
        (b.amount * (b.interest_rate / Decimal('100')) * (b.auction.duration_days / Decimal('365')) for b in closed_bids),
        Decimal('0'),
    )
    for_sale_count = my_bids.filter(for_sale=True).count()
    context = {
        'my_bids': my_bids,
        'active_bids': active_bids,
        'funded_bids': funded_bids,
        'closed_bids': closed_bids,
        'wallet_balance': request.user.wallet_balance,
        'total_invested': total_invested,
        'active_count': funded_bids.count(),
        'expected_yield': round(expected_yield, 2),
        'realized_yield': round(realized_yield, 2),
        'for_sale_count': for_sale_count,
        'bids_count': my_bids.count(),
    }
    return render(request, 'auctions/investor_dashboard.html', context)


@login_required
def open_auctions_view(request):
    """'Čakáreň' - zoznam otvorených žiadostí o pôžičku, do ktorých investor
    ešte nefinancoval. Zobrazí sa po kliknutí na 'Získať nové pôžičky'."""
    open_auctions = Auction.objects.filter(status=Auction.Status.ACTIVE).exclude(
        bids__lender=request.user,
    ).distinct()
    return render(request, 'auctions/open_auctions.html', {'open_auctions': open_auctions})


@login_required
def wallet_deposit(request):
    """Simulovaný vklad peňazí na investorskú peňaženku."""
    if request.method == 'POST':
        try:
            amount = Decimal(request.POST.get('amount', '0'))
        except Exception:
            amount = Decimal('0')
        if amount > 0:
            request.user.wallet_balance += amount
            request.user.save(update_fields=['wallet_balance'])
            messages.success(request, f'Na účet bolo pripísaných {amount} €.')
        else:
            messages.error(request, 'Zadaj platnú sumu na vklad.')
    return redirect('auctions:investor_dashboard')


@login_required
def wallet_withdraw(request):
    """Simulovaná výplata peňazí z investorskej peňaženky na bankový účet."""
    if request.method == 'POST':
        try:
            amount = Decimal(request.POST.get('amount', '0'))
        except Exception:
            amount = Decimal('0')
        if amount <= 0:
            messages.error(request, 'Zadaj platnú sumu na výplatu.')
        elif amount > request.user.wallet_balance:
            messages.error(request, 'Na účte nemáš dostatok voľných prostriedkov.')
        else:
            request.user.wallet_balance -= amount
            request.user.save(update_fields=['wallet_balance'])
            messages.success(request, f'Žiadosť o výplatu {amount} € bola odoslaná na tvoj bankový účet.')
    return redirect('auctions:investor_dashboard')


@login_required
def bid_toggle_sale(request, bid_id):
    """Investor ponúkne (alebo stiahne z ponuky) svoj podiel na aktívnej pôžičke
    na sekundárnom trhu, aby ho mohol odkúpiť iný investor. Zrušiť ponuku na
    predaj je možné len do 5 minút od jej vytvorenia."""
    from django.utils import timezone

    bid = get_object_or_404(Bid, pk=bid_id, lender=request.user)
    if bid.auction.status != Auction.Status.FUNDED:
        messages.error(request, 'Na predaj je možné ponúknuť len aktívnu (vyfinancovanú) pôžičku.')
    elif bid.for_sale:
        if not bid.can_cancel_sale:
            messages.error(
                request,
                'Čas na zastavenie predaja (5 minút) už uplynul, investícia zostáva v ponuke.',
            )
        else:
            bid.for_sale = False
            bid.for_sale_since = None
            bid.save(update_fields=['for_sale', 'for_sale_since'])
            messages.info(request, 'Investícia bola stiahnutá z predaja.')
    else:
        bid.for_sale = True
        bid.for_sale_since = timezone.now()
        bid.save(update_fields=['for_sale', 'for_sale_since'])
        messages.success(
            request,
            'Tvoja investícia bola ponúknutá na sekundárnom trhu. Na zastavenie predaja máš 5 minút.',
        )
    return redirect('auctions:investor_dashboard')


@login_required
def marketplace(request):
    """Sekundárny trh - investor môže odkúpiť podiely na pôžičkách od iných investorov."""
    listings = Bid.objects.filter(for_sale=True).exclude(lender=request.user).select_related('auction', 'lender')
    return render(request, 'auctions/marketplace.html', {'listings': listings})


@login_required
def marketplace_buy(request, bid_id):
    """Kúpa podielu na pôžičke od iného investora - jednoduchý prevod vlastníctva
    danej investície (Bid) za jej nominálnu hodnotu, hradené z peňaženky kupujúceho."""
    listing = get_object_or_404(Bid, pk=bid_id, for_sale=True)
    if listing.lender_id == request.user.pk:
        messages.error(request, 'Nemôžeš odkúpiť vlastnú investíciu.')
        return redirect('auctions:marketplace')
    if request.user.wallet_balance < listing.amount:
        messages.error(request, 'Na účte nemáš dostatok voľných prostriedkov na odkúpenie tejto investície.')
        return redirect('auctions:marketplace')

    seller = listing.lender
    request.user.wallet_balance -= listing.amount
    request.user.save(update_fields=['wallet_balance'])
    seller.wallet_balance += listing.amount
    seller.save(update_fields=['wallet_balance'])

    listing.lender = request.user
    listing.for_sale = False
    listing.save(update_fields=['lender', 'for_sale'])

    messages.success(request, f'Investícia {listing.amount} € bola prevedená na tvoj účet.')
    return redirect('auctions:investor_dashboard')

