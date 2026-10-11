from django.shortcuts import render

DESIGNS = [
    {
        'slug': 'a-cista-modra',
        'number': 1,
        'name': 'A - Čistá modrá (korporátny štýl)',
        'description': 'Pokojný, dôveryhodný štýl pripomínajúci banku. Modrá + biela, veľké karty, jasné čísla.',
    },
    {
        'slug': 'b-urgentna-zelena',
        'number': 2,
        'name': 'B - Urgentná zelená (rýchlosť je kľúč)',
        'description': 'Zvýrazňuje časový tlak "kto prv prišiel" - odpočítavanie, farebné štítky, pocit naliehavosti.',
    },
    {
        'slug': 'c-tmavy-fintech',
        'number': 3,
        'name': 'C - Tmavý fintech štýl',
        'description': 'Moderný dark-mode dizajn, aký používajú fintech/crypto appky. Pôsobí technologicky.',
    },
    {
        'slug': 'd-kartova-jednoducha',
        'number': 4,
        'name': 'D - Jednoduché karty (minimalizmus)',
        'description': 'Veľmi jednoduchý, čistý dizajn bez rušivých prvkov - dôraz na čitateľnosť a pokojný dojem.',
    },
    {
        'slug': 'e-oranzova-energia',
        'number': 5,
        'name': 'E - Oranžová energia (akčný štýl)',
        'description': 'Teplé, energické farby, veľké tlačidlá "Chytiť pôžičku" - pôsobí aktívne a motivujúco.',
    },
]

LOANS_DEMO = [
    {'id': 1, 'borrower': 'Peter K.', 'amount': 150, 'days': 14, 'remaining': '00:04:32', 'claimed_pct': 20},
    {'id': 2, 'borrower': 'Martina S.', 'amount': 300, 'days': 30, 'remaining': '00:01:07', 'claimed_pct': 65},
    {'id': 3, 'borrower': 'Jozef H.', 'amount': 50, 'days': 7, 'remaining': '00:09:50', 'claimed_pct': 0},
    {'id': 4, 'borrower': 'Lucia P.', 'amount': 500, 'days': 30, 'remaining': '00:00:28', 'claimed_pct': 90},
    {'id': 5, 'borrower': 'Tomáš V.', 'amount': 220, 'days': 21, 'remaining': '00:06:15', 'claimed_pct': 40},
]


def interest_fee(amount, days):
    """24% p.a. úrok + 20% poplatok platformy z istiny, prepočítané na dané dni."""
    interest = round(amount * 0.24 * (days / 365), 2)
    fee = round(amount * 0.20, 2)
    total_to_repay = round(amount + interest, 2)
    return interest, fee, total_to_repay


def designs_index(request):
    return render(request, 'designs/index.html', {'designs': DESIGNS})


def design_home(request, slug):
    design = next(d for d in DESIGNS if d['slug'] == slug)
    amount = 150
    days = 14
    interest, fee, total_to_repay = interest_fee(amount, days)
    context = {
        'design': design,
        'designs': DESIGNS,
        'amount': amount,
        'days': days,
        'interest': interest,
        'fee': fee,
        'total_to_repay': total_to_repay,
        'net_to_borrower': round(amount - fee, 2),
    }
    return render(request, f'designs/{design["slug"]}/home.html', context)


def design_rooms(request, slug):
    design = next(d for d in DESIGNS if d['slug'] == slug)
    context = {'design': design, 'designs': DESIGNS, 'loans': LOANS_DEMO}
    return render(request, f'designs/{design["slug"]}/rooms.html', context)


def design_dashboard(request, slug):
    design = next(d for d in DESIGNS if d['slug'] == slug)
    context = {'design': design, 'designs': DESIGNS, 'loans': LOANS_DEMO[:3]}
    return render(request, f'designs/{design["slug"]}/dashboard.html', context)

