from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Sum
from django.shortcuts import get_object_or_404, redirect, render

from auctions.models import Auction
from bids.models import Bid

from .models import Notification


def landing(request):
    """Rozlišovacia domovská stránka - výber investor / dlžník."""
    return render(request, 'core/landing.html')


def landing_investor(request):
    open_auctions = Auction.objects.filter(status=Auction.Status.ACTIVE).count()
    context = {
        'open_auctions': open_auctions or 5,
    }
    return render(request, 'core/investor_landing.html', context)


#: Minimálny jednorazový aukčný poplatok platformy (€), bez ohľadu na sumu/dni.
MIN_AUCTION_FEE = 20


def _auction_fee(amount, days):
    """Aukčný poplatok sa mení podľa dĺžky splácania (20 % z istiny pri max.
    30-dňovej splatnosti, úmerne menej pri kratšej splatnosti), vždy však
    aspoň MIN_AUCTION_FEE €."""
    return max(round(amount * 0.20 * (days / 30), 2), MIN_AUCTION_FEE)


def landing_borrower(request):
    from users.forms import interest_rate_for_duration

    amount, days = 150, 15
    rate = interest_rate_for_duration(days) / Decimal('100')
    interest = round(amount * float(rate) * (days / 365), 2)
    fee = _auction_fee(amount, days)
    context = {
        'amount': amount, 'days': days, 'interest': interest, 'fee': fee,
        'total_to_repay': round(amount + interest, 2),
        'net_to_borrower': round(amount - fee, 2),
    }
    return render(request, 'core/borrower_landing.html', context)


#: Fakturačné/kontaktné údaje spoločnosti - zobrazené na stránke Kontakt a v pätičke.
COMPANY_DETAILS = {
    'name': 'Insight Partners s. r. o.',
    'address': 'Suché mýto 4769/2, 811 03 Bratislava - mestská časť Staré Mesto',
    'ico': '56609060',
    'dic': '2122361164',
    'email': 'info@insightpartners.sk',
    'phone': '+421 910 314 417',
    'contact_person': 'Juraj Šupina',
}


def contact(request):
    """Kontaktná stránka s fakturačnými a kontaktnými údajmi spoločnosti."""
    return render(request, 'core/contact.html', {'company': COMPANY_DETAILS})


def faq(request):
    """Stránka s často kladenými otázkami (pre investorov aj žiadateľov)."""
    return render(request, 'core/faq.html')


def terms(request):
    """Všeobecné obchodné podmienky."""
    return render(request, 'core/terms.html', {'company': COMPANY_DETAILS})


def privacy(request):
    """Zásady ochrany osobných údajov (GDPR)."""
    return render(request, 'core/privacy.html', {'company': COMPANY_DETAILS})


def public_stats(request):
    """Verejný štatistický prehľad platformy - buduje dôveru nových investorov
    (celkový objem, počet pôžičiek, priemerný výnos, miera defaultu)."""
    all_bids = Bid.objects.select_related('auction')
    total_invested = all_bids.aggregate(total=Sum('amount'))['total'] or Decimal('0')
    total_loans = Auction.objects.filter(status__in=[Auction.Status.FUNDED, Auction.Status.CLOSED]).count()
    closed_loans = Auction.objects.filter(status=Auction.Status.CLOSED)
    defaulted_loans = closed_loans.filter(bought_back=True).count()
    repaid_loans = closed_loans.exclude(bought_back=True).count()
    default_rate = round((defaulted_loans / closed_loans.count()) * 100, 1) if closed_loans.count() else 0

    avg_interest = all_bids.aggregate(avg=Avg('interest_rate'))['avg']

    context = {
        'total_invested': round(total_invested, 2),
        'total_loans': total_loans,
        'repaid_loans': repaid_loans,
        'defaulted_loans': defaulted_loans,
        'default_rate': default_rate,
        'avg_interest': round(avg_interest, 1) if avg_interest else Decimal('24.0'),
        'active_investors': Bid.objects.values('lender').distinct().count(),
    }
    return render(request, 'core/public_stats.html', context)


@login_required
def notifications_list(request):
    """Zoznam notifikácií prihláseného používateľa (zvonček v hlavičke) -
    šablóna sa líši podľa role prihláseného používateľa (investor/dlžník)."""
    from users.models import User
    notifications = Notification.objects.filter(user=request.user)
    template = (
        'core/notifications_borrower.html'
        if request.user.role == User.Role.BORROWER
        else 'core/notifications_investor.html'
    )
    return render(request, template, {'notifications': notifications})


@login_required
def notification_mark_read(request, pk):
    notif = get_object_or_404(Notification, pk=pk, user=request.user)
    notif.is_read = True
    notif.save(update_fields=['is_read'])
    return redirect(notif.url or 'core:notifications')


@login_required
def notifications_mark_all_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return redirect('core:notifications')
