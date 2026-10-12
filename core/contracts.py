"""Generovanie PDF zmluvnej dokumentácie (Zmluva o pôžičke, Predpis k úhrade,
Potvrdenie o zániku dlhu, Oznámenie o postúpení pohľadávky, Zmluva o postúpení
pohľadávky) - štruktúra a princíp prevzaté z reálnych vzorov používaných v P2P
pôžičkovom sektore, upravené na naše obchodné údaje, úrokové sadzby a poplatky.

Všetky sumy/percentá/lehoty sa riadia skutočnými hodnotami použitými v appke
(24 % p.a. úrok, variabilný aukčný poplatok, 7-dňový odklad za 15 €, zmluvná
pokuta 8/16/24/32 % podľa dĺžky omeškania v intervaloch po 7 dňoch).
"""
import os
from decimal import Decimal

import reportlab
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

from core.views import _auction_fee

#: Údaje prevádzkovateľa platformy (zhodné s core.views.COMPANY_DETAILS).
COMPANY = {
    'name': 'Insight Partners s. r. o.',
    'address': 'Suché mýto 4769/2, 811 03 Bratislava - mestská časť Staré Mesto',
    'ico': '56609060',
    'dic': '2122361164',
    'email': 'info@insightpartners.sk',
    'web': 'www.pozickypredlznikov.sk',
    'phone': '',  # TODO: doplniť zákaznícku linku, ak bude zriadená
}

#: Bankové údaje, na ktoré dlžníci zasielajú splátky (zhodné s users.views.REPAYMENT_BANK_DETAILS).
REPAYMENT_BANK = {
    'bank_name': 'Fio banka, a.s., pobočka zahraničnej banky',
    'iban': 'SK89 8330 0000 0021 0167 2695',
    'swift': 'FIOZSKBA',
}

#: Úroková sadzba pôžičiek (% p.a.) - zhodná s BorrowerApplicationForm.DEFAULT_INTEREST_RATE.
LOAN_INTEREST_RATE = Decimal('24')

#: Jednorazový poplatok a dĺžka odkladu splátky (zhodné s users.views.POSTPONE_FEE/POSTPONE_DAYS).
POSTPONE_FEE = Decimal('15')
POSTPONE_DAYS = 7

#: Zmluvná pokuta pri omeškaní - % z istiny pôžičky podľa počtu dní omeškania
#: (rovnaký princíp intervalov ako je bežné v odvetví, upravené na náš 7-dňový krok).
PENALTY_TIERS = (
    (7, 13, Decimal('8')),
    (14, 20, Decimal('16')),
    (21, 27, Decimal('24')),
    (28, None, Decimal('32')),
)


def _register_fonts():
    """Zaregistruje font Vera (podpora slovenskej diakritiky) pre reportlab, ak ešte nie je."""
    font_path = os.path.join(os.path.dirname(reportlab.__file__), 'fonts', 'Vera.ttf')
    font_path_bold = os.path.join(os.path.dirname(reportlab.__file__), 'fonts', 'VeraBd.ttf')
    if 'Vera' not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont('Vera', font_path))
        pdfmetrics.registerFont(TTFont('Vera-Bold', font_path_bold))


def _styles():
    _register_fonts()
    styles = getSampleStyleSheet()
    styles['Title'].fontName = 'Vera-Bold'
    styles['Title'].fontSize = 15
    styles['Normal'].fontName = 'Vera'
    styles['Normal'].fontSize = 10
    styles['Normal'].leading = 14
    styles.add(ParagraphStyle(name='Heading', fontName='Vera-Bold', fontSize=11, spaceBefore=12, spaceAfter=6))
    styles.add(ParagraphStyle(name='Small', fontName='Vera', fontSize=8.5, textColor=colors.HexColor('#55607a')))
    return styles


def _penalty_percent(days_overdue):
    """Vráti kumulatívne % zmluvnej pokuty z istiny pre daný počet dní omeškania."""
    percent = Decimal('0')
    for lo, hi, tier_percent in PENALTY_TIERS:
        if days_overdue >= lo:
            percent = tier_percent
    return percent


def _pdf_response(filename):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


def generate_loan_agreement_pdf(loan, bid):
    """Zmluva o pôžičke medzi Dlžníkom a Veriteľom (investorom), sprostredkovaná
    platformou - rovnaká štruktúra ako reálne používané vzory v P2P sektore,
    upravená na naše % a poplatky."""
    styles = _styles()
    response = _pdf_response(f'Zmluva_o_pozicke_{loan.pk}.pdf')
    doc = SimpleDocTemplate(response, pagesize=A4, topMargin=18 * mm, bottomMargin=18 * mm,
                             leftMargin=20 * mm, rightMargin=20 * mm)

    borrower = loan.borrower
    lender = bid.lender
    amount = bid.amount
    interest = round(amount * (bid.interest_rate / Decimal('100')) * (Decimal(loan.duration_days) / Decimal('365')), 2)
    total_repay = amount + interest
    due_date = loan.computed_due_date
    auction_fee = Decimal(str(_auction_fee(float(amount), loan.duration_days)))

    el = [
        Paragraph(f'Zmluva o pôžičke č. {loan.pk}', styles['Title']),
        Paragraph('uzatvorená v súlade s § 657 a nasl. Občianskeho zákonníka', styles['Normal']),
        Paragraph('(ďalej len „Zmluva“)', styles['Normal']),
        Spacer(1, 6 * mm),
        Paragraph('medzi', styles['Normal']),
        Paragraph('<b>dlžníkom</b>', styles['Normal']),
        Paragraph(f'Užívateľské číslo dlžníka: {borrower.display_id}', styles['Normal']),
        Paragraph('(ďalej len „Dlžník“)', styles['Normal']),
        Paragraph('a', styles['Normal']),
        Paragraph('<b>investorom</b>', styles['Normal']),
        Paragraph(f'Užívateľské číslo investora: {lender.display_id}', styles['Normal']),
        Paragraph('(ďalej len „Veriteľ“)', styles['Normal']),
        Paragraph('zastúpený sprostredkovateľom:', styles['Normal']),
        Paragraph(
            f'Obchodné meno: {COMPANY["name"]}<br/>'
            f'Sídlo: {COMPANY["address"]}<br/>'
            f'IČO: {COMPANY["ico"]}, DIČ: {COMPANY["dic"]}',
            styles['Normal'],
        ),
        Paragraph('(ďalej len „Sprostredkovateľ“)', styles['Normal']),
        Paragraph('(Dlžník a Veriteľ ďalej spolu len „Zmluvné strany“)', styles['Normal']),
        Paragraph('v nasledujúcom znení:', styles['Normal']),

        Paragraph('Čl. I. Úvodné ustanovenia', styles['Heading']),
        Paragraph(
            f'1. Zmluvné strany zhodne vyhlasujú a súhlasia s tým, že k uzatvoreniu tejto Zmluvy dochádza '
            f'prostredníctvom internetového portálu {COMPANY["web"]} a v súlade s ustanoveniami Všeobecných '
            f'zmluvných podmienok Sprostredkovateľa (ďalej len „VZP“) po úspešnom vyfinancovaní žiadosti o pôžičku '
            f'investorom.', styles['Normal'],
        ),
        Paragraph(
            '2. Pojmy označované s veľkým začiatočným písmenom používané v tejto Zmluve sú používané s rovnakým '
            'významom aký majú vo VZP.', styles['Normal'],
        ),

        Paragraph('Čl. II. Predmet Zmluvy', styles['Heading']),
        Paragraph(
            f'1. Na základe tejto Zmluvy sa Veriteľ zaväzuje poskytnúť Dlžníkovi bezúčelovú pôžičku vo výške '
            f'{amount} EUR (ďalej len „Pôžička“), a to bezhotovostným prevodom na Dlžníkom určený bankový účet, '
            f'pričom Dlžník sa zaväzuje Pôžičku Veriteľovi vrátiť spolu s dohodnutým úrokom vo výške {bid.interest_rate} % '
            f'p.a., dohodnutým spôsobom a v dohodnutom Termíne splatnosti, a to v súlade s ustanoveniami tejto Zmluvy.',
            styles['Normal'],
        ),
    ]

    el.append(Paragraph('Čl. III. Podmienky poskytnutia a čerpania Pôžičky', styles['Heading']))
    el.append(Paragraph(
        '1. Veriteľa pri plnení záväzkov vyplývajúcich mu z tejto Zmluvy zastupuje Sprostredkovateľ ako '
        'splnomocnený zástupca. Sprostredkovateľ v mene Veriteľa poskytne Dlžníkovi Pôžičku formou '
        'bezhotovostného prevodu finančných prostriedkov na Dlžníkom určený účet. Dlžník je povinný vrátiť '
        'poskytnutú Pôžičku spolu s dohodnutým úrokom Veriteľovi na účet Sprostredkovateľa v súlade s Čl. IV. '
        'tejto Zmluvy.', styles['Normal'],
    ))
    el.append(Paragraph(
        f'2. Dlžník podpisom tejto Zmluvy potvrdzuje, že súhlasí s tým, aby mu bola Pôžička zo strany Veriteľa '
        f'poskytnutá prostredníctvom Sprostredkovateľa, a že si je vedomý, že z poskytnutej Pôžičky si '
        f'Sprostredkovateľ ponechá dohodnutý Aukčný poplatok vo výške {auction_fee} EUR a na Dlžníkom '
        f'určený účet poukáže sumu vo výške {amount - auction_fee} EUR.', styles['Normal'],
    ))
    el.append(Paragraph(
        '3. Za deň poskytnutia Pôžičky sa považuje deň pripísania finančných prostriedkov na Dlžníkom určený '
        'účet.', styles['Normal'],
    ))

    el.append(Paragraph('Čl. IV. Podmienky splatenia Pôžičky', styles['Heading']))
    el.append(Paragraph(
        f'1. Zmluvné strany sa dohodli, že dohodnutý úrok za poskytnutie Pôžičky je vo výške {interest} EUR '
        f'({bid.interest_rate} % p.a. prepočítaných na {loan.duration_days} dní splatnosti). Predčasné splatenie '
        f'Pôžičky nemá vplyv na výšku dohodnutého úroku.', styles['Normal'],
    ))
    el.append(Paragraph(
        f'2. Dlžník je Pôžičku spolu s dohodnutým úrokom, t.j. celkovú sumu vo výške {total_repay} EUR, povinný '
        f'vrátiť Veriteľovi najneskôr do {due_date.strftime("%d.%m.%Y")} (ďalej len „Termín splatnosti“).',
        styles['Normal'],
    ))
    el.append(Paragraph(
        f'3. Dlžník je povinný celkovú sumu uvedenú v bode 2. vyššie uhradiť bezhotovostným prevodom na účet '
        f'Sprostredkovateľa: {REPAYMENT_BANK["bank_name"]}, IBAN: {REPAYMENT_BANK["iban"]}. Pri úhrade je '
        f'Dlžník povinný uviesť variabilný symbol zhodný s číslom tejto Zmluvy ({loan.pk}).', styles['Normal'],
    ))
    el.append(Paragraph(
        '4. Za deň vrátenia Pôžičky sa považuje deň pripísania finančných prostriedkov v celej dlžnej sume na '
        'účet Sprostredkovateľa.', styles['Normal'],
    ))

    el.append(Paragraph('Čl. V. Porušenie Zmluvy zo strany Dlžníka', styles['Heading']))
    el.append(Paragraph(
        '1. Zmluvné strany sa dohodli, že ak Dlžník aj bez svojho zavinenia nesplní záväzok vyplývajúci mu z '
        'tejto Zmluvy voči Veriteľovi, t.j. riadne a včas neuhradí Pôžičku spolu s dohodnutým úrokom, zaväzuje '
        'sa za porušenie svojej povinnosti zaplatiť Veriteľovi zmluvnú pokutu vo výške uvedenej v bode 2. nižšie.',
        styles['Normal'],
    ))
    el.append(Paragraph(
        '2. Zmluvná pokuta je vo výške: 8 % z istiny Pôžičky, ak je Dlžník v omeškaní 7 až 13 dní; 16 % z '
        'istiny Pôžičky, ak je Dlžník v omeškaní 14 až 20 dní; 24 % z istiny Pôžičky, ak je Dlžník v omeškaní '
        '21 až 27 dní; 32 % z istiny Pôžičky, ak je Dlžník v omeškaní viac ako 28 dní, pričom ide vždy o '
        'celkovú (nie priebežne sa sčítavajúcu) sumu zmluvnej pokuty pre daný interval omeškania.',
        styles['Normal'],
    ))
    el.append(Paragraph(
        '3. Zmluvná pokuta je splatná momentom jej uplatnenia zo strany Veriteľa, ktorý o vzniku tohto nároku '
        'a jeho výške notifikuje Dlžníka prostredníctvom Sprostredkovateľa v jeho účte na platforme.',
        styles['Normal'],
    ))
    el.append(Paragraph(
        '4. Zaplatením zmluvnej pokuty nie je dotknutý nárok Veriteľa požadovať od Dlžníka aj náhradu škody, '
        'ako aj úroky z omeškania v zákonom stanovenej výške.', styles['Normal'],
    ))
    el.append(Paragraph(
        '5. V prípade omeškania Dlžníka je Veriteľ oprávnený svoje pohľadávky voči Dlžníkovi vymáhať cestou '
        'mimosúdneho alebo súdneho vymáhania, vrátane úhrady nákladov spojených s vymáhaním pohľadávky.',
        styles['Normal'],
    ))

    el.append(Paragraph('Čl. VI. Predĺženie Termínu splatnosti Pôžičky (odklad splátky)', styles['Heading']))
    el.append(Paragraph(
        f'1. Dlžník môže požiadať o predĺženie Termínu splatnosti Pôžičky o {POSTPONE_DAYS} kalendárnych dní, '
        f'a to opakovane, vždy za jednorazový poplatok vo výške {POSTPONE_FEE} EUR, ktorý je splatný súčasne s '
        f'podaním žiadosti o odklad. Úhradou poplatku je odklad splatnosti automaticky potvrdený.',
        styles['Normal'],
    ))

    el.append(Paragraph('Čl. VII. Garancia odkúpenia pohľadávky', styles['Heading']))
    el.append(Paragraph(
        '1. Veriteľ berie na vedomie a súhlasí s tým, že v prípade, ak Dlžník nesplní svoj záväzok z tejto '
        'Zmluvy ani do 90 dní po Termíne splatnosti, Sprostredkovateľ automaticky odkúpi pohľadávku Veriteľa '
        'voči Dlžníkovi za sumu rovnajúcu sa istine Pôžičky a dohodnutému úroku, a to pripísaním tejto sumy na '
        'virtuálny účet (peňaženku) Veriteľa. Ďalšie vymáhanie pohľadávky voči Dlžníkovi preberá na seba '
        'Sprostredkovateľ.', styles['Normal'],
    ))

    el.append(Paragraph('Čl. VIII. Trvanie a zánik Zmluvy, postúpenie pohľadávky', styles['Heading']))
    el.append(Paragraph(
        '1. Táto Zmluva sa uzatvára na dobu určitú, a to do konečného vysporiadania záväzkov oboch Zmluvných '
        'strán vyplývajúcich im z tejto Zmluvy.', styles['Normal'],
    ))
    el.append(Paragraph(
        '2. Veriteľ je oprávnený v súlade s § 524 ods. 1 Občianskeho zákonníka aj bez súhlasu Dlžníka postúpiť '
        'pohľadávky, a to aj nesplatné, vzniknuté mu voči Dlžníkovi z tejto Zmluvy na tretiu osobu (napr. inému '
        'investorovi prostredníctvom sekundárneho trhu platformy).', styles['Normal'],
    ))

    el.append(Paragraph('Čl. IX. Záverečné ustanovenia', styles['Heading']))
    el.append(Paragraph(
        '1. Táto Zmluva je vyhotovená v elektronickej podobe v záväznom znení v podobe zápisu na trvanlivom '
        'médiu. Zmluva nadobúda platnosť dňom jej uzatvorenia oboma Zmluvnými stranami a účinnosť dňom '
        'poskytnutia Pôžičky.', styles['Normal'],
    ))
    el.append(Paragraph(
        '2. Táto Zmluva a všetky vzťahy z nej vyplývajúce sa riadia príslušnými ustanoveniami právneho poriadku '
        'Slovenskej republiky, najmä Občianskeho zákonníka a ustanoveniami VZP.', styles['Normal'],
    ))
    el.append(Paragraph(
        '3. Zmluvné strany deklarujú svoju vôľu riešiť každý spor, ktorý vznikne z tejto Zmluvy, prednostne '
        'rokovaním a dohodou. Ak vzniknutý spor nebude možné urovnať dohodou, spor bude riešený na '
        'všeobecných súdoch v Slovenskej republike.', styles['Normal'],
    ))
    el.append(Paragraph(
        '4. Uzatvorením tejto Zmluvy Dlžník vyhlasuje, že túto Zmluvu uzatvára na vlastnú žiadosť, že si Zmluvu '
        'prečítal, jej obsahu porozumel a súhlasí s ním, a že nebola dojednaná pod nátlakom, v tiesni alebo za '
        'inak nápadne nevýhodných podmienok.', styles['Normal'],
    ))
    el.append(Spacer(1, 10 * mm))
    el.append(Paragraph(f'V Bratislave dňa {loan.created_at.strftime("%d.%m.%Y")}', styles['Normal']))
    el.append(Spacer(1, 6 * mm))

    sig_table = Table(
        [['Veriteľ', 'Dlžník'],
         [f'Investor č. {lender.display_id}', f'Dlžník č. {borrower.display_id}'],
         [f'zastúpený na základe plnej moci\n{COMPANY["name"]}', '']],
        colWidths=[80 * mm, 80 * mm],
    )
    sig_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Vera'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    el.append(sig_table)
    el.append(Spacer(1, 10 * mm))
    el.append(Paragraph(
        f'{COMPANY["name"]}, {COMPANY["address"]}, IČO: {COMPANY["ico"]}, {COMPANY["email"]}, {COMPANY["web"]}',
        styles['Small'],
    ))

    doc.build(el)
    return response


def generate_payment_notice_pdf(loan, bid):
    """Predpis k úhrade - doklad so sumou, variabilným symbolom a bankovými
    údajmi na splatenie pôžičky."""
    styles = _styles()
    response = _pdf_response(f'Predpis_k_uhrade_{loan.pk}.pdf')
    doc = SimpleDocTemplate(response, pagesize=A4, topMargin=18 * mm, bottomMargin=18 * mm,
                             leftMargin=20 * mm, rightMargin=20 * mm)

    interest = round(bid.amount * (bid.interest_rate / Decimal('100')) * (Decimal(loan.duration_days) / Decimal('365')), 2)
    total = bid.amount + interest

    el = [
        Paragraph(f'Predpis k úhrade č. {loan.pk}', styles['Title']),
        Paragraph(f'Dlžník č. {loan.borrower.display_id}', styles['Normal']),
        Spacer(1, 8 * mm),
        Paragraph('Údaje potrebné na úhradu', styles['Heading']),
        Paragraph(f'Variabilný symbol: {loan.pk}', styles['Normal']),
        Paragraph(
            'Uvedenie správneho variabilného symbolu je nevyhnutné pre korektné priradenie Vašej platby.',
            styles['Small'],
        ),
        Paragraph(f'Dátum vystavenia: {loan.created_at.strftime("%d.%m.%Y")}', styles['Normal']),
        Paragraph(f'Dátum splatnosti: {loan.computed_due_date.strftime("%d.%m.%Y")}', styles['Normal']),
        Spacer(1, 6 * mm),
        Paragraph(f'<b>Celková čiastka k úhrade: {total} EUR</b>', styles['Normal']),
        Spacer(1, 4 * mm),
        Paragraph('Bankové spojenie:', styles['Heading']),
        Paragraph(f'{REPAYMENT_BANK["bank_name"]}<br/>IBAN: {REPAYMENT_BANK["iban"]}<br/>'
                  f'SWIFT/BIC: {REPAYMENT_BANK["swift"]}', styles['Normal']),
        Spacer(1, 6 * mm),
        Paragraph(
            'K vykonaniu úhrady použite hore uvedený variabilný symbol potrebný k priradeniu platby. Neúplný '
            'alebo nesprávny variabilný symbol môže zapríčiniť nezaúčtovanie úhrady k Vašej poskytnutej pôžičke. '
            'V prípade, ak zistíte, že ste použili nesprávny variabilný symbol, bezodkladne nás prosím '
            'kontaktujte.', styles['Normal'],
        ),
        Spacer(1, 10 * mm),
        Paragraph(
            f'{COMPANY["email"]} · {COMPANY["web"]}<br/>{COMPANY["name"]}, {COMPANY["address"]}, '
            f'IČO: {COMPANY["ico"]}', styles['Small'],
        ),
    ]
    doc.build(el)
    return response


def generate_assignment_notice_pdf(bid):
    """Oznámenie o postúpení pohľadávky dlžníkovi - vystavuje ho pôvodný
    investor po predaji investície na sekundárnom trhu."""
    styles = _styles()
    loan = bid.auction
    seller = bid.previous_lender
    buyer = bid.lender
    response = _pdf_response(f'Oznamenie_o_postupeni_pohladavky_{loan.pk}.pdf')
    doc = SimpleDocTemplate(response, pagesize=A4, topMargin=18 * mm, bottomMargin=18 * mm,
                             leftMargin=20 * mm, rightMargin=20 * mm)

    interest = round(bid.amount * (bid.interest_rate / Decimal('100')) * (Decimal(loan.duration_days) / Decimal('365')), 2)
    transfer_date = (bid.transferred_at or loan.updated_at).strftime('%d.%m.%Y')

    el = [
        Paragraph('Oznámenie o postúpení pohľadávky', styles['Title']),
        Spacer(1, 6 * mm),
        Paragraph(f'Vážený dlžník - užívateľské číslo dlžníka {loan.borrower.display_id}', styles['Normal']),
        Paragraph(
            f'Touto cestou Vám oznamujeme, že investor č. {seller.display_id if seller else "-"} ako postupca '
            f'uzatvoril so spoločnosťou {COMPANY["name"]}, so sídlom {COMPANY["address"]}, IČO: {COMPANY["ico"]}, '
            f'ako sprostredkovateľom, dňa {transfer_date} Zmluvu o postúpení pohľadávky č. {bid.pk}, predmetom '
            f'ktorej bolo postúpenie jeho peňažnej pohľadávky voči Vám vzniknutej na základe Zmluvy o pôžičke '
            f'č. {loan.pk} zo dňa {loan.created_at.strftime("%d.%m.%Y")}, ktorá pozostáva z:',
            styles['Normal'],
        ),
        Paragraph(f'i) neuhradenej istiny pôžičky vo výške {bid.amount} EUR, splatnej dňa '
                  f'{loan.computed_due_date.strftime("%d.%m.%Y")};', styles['Normal']),
        Paragraph(f'ii) neuhradeného úroku vo výške {interest} EUR, splatného dňa '
                  f'{loan.computed_due_date.strftime("%d.%m.%Y")}.', styles['Normal']),
        Spacer(1, 6 * mm),
        Paragraph(
            f'Na základe uvedeného Vás žiadame, aby ste Váš záväzok uhradili na nasledujúci účet spoločnosti '
            f'{COMPANY["name"]}: {REPAYMENT_BANK["bank_name"]}, IBAN: {REPAYMENT_BANK["iban"]}, pri úhrade '
            f'uveďte variabilný symbol zhodný s číslom pôžičky ({loan.pk}).', styles['Normal'],
        ),
        Spacer(1, 10 * mm),
        Paragraph(f'V Bratislave, dňa {transfer_date}', styles['Normal']),
        Paragraph(f'Investor - užívateľské číslo investora {buyer.display_id}', styles['Normal']),
    ]
    doc.build(el)
    return response


def generate_assignment_agreement_pdf(bid):
    """Zmluva o postúpení pohľadávky medzi pôvodným investorom (postupca) a
    novým investorom (postupník) na sekundárnom trhu."""
    styles = _styles()
    loan = bid.auction
    seller = bid.previous_lender
    buyer = bid.lender
    response = _pdf_response(f'Zmluva_o_postupeni_pohladavky_{bid.pk}.pdf')
    doc = SimpleDocTemplate(response, pagesize=A4, topMargin=18 * mm, bottomMargin=18 * mm,
                             leftMargin=20 * mm, rightMargin=20 * mm)

    interest = round(bid.amount * (bid.interest_rate / Decimal('100')) * (Decimal(loan.duration_days) / Decimal('365')), 2)
    transfer_date = (bid.transferred_at or loan.updated_at).strftime('%d.%m.%Y')
    seller_id = seller.display_id if seller else '-'

    el = [
        Paragraph(f'Zmluva o postúpení pohľadávky č. {bid.pk}', styles['Title']),
        Paragraph('uzatvorená v súlade s § 524 a nasl. Občianskeho zákonníka v znení neskorších predpisov',
                   styles['Normal']),
        Paragraph('(ďalej len „Zmluva“)', styles['Normal']),
        Spacer(1, 6 * mm),
        Paragraph('medzi', styles['Normal']),
        Paragraph('<b>postupcom</b>', styles['Normal']),
        Paragraph(f'Užívateľské číslo investora: {seller_id}', styles['Normal']),
        Paragraph('(ďalej len „Postupca“)', styles['Normal']),
        Paragraph('a', styles['Normal']),
        Paragraph('<b>postupníkom</b>', styles['Normal']),
        Paragraph(f'Užívateľské číslo investora: {buyer.display_id}', styles['Normal']),
        Paragraph('(ďalej len „Postupník“)', styles['Normal']),
        Paragraph(
            f'obaja zastúpení sprostredkovateľom {COMPANY["name"]}, {COMPANY["address"]}, '
            f'IČO: {COMPANY["ico"]} (ďalej len „Sprostredkovateľ“)', styles['Normal'],
        ),
        Paragraph('(Postupca a Postupník ďalej spolu aj ako „Zmluvné strany“)', styles['Normal']),
        Paragraph('v nasledujúcom znení:', styles['Normal']),
    ]
    el.append(Paragraph('Čl. I. Úvodné ustanovenia', styles['Heading']))
    el.append(Paragraph(
        f'1. Zmluvné strany sú používateľmi služieb Sprostredkovateľa na internetovom portáli {COMPANY["web"]}, '
        f'na ktorom Sprostredkovateľ prevádzkuje aukčný systém krátkodobých pôžičiek a sekundárny trh investícií '
        f'medzi investormi.', styles['Normal'],
    ))

    el.append(Paragraph('Čl. II. Predmet Zmluvy', styles['Heading']))
    el.append(Paragraph(
        '1. Na základe tejto Zmluvy Postupca postupuje v prospech Postupníka svoju pohľadávku bližšie '
        'špecifikovanú v bode 2. tejto Zmluvy, vrátane jej príslušenstva a všetkých práv s ňou spojených.',
        styles['Normal'],
    ))
    el.append(Paragraph(
        f'2. Postupca má voči dlžníkovi - užívateľské číslo dlžníka {loan.borrower.display_id} (ďalej len '
        f'„Dlžník“) peňažnú pohľadávku vzniknutú na základe Zmluvy o pôžičke č. {loan.pk} uzatvorenej dňa '
        f'{loan.created_at.strftime("%d.%m.%Y")} medzi Postupcom ako veriteľom a Dlžníkom, ktorá pozostáva z:',
        styles['Normal'],
    ))
    el.append(Paragraph(f'i) neuhradenej istiny pôžičky vo výške {bid.amount} EUR, splatnej dňa '
                         f'{loan.computed_due_date.strftime("%d.%m.%Y")};', styles['Normal']))
    el.append(Paragraph(f'ii) neuhradeného úroku vo výške {interest} EUR, splatného dňa '
                         f'{loan.computed_due_date.strftime("%d.%m.%Y")}', styles['Normal']))
    el.append(Paragraph('(ďalej spolu len „Pohľadávka“).', styles['Normal']))
    el.append(Paragraph(
        '3. Postupník dňom účinnosti tejto Zmluvy vstupuje do všetkých práv Postupcu týkajúcich sa Pohľadávky, '
        'hlavných i akcesorických, vrátane nároku na prípadnú zmluvnú pokutu a práv z dohody o zrážkach zo mzdy '
        'a z iných príjmov dojednanej v Zmluve o pôžičke.', styles['Normal'],
    ))

    el.append(Paragraph('Čl. III. Odplata za postúpenie a platobné podmienky', styles['Heading']))
    el.append(Paragraph(
        f'1. Postupca postupuje Postupníkovi Pohľadávku odplatne, t.j. za odplatu vo výške {bid.amount} EUR '
        f'(ďalej len „Odplata“). Odplata je splatná v deň uzatvorenia tejto Zmluvy.', styles['Normal'],
    ))
    el.append(Paragraph(
        '2. Zmluvné strany potvrdzujú, že úhrada Odplaty bola zrealizovaná prostredníctvom Sprostredkovateľa '
        'odpísaním sumy Odplaty z peňaženky Postupníka a jej pripísaním na peňaženku Postupcu, bezodkladne po '
        'uzatvorení tejto Zmluvy.', styles['Normal'],
    ))

    el.append(Paragraph('Čl. IV. Vyhlásenia Postupcu', styles['Heading']))
    el.append(Paragraph(
        '1. Postupca vyhlasuje, že postúpenie Pohľadávky neodporuje dohode s Dlžníkom, Pohľadávka je spôsobilá '
        'na postúpenie, je reálna a nie je premlčaná, záväzok Dlžníka ku dňu uzatvorenia tejto Zmluvy nezanikol, '
        'je oprávnený neobmedzene disponovať s postupovanou Pohľadávkou, k Pohľadávke nie sú zriadené práva '
        'tretích osôb a nemá vedomosť o žiadnych započítateľných pohľadávkach, ktoré by voči nemu Dlžník mohol '
        'mať.', styles['Normal'],
    ))

    el.append(Paragraph('Čl. V. Záverečné ustanovenia', styles['Heading']))
    el.append(Paragraph(
        '1. Táto Zmluva je vyhotovená v elektronickej podobe v záväznom znení v podobe zápisu na trvanlivom '
        'médiu a uzatvára sa na diaľku prostredníctvom prostriedkov diaľkovej komunikácie prostredníctvom '
        'Sprostredkovateľa.', styles['Normal'],
    ))
    el.append(Paragraph('2. Zmluva nadobúda platnosť a účinnosť dňom jej uzatvorenia oboma Zmluvnými stranami.',
                         styles['Normal']))
    el.append(Paragraph(
        '3. Táto Zmluva a všetky vzťahy z nej vyplývajúce sa riadia príslušnými ustanoveniami právneho poriadku '
        'Slovenskej republiky, najmä Občianskeho zákonníka.', styles['Normal'],
    ))
    el.append(Spacer(1, 10 * mm))
    el.append(Paragraph(f'V Bratislave, dňa {transfer_date}', styles['Normal']))
    el.append(Spacer(1, 6 * mm))

    sig_table = Table(
        [['Postupca', 'Postupník'],
         [f'Investor č. {seller_id}', f'Investor č. {buyer.display_id}'],
         [f'zastúpený na základe plnej moci\n{COMPANY["name"]}',
          f'zastúpený na základe plnej moci\n{COMPANY["name"]}']],
        colWidths=[80 * mm, 80 * mm],
    )
    sig_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Vera'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    el.append(sig_table)

    doc.build(el)
    return response


def generate_debt_discharge_certificate_pdf(loan, bid):
    """Potvrdenie o zániku dlhu - vystavené po úplnom splatení pôžičky."""
    styles = _styles()
    response = _pdf_response(f'Potvrdenie_o_zaniku_dlhu_{loan.pk}.pdf')
    doc = SimpleDocTemplate(response, pagesize=A4, topMargin=18 * mm, bottomMargin=18 * mm,
                             leftMargin=20 * mm, rightMargin=20 * mm)

    el = [
        Paragraph('Potvrdenie o zániku dlhu', styles['Title']),
        Spacer(1, 6 * mm),
        Paragraph(
            f'Obchodné meno: {COMPANY["name"]}<br/>Sídlo: {COMPANY["address"]}<br/>'
            f'IČO: {COMPANY["ico"]}', styles['Normal'],
        ),
        Paragraph('(ďalej len „Poskytovateľ“)', styles['Normal']),
        Spacer(1, 4 * mm),
        Paragraph(f'Dlžník<br/>Užívateľské číslo dlžníka: {loan.borrower.display_id}', styles['Normal']),
        Paragraph('(ďalej len „Dlžník“)', styles['Normal']),
        Spacer(1, 6 * mm),
        Paragraph(
            f'Veriteľ týmto potvrdzuje, že ku dňu vystavenia tohto potvrdenia došlo k úhrade všetkých záväzkov '
            f'Dlžníka voči Veriteľovi zo Zmluvy o pôžičke č. {loan.pk}.', styles['Normal'],
        ),
        Paragraph(
            f'Pohľadávka, vrátane príslušenstva z titulu Zmluvy o pôžičke č. {loan.pk}, zanikla splnením a ku '
            f'dňu vystavenia tohto potvrdenia sa považuje za vysporiadanú v celom rozsahu.', styles['Normal'],
        ),
        Spacer(1, 10 * mm),
        Paragraph('V Bratislave', styles['Normal']),
        Spacer(1, 10 * mm),
        Paragraph(
            f'{COMPANY["name"]}<br/>{COMPANY["address"]}<br/>IČO: {COMPANY["ico"]}<br/>'
            f'E-mail: {COMPANY["email"]}<br/>{COMPANY["web"]}', styles['Normal'],
        ),
    ]
    doc.build(el)
    return response
