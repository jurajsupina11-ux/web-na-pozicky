"""Hero pozadie, ikony krokov a pozadie sekcii domovskej stranky."""
from a9_common import bank_card, bars, grid_dots, line_chart, shield, svg, wave
from home_art1 import D, Pal, circ, dcoin, deep, gcol, mix  # noqa: F401


def hero(p):
    W, H = 1600, 800
    op = .2 if p.dark else .14
    b = D(p.inv, p.bor) + circ(140, 170, 270, p.inv, op, p) + circ(1470, 640, 310, p.bor, op, p)
    b += circ(1330, 120, 130, p.inv, op * .8, p) + circ(250, 700, 120, p.bor, op * .8, p)
    b += grid_dots(W, H, 52, p.line, .09, 2)
    b += bank_card(50, 120, 180, 112, p.inv, deep(p.inv), -10) + bank_card(1370, 520, 180, 112, p.bor, deep(p.bor), 8)
    b += dcoin(p, 120, 520, 36) + dcoin(p, 235, 610, 22) + dcoin(p, 1480, 210, 40) + dcoin(p, 1385, 120, 22) + dcoin(p, 1290, 700, 26)
    b += line_chart(40, 650, 330, 90, p.inv, None, p.style == 'soft', 4)
    b += '<g opacity=".9">' + bars(1200, 300, 200, 120, [p.bor, mix(p.bor, p.bg, .5)], None, 12) + '</g>'
    b += shield(1510, 400, .8, p.inv, gcol(p.inv))
    b += '<g transform="translate(0 640)">' + wave(W, 160, p.bg, 1, 22, 2) + '</g>'
    return svg(W, H, b)


def glyph(k, c):
    g = {1: '<rect x="38" y="28" width="44" height="58" rx="5"/><path d="M48 46H72M48 58H72M48 70H62"/>',
         2: '<circle cx="54" cy="54" r="20"/><path d="M69 69 86 86"/>',
         3: '<circle cx="60" cy="60" r="24"/><path d="M60 72V50M50 58l10-10 10 10"/>'}[k]
    return '<g stroke="%s" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round">%s</g>' % (c, g)


def step_icon(p, k):
    col = (p.bor, p.inv, p.bor)[k - 1]
    s = p.style
    if s in ('line', 'glow'):
        f = ' filter="url(#gl)"' if s == 'glow' else ''
        b = '<g%s><circle cx="60" cy="60" r="50" fill="none" stroke="%s" stroke-width="4"/>%s</g>' % (f, col, glyph(k, col))
    elif s == 'pop':
        b = ('<circle cx="66" cy="66" r="50" fill="%s"/><circle cx="60" cy="60" r="50" fill="%s" stroke="%s" stroke-width="5"/>' % (p.ink, col, p.ink)) + glyph(k, gcol(col))
    elif s == 'geo':
        b = '<rect x="14" y="14" width="96" height="96" fill="%s"/>' % p.ink + '<rect x="8" y="8" width="96" height="96" fill="%s"/>' % col + glyph(k, gcol(col))
    else:
        b = '<g filter="url(#sh)"><circle cx="60" cy="60" r="50" fill="%s"/></g>' % col + glyph(k, gcol(col))
    return svg(120, 120, D(col, col) + b)


def bg2(p):
    W, H = 1600, 700
    b = D(p.inv, p.bor) + circ(80, 120, 200, p.inv, .08, p) + circ(1540, 560, 240, p.bor, .08, p)
    b += grid_dots(W, H, 56, p.line, .06, 2)
    b += '<g opacity=".4">' + dcoin(p, 1400, 90, 26) + dcoin(p, 150, 600, 20) + dcoin(p, 800, 650, 16) + '</g>'
    return svg(W, H, b)
