import math

from a9_common import coin, defs, grid_dots, line_chart, svg, wave


def glyph(k, fg, sw=8):
    s = 'stroke="%s" stroke-width="%d" fill="none" stroke-linecap="round" stroke-linejoin="round"' % (fg, sw)
    if k == 1:
        return '<polyline points="38,98 60,72 78,84 104,44" %s/><path d="M88 44H104V60" %s/>' % (s, s)
    if k == 2:
        return '<circle cx="64" cy="64" r="24" %s/><path d="M82 82L104 104" %s/>' % (s, s)
    if k == 3:
        return ('<path d="M70 32L102 44V70C102 90 88 102 70 108 52 102 38 90 38 70V44z" %s/>'
                '<path d="M56 70L66 80L86 58" %s/>' % (s, s))
    return '<path d="M44 102V74M70 102V52M96 102V36" %s/>' % s


def icons(bg, fg, cols):
    return [svg(140, 140, bg(cols[i % len(cols)]) + glyph(i + 1, fg)) for i in range(4)]


def std_extras(ics, c1, c2, k1='#FFD166', k2='#F5A524'):
    d = {'ic%d' % (i + 1): s for i, s in enumerate(ics)}
    d['wave'] = svg(1400, 200, wave(1400, 200, c1, .35, 30, 2) + wave(1400, 200, c2, .5, 24, 3, 1.5))
    d['chart'] = svg(600, 260, defs(c1, c2) + line_chart(10, 20, 580, 220, c1, None, True, 5))
    d['coins'] = svg(300, 220, coin(80, 120, 50, k1, k2) + coin(180, 90, 36, k1, k2) + coin(230, 160, 44, k1, k2))
    d['dots'] = svg(400, 300, grid_dots(400, 300, 26, c1, .3, 2))
    return d


def synth_hero():
    b = ('<defs><linearGradient id="sn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFD93D"/>'
         '<stop offset="1" stop-color="#FF3CAC"/></linearGradient><filter id="gl"><feGaussianBlur stdDeviation="3.5" result="b"/>'
         '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
         '<clipPath id="cl"><rect width="520" height="250"/></clipPath></defs>')
    for i in range(24):
        b += '<circle cx="%d" cy="%d" r="1.6" fill="#fff" opacity=".7"/>' % ((i * 97) % 520, (i * 41) % 130)
    b += '<g clip-path="url(#cl)"><circle cx="260" cy="175" r="120" fill="url(#sn)"/>'
    for i in range(7):
        b += '<rect x="130" y="%g" width="260" height="%g" fill="#1B0B3A"/>' % (160 + i * 13, 2 + i * 1.7)
    b += '</g><path d="M0 250 70 170 130 230 190 150 250 250zM270 250 340 160 400 220 450 180 520 250z" fill="#2B1060" stroke="#28F2FF" stroke-width="2"/>'
    b += '<rect x="0" y="250" width="520" height="170" fill="#140630"/><g stroke="#FF3CAC" stroke-width="2" filter="url(#gl)">'
    for x in range(-340, 861, 80):
        b += '<path d="M%g 250L%d 420"/>' % (260 + (x - 260) * .12, x)
    for k in range(1, 8):
        b += '<path d="M0 %g H520"/>' % (250 + 170 * (k / 7) ** 2)
    b += '</g><polyline points="40,340 120,305 190,325 270,270 350,290 430,215 490,185" fill="none" stroke="#28F2FF" stroke-width="5" '
    b += 'filter="url(#gl)" stroke-linecap="round" stroke-linejoin="round"/>'
    return svg(520, 420, b + coin(440, 110, 28, '#FFD93D', '#FF3CAC'))


def deco_hero():
    g = '#D4AF37'
    b = '<g stroke="%s" fill="none" stroke-width="2.5">' % g
    for a in range(190, 351, 10):
        t = math.radians(a)
        b += '<path d="M260 400L%g %g"/>' % (260 + 300 * math.cos(t), 400 + 300 * math.sin(t))
    for r in (70, 120, 170, 220, 270):
        b += '<path d="M%d 400A%d %d 0 0 1 %d 400"/>' % (260 - r, r, r, 260 + r)
    b += '</g><polygon points="200,400 200,300 225,300 225,240 245,240 245,170 260,135 275,170 275,240 295,240 295,300 320,300 320,400" '
    b += 'fill="#0C1A2B" stroke="%s" stroke-width="4"/><g stroke="%s" stroke-width="2.5">' % (g, g)
    for x in (212, 236, 260, 284, 308):
        b += '<path d="M%d %d V396"/>' % (x, 310 if x in (212, 308) else 250 if x in (236, 284) else 180)
    b += '</g><path d="M260 60 290 100 260 140 230 100z" fill="%s"/>' % g
    b += '<circle cx="260" cy="100" r="9" fill="#0C1A2B"/><path d="M60 400H460" stroke="%s" stroke-width="5"/>' % g
    for x, y in ((90, 120), (430, 110), (60, 250), (460, 260)):
        b += '<path d="M%d %d l12 14 -12 14 -12 -14z" fill="none" stroke="%s" stroke-width="3"/>' % (x, y - 14, g)
    return svg(520, 420, b)
