from d7_common import svg

PINK, YEL, TEAL, BLK, CRM = '#FF4FA3', '#FFD60A', '#00C2A8', '#14110F', '#FFF4E0'


def zig(x, y, n, w=18, h=14, col=BLK, sw=5):
    pts = ' '.join('%g,%g' % (x + i * w, y + (h if i % 2 else 0)) for i in range(n))
    return '<polyline points="%s" stroke="%s" stroke-width="%d"/>' % (pts, col, sw)


def dots(x, y, cols, rows, gap=14, r=3, col=BLK):
    return ''.join('<circle cx="%d" cy="%d" r="%d" fill="%s"/>' % (x + c * gap, y + rr * gap, r, col)
                   for c in range(cols) for rr in range(rows))


def squig(x, y, col=BLK):
    return '<path d="M%d %d q10 -18 20 0 t20 0 t20 0 t20 0" stroke="%s" stroke-width="5"/>' % (x, y, col)


def hero():
    b = '<circle cx="270" cy="210" r="150" fill="%s" stroke="%s" stroke-width="5"/>' % (YEL, BLK)
    b += '<rect x="60" y="60" width="120" height="120" fill="%s" stroke="%s" stroke-width="5" transform="rotate(-12 120 120)"/>' % (PINK, BLK)
    b += '<path d="M330 40 450 250H210z" fill="%s" stroke="%s" stroke-width="5" transform="translate(70 90) scale(.7)"/>' % (TEAL, BLK)
    b += '<g stroke="%s" stroke-width="5" fill="%s">' % (BLK, CRM)
    for i, h in enumerate((90, 150, 220, 300)):
        b += '<rect x="%d" y="%d" width="52" height="%d"/>' % (150 + i * 62, 390 - h, h)
    b += '</g><polyline points="140,330 220,270 290,290 380,170 450,100" stroke="%s" stroke-width="9"/>' % PINK
    b += '<path d="M450 100l-34 4M450 100l-8 32" stroke="%s" stroke-width="9"/>' % PINK
    b += zig(30, 330, 7) + zig(380, 20, 6, col=PINK) + squig(40, 250, TEAL) + dots(400, 300, 5, 4)
    b += '<circle cx="470" cy="360" r="22" fill="%s" stroke="%s" stroke-width="5"/>' % (PINK, BLK)
    b += '<path d="M60 40l10 22 24 3-18 16 5 24-21-12-21 12 5-24-18-16 24-3z" fill="%s" stroke="%s" stroke-width="4"/>' % (YEL, BLK)
    return svg(520, 420, b)


def icon(kind):
    if kind == 1:
        b = '<circle cx="70" cy="70" r="50" fill="%s" stroke="%s" stroke-width="5"/><path d="M45 72l18 18 34-40" stroke="%s" stroke-width="9"/>' % (YEL, BLK, BLK)
    elif kind == 2:
        b = '<rect x="22" y="22" width="96" height="96" fill="%s" stroke="%s" stroke-width="5" transform="rotate(10 70 70)"/>' % (PINK, BLK) + zig(34, 66, 5, 18, 14)
    elif kind == 3:
        b = '<path d="M70 14 128 118H12z" fill="%s" stroke="%s" stroke-width="5"/><circle cx="70" cy="86" r="16" fill="%s" stroke="%s" stroke-width="4"/>' % (TEAL, BLK, YEL, BLK)
    else:
        b = '<circle cx="70" cy="70" r="52" fill="%s" stroke="%s" stroke-width="5"/>' % (CRM, BLK) + dots(40, 40, 4, 4, 20, 4)
    return svg(140, 140, b)


def band(w=1400, h=120):
    b = '<rect width="%d" height="%d" fill="%s"/>' % (w, h, PINK)
    x = 0
    while x < w:
        b += '<path d="M%d %dl30 -50l30 50z" fill="%s" stroke="%s" stroke-width="4"/>' % (x + 10, h - 8, YEL, BLK)
        b += '<circle cx="%d" cy="30" r="12" fill="%s" stroke="%s" stroke-width="4"/>' % (x + 70, TEAL, BLK)
        x += 120
    return svg(w, h, b)


def confetti():
    b = ''
    cols = (PINK, YEL, TEAL, BLK)
    for i in range(26):
        x, y = (i * 83) % 560, (i * 61) % 300
        c = cols[i % 4]
        if i % 3 == 0:
            b += '<circle cx="%d" cy="%d" r="9" fill="%s"/>' % (x, y, c)
        elif i % 3 == 1:
            b += '<rect x="%d" y="%d" width="16" height="16" fill="%s" transform="rotate(%d %d %d)"/>' % (x, y, c, i * 20, x, y)
        else:
            b += '<path d="M%d %dl14 -6 14 6" stroke="%s" stroke-width="4"/>' % (x, y, c)
    return svg(560, 300, b)


def build():
    ex = {'band': band(), 'confetti': confetti(), 'zig': svg(200, 30, zig(6, 6, 10, 20, 16)), 'dots': svg(120, 120, dots(10, 10, 8, 8, 14, 3))}
    ex.update({'ic%d' % i: icon(i) for i in range(1, 5)})
    return hero(), ex
