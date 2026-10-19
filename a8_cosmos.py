from d7_common import svg

DEFS = ('<defs><radialGradient id="p1" cx="35%" cy="30%"><stop offset="0" stop-color="#FFB5F0"/><stop offset="1" stop-color="#7A2CF0"/></radialGradient>'
        '<radialGradient id="p2" cx="35%" cy="30%"><stop offset="0" stop-color="#FFE9A0"/><stop offset="1" stop-color="#FF7A3D"/></radialGradient>'
        '<radialGradient id="p3" cx="35%" cy="30%"><stop offset="0" stop-color="#B8F3FF"/><stop offset="1" stop-color="#2D7BFF"/></radialGradient>'
        '<linearGradient id="fl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE066"/><stop offset="1" stop-color="#FF4D4D" stop-opacity="0"/></linearGradient></defs>')


def stars(w, h, n, seed=3):
    out = ''
    for i in range(n):
        x = (i * 7919 + seed * 131) % w
        y = (i * 104729 + seed * 71) % h
        r = 0.8 + (i % 4) * 0.6
        out += '<circle cx="%d" cy="%d" r="%.1f" fill="#fff" opacity="%.2f"/>' % (x, y, r, 0.35 + (i % 5) * 0.13)
    return out


def rocket(x, y, s=1.0, rot=35):
    b = '<g transform="translate(%g %g) rotate(%d) scale(%g)">' % (x, y, rot, s)
    b += '<path d="M0 70 -14 120 14 120z" fill="url(#fl)"/>'
    b += '<path d="M0 -70C26 -40 28 20 20 70H-20C-28 20 -26 -40 0 -70z" fill="#EEF2FF"/>'
    b += '<path d="M-20 40-44 78-20 66zM20 40 44 78 20 66z" fill="#FF4D6D"/>'
    b += '<circle cx="0" cy="-12" r="13" fill="#2D7BFF" stroke="#B8F3FF" stroke-width="4"/>'
    b += '<path d="M0 -70C12 -62 20 -50 22 -38H-22C-20 -50 -12 -62 0 -70z" fill="#FF4D6D"/></g>'
    return b


def planet(cx, cy, r, grad, ring=False):
    b = '<circle cx="%d" cy="%d" r="%d" fill="url(#%s)"/>' % (cx, cy, r, grad)
    if ring:
        b += '<ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="none" stroke="#FFE9A0" stroke-width="5" opacity=".8" transform="rotate(-18 %d %d)"/>' % (cx, cy, r * 1.7, r * .38, cx, cy)
    return b


def hero():
    b = DEFS + stars(520, 420, 55)
    b += planet(380, 120, 70, 'p2', True) + planet(90, 300, 46, 'p1') + planet(450, 330, 28, 'p3')
    b += '<path d="M40 380Q200 330 330 250T480 120" stroke="#6EE7FF" stroke-width="3" stroke-dasharray="3 10" fill="none"/>'
    b += rocket(250, 230, 1.15, 38)
    b += '<g stroke="#6EE7FF" stroke-width="3" fill="none"><circle cx="150" cy="110" r="32" opacity=".5"/><circle cx="150" cy="110" r="52" opacity=".25"/></g>'
    return svg(520, 420, b)


def icon(kind):
    b = DEFS
    if kind == 1:
        b += planet(70, 70, 46, 'p1', True)
    elif kind == 2:
        b += planet(70, 70, 46, 'p2')
    elif kind == 3:
        b += planet(70, 70, 46, 'p3', True)
    else:
        b += rocket(70, 66, .6, 25)
    return svg(140, 140, b)


def space(w, h, n, seed):
    return svg(w, h, stars(w, h, n, seed))


def horizon():
    b = DEFS + stars(1400, 260, 70, 9)
    b += '<ellipse cx="700" cy="560" rx="900" ry="360" fill="#0E1E55"/><ellipse cx="700" cy="560" rx="900" ry="360" fill="none" stroke="#6EE7FF" stroke-width="3" opacity=".7"/>'
    b += planet(1180, 90, 40, 'p2', True)
    return svg(1400, 260, b)


def build():
    ex = {'space': space(900, 600, 120, 1), 'horizon': horizon(), 'stars': space(560, 360, 50, 5)}
    ex.update({'ic%d' % i: icon(i) for i in range(1, 5)})
    return hero(), ex
