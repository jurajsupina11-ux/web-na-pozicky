from d7_common import svg

INK, PAP, RED = '#1A1A1A', '#F4EEDF', '#B3261E'


def halftone(x, y, w, h, step=9, rmax=4.2, grad='x', col=INK):
    out = ''
    nx, ny = int(w / step), int(h / step)
    for i in range(nx):
        for j in range(ny):
            t = (i / nx) if grad == 'x' else (j / ny)
            r = rmax * t
            if r > .5:
                out += '<circle cx="%g" cy="%g" r="%.1f" fill="%s"/>' % (x + i * step + step / 2, y + j * step + step / 2, r, col)
    return out


def hatch(x, y, w, h, gap=7, col=INK, sw=1.4):
    out = ''
    for k in range(-int(h), int(w), gap):
        out += '<path d="M%g %gL%g %g"/>' % (x + max(k, 0), y + max(-k, 0), x + min(k + h, w), y + min(h, w - k))
    return '<g stroke="%s" stroke-width="%s">%s</g>' % (col, sw, out)


def hero():
    b = '<rect x="20" y="20" width="480" height="380" fill="%s" stroke="%s" stroke-width="4"/>' % (PAP, INK)
    b += '<rect x="30" y="30" width="460" height="360" fill="none" stroke="%s" stroke-width="1.5"/>' % INK
    b += '<rect x="50" y="52" width="250" height="26" fill="%s"/>' % INK
    b += '<g stroke="%s" stroke-width="3">' % INK
    for i in range(5):
        b += '<path d="M320 %d H460"/>' % (60 + i * 11)
    b += '</g>'
    b += halftone(50, 96, 250, 150, 8, 3.6, 'y')
    b += '<path d="M50 240 110 190 160 215 230 140 300 120" stroke="%s" stroke-width="5" fill="none"/>' % RED
    b += '<circle cx="300" cy="120" r="9" fill="%s"/>' % RED
    b += '<rect x="50" y="96" width="250" height="150" fill="none" stroke="%s" stroke-width="2.5"/>' % INK
    b += hatch(320, 96, 140, 150)
    b += '<g fill="%s"><circle cx="390" cy="171" r="46"/></g><text x="390" y="184" font-family="Georgia,serif" font-size="38" font-weight="700" fill="%s" text-anchor="middle">%%</text>' % (RED, PAP)
    for i in range(7):
        b += '<rect x="50" y="%d" width="%d" height="5" fill="%s"/>' % (268 + i * 17, 250 - (i * 37) % 70, INK)
        b += '<rect x="320" y="%d" width="%d" height="5" fill="%s"/>' % (268 + i * 17, 140 - (i * 29) % 50, INK)
    b += '<path d="M310 268V380" stroke="%s" stroke-width="1.5"/>' % INK
    return svg(520, 420, b)


def icon(kind):
    b = '<circle cx="70" cy="70" r="52" fill="%s" stroke="%s" stroke-width="4"/>' % (PAP, INK)
    if kind == 1:
        b += halftone(24, 24, 92, 92, 8, 3.5, 'x')
    elif kind == 2:
        b += hatch(26, 26, 88, 88, 7)
    elif kind == 3:
        b += '<path d="M70 28l12 26 28 3-21 19 6 28-25-14-25 14 6-28-21-19 28-3z" fill="%s"/>' % RED
    else:
        b += '<path d="M34 100V70M58 100V50M82 100V36M106 100V24" stroke="%s" stroke-width="9"/>' % INK
    return svg(140, 140, b)


def band():
    b = ''
    for i in range(40):
        b += '<rect x="%d" y="0" width="%d" height="8" fill="%s"/>' % (i * 36, 22, INK)
    b += halftone(0, 14, 1400, 80, 8, 3.2, 'y', '#F4EEDF')
    return svg(1400, 100, b)


def paper():
    b = ''
    for i in range(60):
        x, y = (i * 97) % 400, (i * 53) % 400
        b += '<circle cx="%d" cy="%d" r="1" fill="#000" opacity=".14"/>' % (x, y)
    return svg(400, 400, b)


def masthead():
    b = '<path d="M0 6H800M0 12H800" stroke="%s" stroke-width="2"/>' % INK
    return svg(800, 20, b)


def build():
    ex = {'paper': paper(), 'foot': band(), 'rule': masthead(), 'ht': svg(300, 300, halftone(0, 0, 300, 300, 10, 4.6, 'y', '#000'))}
    ex.update({'ic%d' % i: icon(i) for i in range(1, 5)})
    return hero(), ex
