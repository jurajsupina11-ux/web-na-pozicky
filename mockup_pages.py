"""Zoznam stranok mockupu: (rola, nazov suboru, URL v appke)."""

PUBLIC = [
    ('landing', '/'), ('investori', '/investori/'),
    ('pre-ziadatelov', '/pre-ziadatelov/'), ('kontakt', '/kontakt/'),
    ('caste-otazky', '/caste-otazky/'),
    ('obchodne-podmienky', '/obchodne-podmienky/'),
    ('ochrana-udajov', '/ochrana-osobnych-udajov/'),
    ('statistiky', '/statistiky/'),
    ('prihlasenie', '/accounts/login/'),
    ('prihlasenie-investor', '/accounts/login/investor/'),
    ('prihlasenie-dlznik', '/accounts/login/dlznik/'),
    ('registracia', '/accounts/signup/'),
    ('ziadost-o-uver', '/accounts/ziadost-o-uver/'),
]

INVESTOR = [
    ('dashboard', '/aukcie/dashboard/'), ('nove-ziadosti', '/aukcie/ziadosti/'),
    ('trh', '/aukcie/trh/'), ('historia', '/aukcie/historia/'),
    ('zmluvy', '/aukcie/moje-zmluvy/'),
    ('danovy-vykaz', '/aukcie/danovy-vykaz/'),
    ('moje-udaje', '/accounts/moje-udaje/'),
    ('nastavenia', '/accounts/nastavenia/'),
    ('zmena-hesla', '/accounts/nastavenia/zmena-hesla/'),
    ('pozvi-priatela', '/accounts/pozvi-priatela/'),
    ('notifikacie', '/notifikacie/'), ('zoznam-aukcii', '/aukcie/'),
]

BORROWER = [
    ('moje-pozicky', '/accounts/moje-ziadosti/'),
    ('ponuky', '/accounts/ponuky/'),
    ('zmluvy', '/accounts/moje-zmluvy/'),
    ('moje-udaje', '/accounts/moje-udaje/'),
    ('nastavenia', '/accounts/nastavenia/'),
    ('zmena-hesla', '/accounts/nastavenia/zmena-hesla/'),
    ('pozvi-priatela', '/accounts/pozvi-priatela/'),
    ('notifikacie', '/notifikacie/'),
    ('stav-ziadosti', '/accounts/stav-ziadosti/'),
    ('nova-ziadost', '/accounts/ziadost-o-uver/'),
]

ADMIN = [
    ('dashboard', '/sprava/'), ('ziadosti', '/sprava/ziadosti/'),
    ('penazenka', '/sprava/penazenka/'), ('pozicky', '/sprava/pozicky/'),
    ('pouzivatelia', '/sprava/pouzivatelia/'), ('trh', '/sprava/trh/'),
    ('audit', '/sprava/audit/'), ('zmluvy', '/sprava/zmluvy/'),
    ('nastavenia', '/sprava/nastavenia/'),
    ('nahlad', '/accounts/admin-nahlad/'),
]


def all_pages():
    out = [('pub', n, u) for n, u in PUBLIC]
    out += [('inv', n, u) for n, u in INVESTOR]
    out += [('bor', n, u) for n, u in BORROWER]
    out += [('adm', n, u) for n, u in ADMIN]
    return out
