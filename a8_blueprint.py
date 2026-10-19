from d7_common import svg

L, Y, C = '#CFE8FF', '#FFD166', '#7FE3FF'


def grid(w, h, step=40, op=.13):
    s = ''.join('<path d="M%d 0V%d"/>' % (x, h) for x in range(0, w + 1, step))
    s += ''.join('<path d="M0 %dH%d"/>' % (y, w) for y in range(0, h + 1, step))
    return '<g stroke="%s" stroke-opacity="%s">%s</g>' % (L, op, s)


def txt(x, y, t, size=12, anchor='middle', fill=L):
    return ('<text x="%g" y="%g" font-family="monospace" font-size="%d" fill="%s" stroke="none" '
            'text-anchor="%s">%s</text>' % (x, y, size, fill, anchor, t))


def hdim(x1, x2, y, label):
    return ('<path d="M%g %gH%g M%g %gv12 M%g %gv12M%g %gl9 -5v10z M%g %gl-9 -5v10z"/>' % (
        x1, y, x2, x1, y - 6, x2, y - 6, x1, y, x2, y) + txt((x1 + x2) / 2, y - 8, label))


def hero():
    b = grid(520, 420) + '<g stroke="%s" stroke-width="2.5">' % L
    b += '<rect x="150" y="110" width="220" height="270"/><path d="M130 110H390M150 150H370"/>'
    for r in range(5):
        for c in range(4):
            b += '<rect x="%d" y="%d" width="30" height="24" stroke-width="1.8"/>' % (170 + c * 50, 168 + r * 40)
    b += '<path d="M240 380v-46a20 20 0 0 1 40 0v46"/></g>'
    b += '<path d="M260 70V400" stroke="%s" stroke-dasharray="14 5 3 5" stroke-opacity=".7"/>' % C
    b += '<g stroke="%s" stroke-width="1.6">%s</g>' % (L, hdim(150, 370, 92, '22,0 m'))
    b += '<path d="M410 110V380M404 110h12M404 380h12" stroke="%s"/>' % L + txt(436, 250, '42 m', 12, 'start')
    b += '<polyline points="40,330 110,290 175,300 235,230 300,240 360,160 450,70" stroke="%s" stroke-width="5"/>' % Y
    for x, y in [(110, 290), (235, 230), (360, 160), (450, 70)]:
        b += '<rect x="%d" y="%d" width="12" height="12" fill="#0E3A7A" stroke="%s" stroke-width="3"/>' % (x - 6, y - 6, Y)
    b += '<g stroke="%s" stroke-width="2.5"><circle cx="90" cy="360" r="40"/><circle cx="90" cy="360" r="26"/>' % L
    b += '<path d="M30 360H150M90 300V420" stroke-dasharray="10 4 2 4" stroke="%s"/></g>' % C
    b += txt(90, 424, 'ø 80', 11)
    return svg(520, 420, b)


def icons():
    f = '<g stroke="%s" stroke-width="3">%%s</g>' % L
    ic1 = f % ('<circle cx="70" cy="70" r="46"/><circle cx="70" cy="70" r="30"/><path d="M14 70H126M70 14V126" stroke="%s" stroke-dasharray="8 4"/>' % C)
    teeth = ''.join('<rect x="62" y="12" width="16" height="22" transform="rotate(%d 70 70)"/>' % (a * 45) for a in range(8))
    ic2 = f % (teeth + '<circle cx="70" cy="70" r="38"/><circle cx="70" cy="70" r="14"/>')
    ic3 = f % '<path d="M70 14 118 34v36c0 28-22 46-48 56C44 116 22 98 22 70V34z"/><path d="M48 70l16 16 30-32" stroke="%s"/>' % Y
    ic4 = f % ('<path d="M20 110V70h30V110zM60 110V40h30V110zM100 110V20h26V110z"/><path d="M10 120H130" stroke="%s"/>' % C)
    return [svg(140, 140, i) for i in (ic1, ic2, ic3, ic4)]


def foot():
    b = '<g stroke="%s" stroke-width="2.5">' % L
    x = 0
    for i in range(14):
        w, h = 70 + (i * 37) % 60, 50 + (i * 53) % 90
        b += '<rect x="%d" y="%d" width="%d" height="%d"/>' % (x, 190 - h, w, h)
        x += w + 12
    b += '<path d="M0 190H1400"/></g>' + grid(1400, 200, 40, .08)
    return svg(1400, 200, b)


def crane():
    b = '<g stroke="%s" stroke-width="3"><path d="M120 190V30M140 190V30M120 190h20M120 150l20-20M120 110l20-20M120 70l20-20"/>' % L
    b += '<path d="M40 30H330V50H40zM140 30L240 6L330 30M60 30V90" stroke="%s"/>' % Y
    b += '<path d="M60 90v26M50 116h20" stroke="%s"/></g>' % C
    return svg(360, 200, b)


def build():
    ic = icons()
    ex = {'foot': foot(), 'crane': crane(), 'grid': svg(80, 80, grid(80, 80, 40, .22))}
    ex.update({'ic%d' % (i + 1): s for i, s in enumerate(ic)})
    return hero(), ex
