"""Spolocne stavebne bloky pre financne ilustracie v9 (SVG)."""
from d7_common import svg  # noqa: F401


def defs(c1, c2, c3='#fff'):
    return ('<defs><linearGradient id="g1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
            '<linearGradient id="g2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s" stop-opacity=".55"/><stop offset="1" stop-color="%s" stop-opacity="0"/></linearGradient>'
            '<filter id="sh" x="-20%%" y="-20%%" width="140%%" height="150%%"><feDropShadow dx="0" dy="10" stdDeviation="9" flood-color="#000" flood-opacity=".22"/></filter></defs>'
            % (c1, c2, c1, c1))


def line_chart(x, y, w, h, col, pts=None, area=True, sw=4):
    pts = pts or [.8, .62, .7, .45, .5, .28, .32, .1]
    n = len(pts) - 1
    xy = [(x + w * i / n, y + h * p) for i, p in enumerate(pts)]
    d = 'M' + ' L'.join('%g %g' % q for q in xy)
    out = ''
    if area:
        out += '<path d="%s L%g %g L%g %g Z" fill="url(#g2)"/>' % (d, x + w, y + h, x, y + h)
    out += '<path d="%s" stroke="%s" stroke-width="%d" fill="none"/>' % (d, col, sw)
    out += '<circle cx="%g" cy="%g" r="8" fill="#fff" stroke="%s" stroke-width="4"/>' % (xy[-1][0], xy[-1][1], col)
    return out


def bars(x, y, w, h, cols, vals=None, gap=10):
    vals = vals or [.4, .55, .5, .75, .65, .95]
    bw = (w - gap * (len(vals) - 1)) / len(vals)
    out = ''
    for i, v in enumerate(vals):
        out += '<rect x="%g" y="%g" width="%g" height="%g" rx="%g" fill="%s"/>' % (
            x + i * (bw + gap), y + h * (1 - v), bw, h * v, min(8, bw / 2), cols[i % len(cols)])
    return out


def card(x, y, w, h, fill='#fff', r=18, extra=''):
    return '<g filter="url(#sh)"><rect x="%g" y="%g" width="%g" height="%g" rx="%d" fill="%s"/></g>%s' % (x, y, w, h, r, fill, extra)


def coin(cx, cy, r, c1='#FFD166', c2='#F5A524', sym='€'):
    return ('<circle cx="%g" cy="%g" r="%g" fill="%s"/><circle cx="%g" cy="%g" r="%g" fill="none" stroke="%s" stroke-width="3"/>'
            '<text x="%g" y="%g" font-family="Arial,sans-serif" font-weight="700" font-size="%g" fill="%s" text-anchor="middle">%s</text>'
            % (cx, cy, r, c1, cx, cy, r * .78, c2, cx, cy + r * .33, r * 1.0, c2, sym))


def bank_card(x, y, w, h, c1, c2, rot=0):
    b = '<g transform="rotate(%g %g %g)" filter="url(#sh)">' % (rot, x + w / 2, y + h / 2)
    b += '<rect x="%g" y="%g" width="%g" height="%g" rx="16" fill="url(#g1)"/>' % (x, y, w, h)
    b += '<rect x="%g" y="%g" width="44" height="32" rx="6" fill="#FFD166" opacity=".9"/>' % (x + 22, y + 30)
    b += '<circle cx="%g" cy="%g" r="18" fill="#fff" opacity=".35"/><circle cx="%g" cy="%g" r="18" fill="#fff" opacity=".55"/>' % (x + w - 52, y + h - 30, x + w - 34, y + h - 30)
    for i in range(4):
        b += '<rect x="%g" y="%g" width="34" height="7" rx="3" fill="#fff" opacity=".7"/>' % (x + 22 + i * 44, y + h - 40)
    return b + '</g>'


def donut(cx, cy, r, parts, sw=22):
    import math
    out, tot, acc = '', sum(p[0] for p in parts), 0
    circ = 2 * math.pi * r
    for v, col in parts:
        out += ('<circle cx="%g" cy="%g" r="%g" fill="none" stroke="%s" stroke-width="%d" stroke-dasharray="%.1f %.1f" '
                'stroke-dashoffset="%.1f" transform="rotate(-90 %g %g)"/>' % (cx, cy, r, col, sw, circ * v / tot, circ, -circ * acc / tot, cx, cy))
        acc += v
    return out


def shield(cx, cy, s, col, tick='#fff'):
    return ('<g transform="translate(%g %g) scale(%g)"><path d="M0 -50 42 -32V4C42 30 22 46 0 54 -22 46 -42 30 -42 4V-32z" fill="%s"/>'
            '<path d="M-17 4 -4 18 20 -14" stroke="%s" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>' % (cx, cy, s, col, tick))


def pill(x, y, w, col, op=1):
    return '<rect x="%g" y="%g" width="%g" height="10" rx="5" fill="%s" opacity="%g"/>' % (x, y, w, col, op)


def icon_set(c_main, c_alt, c_acc):
    d = defs(c_main, c_alt)
    i1 = svg(140, 140, d + '<circle cx="70" cy="70" r="56" fill="url(#g1)"/>' + line_chart(30, 40, 80, 56, '#fff', area=False, sw=6))
    i2 = svg(140, 140, d + '<circle cx="70" cy="70" r="56" fill="url(#g1)"/>' + donut(70, 70, 28, [(55, '#fff'), (25, c_acc), (20, 'rgba(255,255,255,.4)')], 16))
    i3 = svg(140, 140, d + '<circle cx="70" cy="70" r="56" fill="url(#g1)"/>' + shield(70, 70, .75, '#fff', c_main))
    i4 = svg(140, 140, d + '<circle cx="70" cy="70" r="56" fill="url(#g1)"/>' + bars(38, 38, 64, 64, ['#fff', c_acc, '#fff', c_acc]))
    return {'ic1': i1, 'ic2': i2, 'ic3': i3, 'ic4': i4}


def wave(w, h, col, op=1, amp=40, freq=2, ph=0):
    import math
    pts = ['%g %g' % (x, h * .5 + amp * math.sin(ph + x / w * math.pi * 2 * freq)) for x in range(0, w + 1, 20)]
    return '<path d="M0 %g L%s L%g %g L0 %g Z" fill="%s" opacity="%g"/>' % (h, ' L'.join(pts), w, h, h, col, op)


def grid_dots(w, h, step, col, op=.25, r=2):
    return ''.join('<circle cx="%d" cy="%d" r="%g" fill="%s" opacity="%g"/>' % (x, y, r, col, op)
                   for x in range(step // 2, w, step) for y in range(step // 2, h, step))
