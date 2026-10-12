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


#: Minimálny jednorazový aukčný poplatok platformy (€), bez ohľadu na sumu/dni.
MIN_AUCTION_FEE = 20


def _auction_fee(amount, days):
    """Aukčný poplatok sa mení podľa dĺžky splácania (20 % z istiny pri max.
    30-dňovej splatnosti, úmerne menej pri kratšej splatnosti), vždy však
    aspoň MIN_AUCTION_FEE €."""
    return max(round(amount * 0.20 * (days / 30), 2), MIN_AUCTION_FEE)


def landing_borrower(request):
    amount, days = 150, 14
    interest = round(amount * 0.24 * (days / 365), 2)
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
