from django.shortcuts import render

DESIGNS = [
    {
        'slug': 'a-cista-modra',
        'number': 1,
        'name': 'A – Sklenený gradient',
        'description': 'Teplý oranžový gradient, "glassmorphism" polopriehľadné karty. Moderné a vzdušné.',
        'bg': 'linear-gradient(135deg,#ff7a3d 0%,#ff9a56 45%,#ffb37a 100%)',
        'surface': 'rgba(255,255,255,0.16)',
        'text': '#ffffff',
        'primary': '#ffffff',
        'primary_text': '#c2410c',
        'muted': 'rgba(255,255,255,0.8)',
        'border': 'rgba(255,255,255,0.35)',
        'accent': '#ffd27a',
        'font': "'Poppins', Arial, sans-serif",
        'radius': '20px',
    },
    {
        'slug': 'b-urgentna-zelena',
        'number': 2,
        'name': 'B – Čierno-oranžový kontrast',
        'description': 'Vysoký kontrast čierna + oranžová. Pôsobí odvážne, naliehavo.',
        'bg': '#0e0b09',
        'surface': '#1a1512',
        'text': '#fff2e8',
        'primary': '#ff6a2b',
        'primary_text': '#0e0b09',
        'muted': '#b89a86',
        'border': '#352720',
        'accent': '#ffb037',
        'font': "'Archivo Black', Arial, sans-serif",
        'radius': '6px',
    },
    {
        'slug': 'c-tmavy-fintech',
        'number': 3,
        'name': 'C – Pastelová broskyňová',
        'description': 'Jemná, krémovo-broskyňová paleta, zaoblené tvary, priateľský a pokojný dojem.',
        'bg': '#fff1e6',
        'surface': '#ffffff',
        'text': '#5c3a24',
        'primary': '#ff8a4c',
        'primary_text': '#ffffff',
        'muted': '#a87d63',
        'border': '#ffd9b8',
        'accent': '#ffb37a',
        'font': "'Nunito', Arial, sans-serif",
        'radius': '28px',
    },
    {
        'slug': 'd-kartova-jednoducha',
        'number': 4,
        'name': 'D – Tmavý mód s neónovou oranžovou',
        'description': 'Čierne pozadie, žiarivá neónová oranžová ako v moderných fintech appkách.',
        'bg': '#08090c',
        'surface': '#121318',
        'text': '#f5f6fa',
        'primary': '#ff5c1a',
        'primary_text': '#08090c',
        'muted': '#8a8d9c',
        'border': '#22242e',
        'accent': '#ff8c42',
        'font': "'Space Grotesk', Arial, sans-serif",
        'radius': '14px',
        'glow': True,
    },
    {
        'slug': 'e-oranzova-energia',
        'number': 5,
        'name': 'E – Kartová mriežka (energická)',
        'description': 'Svetlé pozadie, výrazné oranžové karty v mriežke. Energické a prehľadné.',
        'bg': '#fffaf5',
        'surface': '#fff3ea',
        'text': '#2a1b10',
        'primary': '#ff6a2b',
        'primary_text': '#ffffff',
        'muted': '#8a6a56',
        'border': '#ffd9bf',
        'accent': '#ff9a56',
        'font': "'Rubik', Arial, sans-serif",
        'radius': '18px',
    },
    {
        'slug': 'f-investor-modra',
        'number': 6,
        'name': 'F – Investor (modrá, dátová dashboard appka)',
        'description': 'Moderný fintech dashboard pre investora: sidebar, bento grid metrík, reálne SVG ikony, žiadne gradienty. Inšpirované Stripe/Mercury.',
        'bg': '#f6f8fb',
        'surface': '#ffffff',
        'text': '#0f1729',
        'primary': '#2554ea',
        'primary_text': '#ffffff',
        'muted': '#55607a',
        'border': '#e8ecf3',
        'accent': '#2554ea',
        'font': "'Inter', Arial, sans-serif",
        'radius': '16px',
    },
    {
        'slug': 'g-dlznik-oranzova',
        'number': 7,
        'name': 'G – Dlžník (oranžová, veľká typografia, jednoduchá appka)',
        'description': 'Moderná konzumná fintech appka pre dlžníka: veľká typografia, jasné CTA, minimum dát, žiadne gradienty ani emoji ikony. Inšpirované Wise/Revolut.',
        'bg': '#fffdfb',
        'surface': '#ffffff',
        'text': '#20150d',
        'primary': '#f05a22',
        'primary_text': '#ffffff',
        'muted': '#6b5a4d',
        'border': '#f1e6db',
        'accent': '#f05a22',
        'font': "'Manrope', Arial, sans-serif",
        'radius': '20px',
    },
]

LOANS_DEMO = [
    {'id': 1, 'borrower': 'Peter K.', 'amount': 150, 'days': 14, 'remaining': '00:04:32', 'claimed_pct': 20, 'purpose': 'Oprava auta'},
    {'id': 2, 'borrower': 'Martina S.', 'amount': 300, 'days': 30, 'remaining': '00:01:07', 'claimed_pct': 65, 'purpose': 'Nedoplatok za energie'},
    {'id': 3, 'borrower': 'Jozef H.', 'amount': 50, 'days': 7, 'remaining': '00:09:50', 'claimed_pct': 0, 'purpose': 'Krátkodobá rezerva'},
    {'id': 4, 'borrower': 'Lucia P.', 'amount': 500, 'days': 30, 'remaining': '00:00:28', 'claimed_pct': 90, 'purpose': 'Zubár'},
    {'id': 5, 'borrower': 'Tomáš V.', 'amount': 220, 'days': 21, 'remaining': '00:06:15', 'claimed_pct': 40, 'purpose': 'Nákup náradia'},
]


def interest_fee(amount, days):
    """24% p.a. úrok + 20% poplatok platformy z istiny."""
    interest = round(amount * 0.24 * (days / 365), 2)
    fee = round(amount * 0.20, 2)
    total_to_repay = round(amount + interest, 2)
    return interest, fee, total_to_repay


def _get_design(slug):
    return next(d for d in DESIGNS if d['slug'] == slug)


def designs_index(request):
    return render(request, 'designs/index.html', {'designs': DESIGNS})


def design_home(request, slug):
    design = _get_design(slug)
    amount, days = 150, 14
    interest, fee, total_to_repay = interest_fee(amount, days)
    context = {
        'design': design, 'designs': DESIGNS, 'amount': amount, 'days': days,
        'interest': interest, 'fee': fee, 'total_to_repay': total_to_repay,
        'net_to_borrower': round(amount - fee, 2),
    }
    return render(request, f'designs/{slug}/home.html', context)


def design_rooms(request, slug):
    design = _get_design(slug)
    return render(request, f'designs/{slug}/rooms.html', {'design': design, 'designs': DESIGNS, 'loans': LOANS_DEMO})


def design_dashboard(request, slug):
    design = _get_design(slug)
    context = {
        'design': design, 'designs': DESIGNS, 'loans': LOANS_DEMO[:3],
        'total_invested': 1240, 'active_count': 3, 'expected_yield': 86.40,
        'avg_interest': 24, 'total_lifetime_yield': 312.50,
    }
    return render(request, f'designs/{slug}/dashboard.html', context)


def design_loan_detail(request, slug, loan_id):
    design = _get_design(slug)
    loan = next(l for l in LOANS_DEMO if l['id'] == loan_id)
    interest, fee, total_to_repay = interest_fee(loan['amount'], loan['days'])
    context = {
        'design': design, 'designs': DESIGNS, 'loan': loan,
        'interest': interest, 'fee': fee, 'total_to_repay': total_to_repay,
    }
    return render(request, f'designs/{slug}/loan_detail.html', context)


def design_how_it_works(request, slug):
    design = _get_design(slug)
    return render(request, f'designs/{slug}/how_it_works.html', {'design': design, 'designs': DESIGNS})


MY_LOANS_DEMO = [
    {'id': 101, 'amount': 200, 'days': 14, 'status': 'Aktívna', 'due': '24.10.2026', 'paid_pct': 0, 'repay': 203.84},
    {'id': 102, 'amount': 100, 'days': 7, 'status': 'Splatená', 'due': '02.09.2026', 'paid_pct': 100, 'repay': 100.46},
    {'id': 103, 'amount': 350, 'days': 30, 'status': 'Po splatnosti', 'due': '28.09.2026', 'paid_pct': 0, 'repay': 356.90},
]

DOCUMENTS_DEMO = [
    {'name': 'Zmluva o pôžičke #101', 'date': '10.10.2026', 'type': 'PDF'},
    {'name': 'Zmluva o pôžičke #102', 'date': '26.08.2026', 'type': 'PDF'},
    {'name': 'Potvrdenie o úhrade #102', 'date': '02.09.2026', 'type': 'PDF'},
    {'name': 'Všeobecné obchodné podmienky', 'date': '01.01.2026', 'type': 'PDF'},
]


def design_my_loans(request, slug):
    design = _get_design(slug)
    context = {
        'design': design, 'designs': DESIGNS,
        'my_loans': MY_LOANS_DEMO, 'documents': DOCUMENTS_DEMO,
        'postpone_fee': 15,
    }
    return render(request, f'designs/{slug}/my_loans.html', context)
