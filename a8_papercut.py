from d7_common import svg

F = '<filter id="s" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="6" stdDeviation="5" flood-color="#000" flood-opacity=".3"/></filter>'


def layer(d, col, dy=0):
    return '<path d="%s" fill="%s" filter="url(#s)" transform="translate(0 %d)"/>' % (d, col, dy)


def hills(w, h, cols, seed=0):
    out = ''
    n = len(cols)
    for i, c in enumerate(cols):
        base = h * (0.35 + 0.6 * i / n)
        pts = 'M0 %d' % h
        for k in range(0, w + 1, w // 8):
            y = base + ((k * 7 + i * 91 + seed) % 60) - 30
            pts += ' L%d %d' % (k, y)
        pts += ' L%d %d Z' % (w, h)
        out += layer(pts, c)
    return out


def hero():
    b = '<defs>%s</defs>' % F
    b += '<circle cx="380" cy="110" r="70" fill="#FFD27A" filter="url(#s)"/>'
    b += '<circle cx="380" cy="110" r="46" fill="#FFE9B0"/>'
    b += hills(520, 420, ['#BFE3D4', '#8FCFB8', '#5FB89A', '#2F8F78'])
    for x, hh in ((90, 120), (150, 160), (210, 100)):
        b += '<path d="M%d %d l30 %d h-60z" fill="#1F6B5A" filter="url(#s)"/>' % (x, 300 - hh, hh)
    b += '<g filter="url(#s)">'
    for i, h in enumerate((70, 110, 160, 220)):
        b += '<rect x="%d" y="%d" width="54" height="%d" rx="6" fill="%s"/>' % (230 + i * 66, 400 - h, h, ('#FF9E80', '#FF8A65', '#F4693F', '#E24E1B')[i])
    b += '</g>'
    b += '<g filter="url(#s)" fill="#fff"><ellipse cx="110" cy="80" rx="50" ry="20"/><ellipse cx="150" cy="70" rx="36" ry="20"/><ellipse cx="60" cy="150" rx="40" ry="14"/></g>'
    b += '<path d="M440 70l12 -34 12 34 34 12 -34 12 -12 34 -12 -34 -34 -12z" fill="#fff" filter="url(#s)" transform="translate(-80 -10) scale(.6)"/>'
    return svg(520, 420, b)


def icon(kind):
    b = '<defs>%s</defs>' % F
    if kind == 1:
        b += '<circle cx="70" cy="70" r="52" fill="#FF9E80" filter="url(#s)"/><circle cx="70" cy="70" r="34" fill="#FFD27A"/><circle cx="70" cy="70" r="14" fill="#F4693F"/>'
    elif kind == 2:
        b += '<rect x="26" y="20" width="88" height="100" rx="10" fill="#8FCFB8" filter="url(#s)"/><rect x="40" y="40" width="60" height="10" rx="5" fill="#fff"/><rect x="40" y="62" width="44" height="10" rx="5" fill="#fff"/><rect x="40" y="84" width="52" height="10" rx="5" fill="#fff"/>'
    elif kind == 3:
        b += '<path d="M70 14 124 40v34c0 30-24 50-54 60C40 124 16 104 16 74V40z" fill="#5FB89A" filter="url(#s)"/><path d="M46 72l18 18 32-38" stroke="#fff" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    else:
        b += '<g filter="url(#s)"><rect x="20" y="76" width="26" height="44" rx="4" fill="#FFD27A"/><rect x="56" y="50" width="26" height="70" rx="4" fill="#FF9E80"/><rect x="92" y="20" width="26" height="100" rx="4" fill="#F4693F"/></g>'
    return svg(140, 140, b)


def footer():
    b = '<defs>%s</defs>' % F + hills(1400, 220, ['#5FB89A', '#2F8F78', '#1F6B5A', '#134D40'], 33)
    return svg(1400, 220, b)


def cta():
    b = '<defs>%s</defs>' % F + hills(800, 260, ['#FFD27A', '#FFB48F', '#FF8A65'], 7)
    b += '<circle cx="640" cy="80" r="46" fill="#FFF3D6" filter="url(#s)"/>'
    return svg(800, 260, b)


def sky():
    b = '<defs>%s</defs><g fill="#fff" filter="url(#s)" opacity=".9">' % F
    for x, y, r in ((90, 80, 1), (330, 150, .8), (560, 60, 1.2), (780, 140, .9)):
        b += '<ellipse cx="%g" cy="%g" rx="%g" ry="%g"/><ellipse cx="%g" cy="%g" rx="%g" ry="%g"/>' % (x, y, 60 * r, 20 * r, x + 40 * r, y - 12 * r, 42 * r, 22 * r)
    return svg(900, 220, b + '</g>')


def build():
    ex = {'foot': footer(), 'cta': cta(), 'sky': sky()}
    ex.update({'ic%d' % i: icon(i) for i in range(1, 5)})
    return hero(), ex
