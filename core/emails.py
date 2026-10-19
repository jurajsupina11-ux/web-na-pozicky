"""Centrálne e-mailové notifikácie pre dlžníkov aj investorov.

Všetky funkcie sú "fail-safe" - ak odoslanie e-mailu zlyhá (napr. chýbajúce
SMTP údaje, výpadok siete), appka to len zaloguje a pokračuje ďalej, nikdy
nezhodí používateľovu akciu (žiadosť, investíciu a pod.).
"""
import logging

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def _send(subject, message, to_email):
    if not to_email:
        return
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [to_email],
            fail_silently=False,
        )
    except Exception:
        logger.exception('Nepodarilo sa odoslať e-mail "%s" na adresu %s', subject, to_email)


def send_investor_welcome(user):
    """Investorovi: po úspešnej registrácii mu pošleme bezpečnostný kód,
    ktorý bude potrebovať na potvrdenie žiadosti o výber peňazí a na zmenu
    bankového účtu (IBAN) v Nastaveniach."""
    _send(
        'Vitajte na Pôžičky pre Dlžníkov - Váš bezpečnostný kód',
        (
            f'Dobrý deň,\n\n'
            f'vitajte medzi investormi na Pôžičky pre Dlžníkov!\n\n'
            f'Váš bezpečnostný kód je: {user.security_code}\n\n'
            f'Tento kód budete potrebovať vždy, keď:\n'
            f'- požiadate o výber peňazí z peňaženky na svoj bankový účet,\n'
            f'- budete meniť bankový účet (IBAN), na ktorý sa Vám majú peniaze posielať,\n'
            f'- budete meniť heslo k účtu.\n\n'
            f'Kód si uložte na bezpečné miesto a nikomu ho neposkytujte.\n\n'
            f'Peniaze posielame výhradne na slovenské bankové účty (SK IBAN) a platby spracúvame '
            f'v pracovné dni od 8:00 do 16:00.\n\n'
            f'S pozdravom,\nPôžičky pre Dlžníkov'
        ),
        user.email,
    )


def send_loan_application_received(user, auction, password=None):
    """Dlžníkovi: potvrdenie prijatia žiadosti o pôžičku - žiadosť najprv
    posudzuje administrátor (register dlžníkov/úverov), o výsledku príde
    samostatný e-mail (schválenie, zamietnutie, alebo protiponuka). Ak ide
    o prvú žiadosť (nový účet), priloží sa aj používateľské meno (rodné
    číslo) a vygenerované heslo, aby sa dlžník mohol kedykoľvek prihlásiť
    a sledovať stav žiadosti."""
    credentials = ''
    if password:
        credentials = (
            f'Vaše prihlasovacie údaje:\n'
            f'Používateľské meno: {user.username}\n'
            f'Heslo: {password}\n\n'
            f'Heslo si po prvom prihlásení odporúčame zmeniť (v sekcii Nastavenia).\n\n'
        )
    _send(
        'Žiadosť o pôžičku bola prijatá - čaká sa na posúdenie',
        (
            f'Dobrý deň,\n\n'
            f'vaša žiadosť o pôžičku {auction.amount_requested} € na {auction.duration_days} dní '
            f'bola úspešne prijatá.\n\n'
            f'{credentials}'
            f'Žiadosť teraz posudzujeme (vrátane overenia v úverovom registri) - môže to trvať '
            f'niekoľko minút až hodín. Hneď ako bude vybavená, dostanete e-mail s výsledkom '
            f'(schválenie, prípadne dôvod zamietnutia alebo protiponuka). Do schválenia nemáte '
            f'prístup do prostredia pre dlžníkov, len na stránku so stavom žiadosti.\n\n'
            f'S pozdravom,\nPôžičky pre Dlžníkov'
        ),
        user.email,
    )


def send_loan_application_approved(user, auction):
    """Dlžníkovi: žiadosť bola administrátorom schválená - žiadosť ide medzi
    otvorené ponuky pre investorov. Spolu so schválením posielame aj
    bezpečnostný kód, ktorý bude dlžník potrebovať pri zmene bankového účtu
    (IBAN) v Nastaveniach."""
    _send(
        'Vaša žiadosť o pôžičku bola schválená',
        (
            f'Dobrý deň,\n\n'
            f'vaša žiadosť o pôžičku {auction.amount_requested} € na {auction.duration_days} dní '
            f'bola schválená a je teraz zobrazená investorom na financovanie.\n\n'
            f'Hneď ako ju niektorý investor financuje, dostanete ďalší e-mail a budete môcť podpísať '
            f'zmluvu vo svojom účte.\n\n'
            f'Váš bezpečnostný kód je: {user.security_code}\n'
            f'Tento kód budete potrebovať pri zmene bankového účtu (IBAN), na ktorý sa Vám majú '
            f'vyplácať peniaze. Kód si uložte na bezpečné miesto a nikomu ho neposkytujte.\n\n'
            f'S pozdravom,\nPôžičky pre Dlžníkov'
        ),
        user.email,
    )


def send_loan_application_rejected(user, auction):
    """Dlžníkovi: žiadosť bola zamietnutá (napr. na základe úverového registra)."""
    reason = f'\n\nDôvod: {auction.rejection_reason}\n' if auction.rejection_reason else '\n'
    _send(
        'Vaša žiadosť o pôžičku bola zamietnutá',
        (
            f'Dobrý deň,\n\n'
            f'bohužiaľ, Vašu žiadosť o pôžičku {auction.amount_requested} € sme nemohli schváliť.'
            f'{reason}\n'
            f'Žiadosť môžete kedykoľvek podať znova.\n\n'
            f'S pozdravom,\nPôžičky pre Dlžníkov'
        ),
        user.email,
    )


def send_loan_application_counter_offer(user, auction):
    """Dlžníkovi: namiesto zamietnutia platforma ponúka nižšiu sumu, dlžník ju
    môže prijať alebo odmietnuť vo svojom účte."""
    _send(
        'Protiponuka k Vašej žiadosti o pôžičku',
        (
            f'Dobrý deň,\n\n'
            f'pôvodne požadovanú sumu {auction.amount_requested} € sme nemohli schváliť v plnej výške, '
            f'namiesto toho Vám ponúkame pôžičku vo výške {auction.counter_offer_amount} €.\n\n'
            f'Protiponuku môžete prijať alebo odmietnuť vo svojom účte (sekcia "Moje žiadosti").\n\n'
            f'S pozdravom,\nPôžičky pre Dlžníkov'
        ),
        user.email,
    )


def send_loan_approved(user, auction):
    """Dlžníkovi: žiadosť bola plne vyfinancovaná (predschválená/schválená)."""
    _send(
        'Vaša pôžička bola schválená!',
        (
            f'Dobrý deň,\n\n'
            f'skvelá správa - vaša žiadosť o pôžičku {auction.amount_requested} € bola plne '
            f'vyfinancovaná. Peniaze budú čoskoro odoslané na váš bankový účet.\n\n'
            f'Prihláste sa do svojho účtu a v sekcii "Moje pôžičky" nájdete všetky informácie '
            f'o splácaní.\n\n'
            f'S pozdravom,\nPôžičky pre Dlžníkov'
        ),
        user.email,
    )


def send_email_verification(user, verify_url):
    """Dlžníkovi: odkaz na overenie e-mailovej adresy - vyžaduje sa pred
    podpisom Zmluvy o pôžičke."""
    _send(
        'Overte svoju e-mailovú adresu',
        (
            f'Dobrý deň,\n\n'
            f'pred podpisom Zmluvy o pôžičke je potrebné overiť Vašu e-mailovú adresu. '
            f'Kliknite prosím na nasledujúci odkaz:\n\n'
            f'{verify_url}\n\n'
            f'S pozdravom,\nPôžičky pre Dlžníkov'
        ),
        user.email,
    )


def send_investment_confirmation(user, bid):
    """Investorovi: potvrdenie, že jeho investícia (ponuka) bola úspešne zaznamenaná."""
    _send(
        'Potvrdenie investície',
        (
            f'Dobrý deň,\n\n'
            f'potvrdzujeme prijatie vašej investície {bid.amount} € s úrokom {bid.interest_rate} % p.a. '
            f'do pôžičky #{bid.auction.pk}.\n\n'
            f'Stav investície môžete sledovať vo svojom Dashboarde investora.\n\n'
            f'S pozdravom,\nPôžičky pre Dlžníkov'
        ),
        user.email,
    )


def send_repayment_reported(user, auction):
    """Investorovi: dlžník nahlásil úhradu, čaká sa na overenie platby."""
    _send(
        'Dlžník nahlásil úhradu pôžičky',
        (
            f'Dobrý deň,\n\n'
            f'dlžník nahlásil úhradu pôžičky #{auction.pk} ({auction.amount_requested} €). '
            f'Platba sa momentálne overuje, o výsledku vás budeme informovať.\n\n'
            f'S pozdravom,\nPôžičky pre Dlžníkov'
        ),
        user.email,
    )


def send_payment_overdue_reminder(user, auction):
    """Dlžníkovi: upozornenie, že splatnosť pôžičky je prekročená."""
    _send(
        'Upozornenie: Vaša pôžička je po splatnosti',
        (
            f'Dobrý deň,\n\n'
            f'vaša pôžička #{auction.pk} ({auction.amount_requested} €) je po termíne splatnosti. '
            f'Prosíme, uhraďte dlžnú sumu čo najskôr, prípadne požiadajte o odklad splátky vo '
            f'svojom účte (sekcia "Moje pôžičky").\n\n'
            f'S pozdravom,\nPôžičky pre Dlžníkov'
        ),
        user.email,
    )


def send_buyback_notice_lender(user, auction):
    """Investorovi: pôžička bola automaticky odkúpená platformou (garancia odkúpenia)."""
    _send(
        'Pôžička bola automaticky odkúpená - garancia odkúpenia',
        (
            f'Dobrý deň,\n\n'
            f'pôžička #{auction.pk} ({auction.amount_requested} €) nebola splatená do 90 dní po splatnosti. '
            f'V súlade s garanciou odkúpenia sme vašu investíciu (istina + dohodnutý úrok) automaticky '
            f'vyplatili na vašu peňaženku. Ďalšie vymáhanie dlhu od dlžníka preberá platforma.\n\n'
            f'S pozdravom,\nPôžičky pre Dlžníkov'
        ),
        user.email,
    )


def send_buyback_notice_borrower(user, auction):
    """Dlžníkovi: pôžička bola odkúpená platformou, dlh teraz voči platforme."""
    _send(
        'Vaša pôžička bola odkúpená platformou',
        (
            f'Dobrý deň,\n\n'
            f'vaša pôžička #{auction.pk} ({auction.amount_requested} €) nebola splatená do 90 dní po splatnosti '
            f'a bola odkúpená platformou Pôžičky pre Dlžníkov. Váš dlh teraz evidujeme priamo voči platforme, '
            f'prosíme uhraďte dlžnú sumu čo najskôr, inak bude pristúpené k ďalšiemu vymáhaniu.\n\n'
            f'S pozdravom,\nPôžičky pre Dlžníkov'
        ),
        user.email,
    )


def send_auction_expired(user, auction):
    """Dlžníkovi: žiadosť o pôžičku nebola vyfinancovaná do konca lehoty a bola zrušená."""
    _send(
        'Vaša žiadosť o pôžičku nebola vyfinancovaná',
        (
            f'Dobrý deň,\n\n'
            f'Vaša žiadosť o pôžičku {auction.amount_requested} € bohužiaľ nebola vyfinancovaná žiadnym '
            f'investorom v stanovenej lehote a bola zrušená.\n\n'
            f'Môžete podať novú žiadosť vo svojom účte.\n\n'
            f'S pozdravom,\nPôžičky pre Dlžníkov'
        ),
        user.email,
    )


def send_payment_due_soon_reminder(user, auction, days_left):
    """Dlžníkovi: pripomienka, že splatnosť sa blíži."""
    _send(
        'Pripomienka: blíži sa splatnosť vašej pôžičky',
        (
            f'Dobrý deň,\n\n'
            f'splatnosť vašej pôžičky #{auction.pk} ({auction.amount_requested} €) sa blíži '
            f'({days_left} {"deň" if days_left == 1 else "dni" if days_left < 5 else "dní"} do splatnosti). '
            f'Všetky platobné údaje nájdete vo svojom účte (sekcia "Moje pôžičky").\n\n'
            f'S pozdravom,\nPôžičky pre Dlžníkov'
        ),
        user.email,
    )
