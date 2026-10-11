from django.shortcuts import render

from auctions.models import Auction


def landing(request):
    """Rozlišovacia domovská stránka - výber investor / dlžník."""
    return render(request, 'core/landing.html')


def landing_investor(request):
    open_auctions = Auction.objects.filter(status=Auction.Status.ACTIVE).count()
    context = {
        'open_auctions': open_auctions or 5,
    }
    return render(request, 'core/investor_landing.html', context)


def landing_borrower(request):
    amount, days = 150, 14
    interest = round(amount * 0.24 * (days / 365), 2)
    fee = round(amount * 0.20, 2)
    context = {
        'amount': amount, 'days': days, 'interest': interest, 'fee': fee,
        'total_to_repay': round(amount + interest, 2),
        'net_to_borrower': round(amount - fee, 2),
    }
    return render(request, 'core/borrower_landing.html', context)
