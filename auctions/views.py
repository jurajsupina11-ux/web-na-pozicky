from datetime import datetime, time
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView

from bids.forms import BidForm
from bids.models import Bid
from core.emails import send_investment_confirmation, send_loan_approved
from core.models import Notification, notify

from .models import Auction
from .forms import AuctionForm

#: Jednorazový bonus (€) pre pozývateľa aj pozvaného po prvej investícii pozvaného.
REFERRAL_BONUS = Decimal('10')


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
    """Financovanie žiadosti o pôžičku - vždy len celá naraz (all-or-nothing).
    Jedna pôžička = jeden investor = jedna investícia za podmienok žiadosti
    (celá požadovaná suma, úrok podľa max_interest_rate aukcie)."""
    auction = get_object_or_404(Auction, pk=pk, status=Auction.Status.ACTIVE)
    if request.method == 'POST':
        amount = auction.amount_requested
        if amount > request.user.wallet_balance:
            messages.error(
                request,
                'Na peňaženke nemáš dostatok voľných prostriedkov na financovanie celej tejto pôžičky. '
                'Pôžičky sa financujú vždy celé naraz, nie je možné investovať len časť.',
            )
            return redirect(auction.get_absolute_url())

        bid = Bid.objects.create(
            auction=auction,
            lender=request.user,
            amount=amount,
            interest_rate=auction.max_interest_rate,
        )

        # Suma investície sa strháva z peňaženky investora hneď pri financovaní.
        request.user.wallet_balance -= amount
        request.user.save(update_fields=['wallet_balance'])
        send_investment_confirmation(request.user, bid)

        # Pôžička je vyfinancovaná celá naraz - okamžite sa schváli.
        auction.status = Auction.Status.FUNDED
        auction.save(update_fields=['status'])
        send_loan_approved(auction.borrower, auction)
        messages.success(request, 'Pôžička bola vyfinancovaná celá a bola schválená.')

        # Referral program - ak je toto prvá investícia pozvaného používateľa,
        # pripíše sa jednorazový bonus (€) pozvanému aj jeho pozývateľovi.
        referrer = request.user.referred_by
        if referrer and not request.user.referral_reward_granted:
            is_first_investment = Bid.objects.filter(lender=request.user).count() == 1
            if is_first_investment:
                request.user.wallet_balance += REFERRAL_BONUS
                request.user.referral_reward_granted = True
                request.user.save(update_fields=['wallet_balance', 'referral_reward_granted'])
                referrer.wallet_balance += REFERRAL_BONUS
                referrer.save(update_fields=['wallet_balance'])
                notify(
                    request.user,
                    f'Odmena za registráciu na pozvanie: +{REFERRAL_BONUS} €',
                    'Vďaka za prvú investíciu - bonus bol pripísaný na tvoju peňaženku.',
                    kind=Notification.Kind.SUCCESS,
                )
                notify(
                    referrer,
                    f'Odmena za odporúčanie: +{REFERRAL_BONUS} €',
                    'Tvoj pozvaný priateľ práve urobil prvú investíciu - bonus bol pripísaný na tvoju peňaženku.',
                    kind=Notification.Kind.SUCCESS,
                )
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


def _parse_history_dates(request):
    """Spoločné parsovanie dátumov 'od'/'do' z GET parametrov pre históriu
    investícií aj PDF export - vracia (date_from, date_to, bids_queryset)."""
    date_from_str = request.GET.get('od', '')
    date_to_str = request.GET.get('do', '')
    qs = Bid.objects.filter(lender=request.user).select_related('auction').order_by('-created_at')

    date_from = None
    date_to = None
    if date_from_str:
        try:
            date_from = datetime.strptime(date_from_str, '%Y-%m-%d').date()
            qs = qs.filter(created_at__gte=timezone.make_aware(datetime.combine(date_from, time.min)))
        except ValueError:
            date_from = None
    if date_to_str:
        try:
            date_to = datetime.strptime(date_to_str, '%Y-%m-%d').date()
            qs = qs.filter(created_at__lte=timezone.make_aware(datetime.combine(date_to, time.max)))
        except ValueError:
            date_to = None
    return date_from_str, date_to_str, qs


@login_required
def investor_history(request):
    """História investícií investora s filtrom podľa obdobia (od-do) a
    možnosťou exportu do PDF pre potreby účtovníctva."""
    date_from_str, date_to_str, bids = _parse_history_dates(request)
    total_amount = sum((b.amount for b in bids), Decimal('0'))
    return render(request, 'auctions/investor_history.html', {
        'bids': bids,
        'date_from': date_from_str,
        'date_to': date_to_str,
        'total_amount': total_amount,
    })


@login_required
def investor_history_pdf(request):
    """Export histórie investícií za zvolené obdobie do PDF (napr. pre účtovníctvo)."""
    import os

    import reportlab
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet

    # Bitstream Vera obsahuje diakritiku (á, č, š...) na rozdiel od vstavaných
    # PDF fontov (Helvetica), ktoré ju nepodporujú.
    font_path = os.path.join(os.path.dirname(reportlab.__file__), 'fonts', 'Vera.ttf')
    font_path_bold = os.path.join(os.path.dirname(reportlab.__file__), 'fonts', 'VeraBd.ttf')
    if 'Vera' not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont('Vera', font_path))
        pdfmetrics.registerFont(TTFont('Vera-Bold', font_path_bold))

    date_from_str, date_to_str, bids = _parse_history_dates(request)

    response = HttpResponse(content_type='application/pdf')
    filename = f'investicie_{date_from_str or "od"}_{date_to_str or "do"}.pdf'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    doc = SimpleDocTemplate(response, pagesize=A4, topMargin=18 * mm, bottomMargin=18 * mm)
    styles = getSampleStyleSheet()
    styles['Title'].fontName = 'Vera-Bold'
    styles['Normal'].fontName = 'Vera'
    elements = [
        Paragraph('Pôžičky Predlžníkov – história investícií', styles['Title']),
        Paragraph(
            f'Obdobie: {date_from_str or "od začiatku"} – {date_to_str or "dnes"}',
            styles['Normal'],
        ),
        Paragraph(f'Investor: {request.user.display_name} ({request.user.username})', styles['Normal']),
        Spacer(1, 10 * mm),
    ]

    data = [['Dátum', 'Žiadateľ', 'Suma (€)', 'Úrok (% p.a.)', 'Splatnosť (dní)', 'Stav']]
    total = Decimal('0')
    for b in bids:
        data.append([
            b.created_at.strftime('%d.%m.%Y'),
            b.auction.borrower.display_name,
            f'{b.amount}',
            f'{b.interest_rate}',
            f'{b.auction.duration_days}',
            b.auction.get_status_display(),
        ])
        total += b.amount
    data.append(['', '', f'{total}', '', '', 'Spolu'])

    table = Table(data, colWidths=[25 * mm, 30 * mm, 25 * mm, 28 * mm, 28 * mm, 28 * mm])
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Vera'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2554ea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Vera-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dbe4f5')),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#eaf0ff')),
        ('FONTNAME', (0, -1), (-1, -1), 'Vera-Bold'),
    ]))
    elements.append(table)
    doc.build(elements)
    return response


def _tax_statement_data(user, year):
    """Vráti (bids_in_year, total_interest) pre daňový výkaz investora za daný rok.
    Zarátavajú sa len úrokové príjmy zo splatených (CLOSED) pôžičiek, ktorých
    splatnosť pripadla na daný rok - to je príjem, ktorý sa reálne realizoval."""
    bids = Bid.objects.filter(
        lender=user,
        auction__status=Auction.Status.CLOSED,
    ).select_related('auction')
    bids_in_year = [b for b in bids if b.auction.computed_due_date.year == year]
    for b in bids_in_year:
        b.interest_amount = round(
            b.amount * (b.interest_rate / Decimal('100')) * (Decimal(b.auction.duration_days) / Decimal('365')),
            2,
        )
    total_interest = sum((b.interest_amount for b in bids_in_year), Decimal('0'))
    return bids_in_year, round(total_interest, 2)


@login_required
def tax_statement(request):
    """Ročný súhrnný výkaz úrokových príjmov investora - podklad pre daňové
    priznanie (príjem z poskytnutia peňažných prostriedkov, § 7 zákona o dani
    z príjmov)."""
    current_year = timezone.now().year
    available_years = sorted({
        b.auction.computed_due_date.year
        for b in Bid.objects.filter(lender=request.user, auction__status=Auction.Status.CLOSED).select_related('auction')
    }, reverse=True) or [current_year]
    selected_year = int(request.GET.get('rok', available_years[0]))
    bids_in_year, total_interest = _tax_statement_data(request.user, selected_year)

    return render(request, 'auctions/tax_statement.html', {
        'available_years': available_years,
        'selected_year': selected_year,
        'bids_in_year': bids_in_year,
        'total_interest': total_interest,
    })


@login_required
def tax_statement_pdf(request, year):
    """Export ročného daňového výkazu úrokových príjmov do PDF."""
    import os

    import reportlab
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet

    font_path = os.path.join(os.path.dirname(reportlab.__file__), 'fonts', 'Vera.ttf')
    font_path_bold = os.path.join(os.path.dirname(reportlab.__file__), 'fonts', 'VeraBd.ttf')
    if 'Vera' not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont('Vera', font_path))
        pdfmetrics.registerFont(TTFont('Vera-Bold', font_path_bold))

    bids_in_year, total_interest = _tax_statement_data(request.user, year)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="danovy_vykaz_{year}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4, topMargin=18 * mm, bottomMargin=18 * mm)
    styles = getSampleStyleSheet()
    styles['Title'].fontName = 'Vera-Bold'
    styles['Normal'].fontName = 'Vera'
    elements = [
        Paragraph(f'Pôžičky Predlžníkov – ročný daňový výkaz {year}', styles['Title']),
        Paragraph(f'Investor: {request.user.display_name} ({request.user.username})', styles['Normal']),
        Paragraph(
            'Súhrn úrokových príjmov zo splatených pôžičiek za daný rok - podklad pre daňové priznanie '
            '(príjem z poskytnutia peňažných prostriedkov).',
            styles['Normal'],
        ),
        Spacer(1, 10 * mm),
    ]

    data = [['Pôžička', 'Dátum splatnosti', 'Istina (€)', 'Úrok (% p.a.)', 'Realizovaný úrok (€)']]
    for b in bids_in_year:
        data.append([
            f'#{b.auction.pk}',
            b.auction.computed_due_date.strftime('%d.%m.%Y'),
            f'{b.amount}',
            f'{b.interest_rate}',
            f'{b.interest_amount}',
        ])
    data.append(['', '', '', 'Spolu', f'{total_interest} €'])

    table = Table(data, colWidths=[22 * mm, 32 * mm, 28 * mm, 30 * mm, 40 * mm])
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Vera'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2554ea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Vera-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dbe4f5')),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#eaf0ff')),
        ('FONTNAME', (0, -1), (-1, -1), 'Vera-Bold'),
    ]))
    elements.append(table)
    doc.build(elements)
    return response


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

