"""Centrálne bankové/platobné údaje a generovanie QR kódu pre úhradu.

Jediný bankový účet platformy, na ktorý dlžníci posielajú splátky aj
investori posielajú vklady na peňaženku. Variabilný symbol platby je VŽDY
rodné číslo platiteľa (bez lomítka) - slúži zároveň ako jeho jednoznačný
identifikátor/"číslo účtu" v appke (rovnako ako username u dlžníka).

QR kód sa generuje vo formáte SPD (Short Payment Descriptor, štandard
používaný slovenskými/českými bankovými aplikáciami na načítanie platby
fotoaparátom) - obsahuje IBAN, sumu a variabilný symbol.
"""
import io

from django.http import HttpResponse

#: Jediný bankový účet platformy - prijíma splátky pôžičiek od dlžníkov
#: aj vklady na peňaženku od investorov.
PLATFORM_BANK = {
    'bank_name': 'Fio banka, a.s., pobočka zahraničnej banky',
    'iban': 'SK62 1100 0000 0029 4931 2130',
    'swift': 'FIOZSKBA',
}


def iban_no_spaces(iban: str) -> str:
    return (iban or '').replace(' ', '').upper()


def variable_symbol_for_user(user) -> str:
    """Variabilný symbol platby pre daného používateľa je vždy jeho rodné
    číslo (bez lomítka) - slúži zároveň ako jeho identifikátor/"číslo účtu"
    v rámci platformy. Ak z nejakého dôvodu rodné číslo chýba (nemalo by sa
    stať, KYC je povinné), padneme späť na display_id, aby appka nespadla."""
    value = (getattr(user, 'birth_number', '') or '').replace('/', '').replace(' ', '').strip()
    return value or user.display_id


def build_spd_payload(iban: str, amount, variable_symbol: str, message: str = '') -> str:
    """Zostaví SPD (Short Payment Descriptor) reťazec pre QR platbu -
    formát podporovaný bankovými aplikáciami na Slovensku/v Česku.
    Príklad: SPD*1.0*ACC:SK6211000000002949312130*AM:123.45*CC:EUR*X-VS:1234567890
    """
    clean_iban = iban_no_spaces(iban)
    parts = ['SPD*1.0', f'ACC:{clean_iban}']
    if amount is not None:
        parts.append(f'AM:{amount:.2f}')
    parts.append('CC:EUR')
    if variable_symbol:
        parts.append(f'X-VS:{variable_symbol}')
    if message:
        safe_message = message.replace('*', ' ')[:60]
        parts.append(f'MSG:{safe_message}')
    return '*'.join(parts)


def generate_payment_qr_png(iban: str, amount, variable_symbol: str, message: str = '') -> bytes:
    """Vygeneruje QR kód (PNG bajty) pre úhradu podľa SPD formátu."""
    import qrcode

    payload = build_spd_payload(iban, amount, variable_symbol, message)
    img = qrcode.make(payload, box_size=8, border=2)
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return buffer.getvalue()


def payment_qr_response(iban: str, amount, variable_symbol: str, message: str = '') -> HttpResponse:
    png_bytes = generate_payment_qr_png(iban, amount, variable_symbol, message)
    return HttpResponse(png_bytes, content_type='image/png')
