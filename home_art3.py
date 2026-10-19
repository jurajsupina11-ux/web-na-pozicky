"""Ilustracie kariet Pozicat / Investovat a pozadia pre sekcie stats a cta."""
from a9_common import grid_dots, line_chart, svg, wave, bank_card
from home_art1 import D, circ, dcoin, deep, gcol, panel


def inv_card(p):
    b = D(p.inv, deep(p.inv)) + circ(250, 190, 150, p.inv, .22 if p.dark else .16, p)
    b += panel(p, 60, 60, 300, 200, 22, None, p.inv)
    b += '<text x="86" y="104" font-family="Arial,sans-serif" font-weight="700" font-size="15" fill="%s" opacity=".7">V\u00fdnos p.a.</text>' % p.ink
    b += '<text x="86" y="140" font-family="Arial,sans-serif" font-weight="800" font-size="34" fill="%s">+22,1 %%</text>' % p.ink
    b += line_chart(86, 156, 250, 70, p.inv)
    b += dcoin(p, 390, 215, 42) + dcoin(p, 335, 275, 28) + dcoin(p, 425, 120, 26)
    b += ('<circle cx="360" cy="70" r="30" fill="%s"/><path d="M348 82 L372 58 M354 58 H372 V76" stroke="%s" stroke-width="6" '
          'fill="none" stroke-linecap="round" stroke-linejoin="round"/>' % (p.inv, gcol(p.inv)))
    return svg(480, 340, b)


def bor_card(p):
    b = D(p.bor, deep(p.bor)) + circ(240, 180, 150, p.bor, .22 if p.dark else .16, p)
    b += bank_card(30, 190, 200, 124, p.bor, deep(p.bor), -9)
    b += panel(p, 190, 30, 150, 270, 26, None, p.bor)
    b += '<rect x="230" y="52" width="70" height="8" rx="4" fill="%s" opacity=".3"/>' % p.ink
    b += '<circle cx="265" cy="130" r="40" fill="%s"/>' % p.bor
    b += '<path d="M247 130 L261 144 L286 116" stroke="%s" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>' % gcol(p.bor)
    b += '<text x="265" y="222" text-anchor="middle" font-family="Arial,sans-serif" font-weight="800" font-size="30" fill="%s">200 \u20ac</text>' % p.ink
    b += '<rect x="225" y="246" width="80" height="24" rx="12" fill="%s"/>' % p.bor
    b += dcoin(p, 400, 100, 34) + dcoin(p, 420, 220, 24) + dcoin(p, 365, 285, 20)
    return svg(480, 340, b)


def cta(p):
    W, H = 1400, 420
    b = D('#FFFFFF', '#FFFFFF') + grid_dots(W, H, 46, '#FFFFFF', .16, 2)
    for r in (120, 190, 260):
        b += '<circle cx="1230" cy="330" r="%d" fill="none" stroke="#FFFFFF" stroke-width="2.5" opacity=".22"/>' % r
        b += '<circle cx="170" cy="90" r="%d" fill="none" stroke="#FFFFFF" stroke-width="2.5" opacity=".18"/>' % (r * .8)
    b += wave(W, H, '#FFFFFF', .10, 22, 2) + wave(W, H, '#FFFFFF', .08, 30, 3, 1.4)
    b += dcoin(p, 150, 300, 46) + dcoin(p, 250, 200, 26) + dcoin(p, 1270, 120, 40) + dcoin(p, 1180, 260, 24)
    b += line_chart(980, 230, 300, 120, '#FFFFFF')
    return svg(W, H, b)


def stats(p):
    W, H = 1400, 300
    b = D('#FFFFFF', '#FFFFFF') + grid_dots(W, H, 36, '#FFFFFF', .14, 2)
    b += '<polyline points="0,230 140,200 260,215 400,150 560,170 720,100 880,125 1040,60 1220,80 1400,30" fill="none" stroke="#FFFFFF" stroke-width="3" opacity=".24"/>'
    b += '<circle cx="1330" cy="250" r="130" fill="none" stroke="#FFFFFF" stroke-width="2.5" opacity=".2"/>'
    b += '<circle cx="70" cy="60" r="90" fill="none" stroke="#FFFFFF" stroke-width="2.5" opacity=".2"/>'
    return svg(W, H, b)

