"""Paleta, panely a drobne prvky pre ilustracie domovskej stranky."""
from a9_common import coin


def hx(c, d):
    c = (c or '').strip()
    if c.startswith('#') and len(c) in (4, 7):
        if len(c) == 4:
            c = '#' + ''.join(ch * 2 for ch in c[1:])
        try:
            int(c[1:], 16)
            return c.upper()
        except ValueError:
            pass
    return d


def mix(a, b, t):
    a, b = a.lstrip('#'), b.lstrip('#')
    r = [round(int(a[i:i + 2], 16) * (1 - t) + int(b[i:i + 2], 16) * t) for i in (0, 2, 4)]
    return '#%02X%02X%02X' % tuple(r)


def lum(c):
    c = c.lstrip('#')
    r, g, b = [int(c[i:i + 2], 16) for i in (0, 2, 4)]
    return (.299 * r + .587 * g + .114 * b) / 255


def deep(c):
    return mix(c, '#000000', .35 + .4 * lum(c))


def gcol(c):
    return '#FFFFFF' if lum(c) < .62 else '#14110F'


class Pal:
    def __init__(self, v, style):
        self.style = style
        self.inv = hx(v.get('inv') or v.get('brand'), '#2F6BFF')
        self.bor = hx(v.get('bor'), '#FF6B4A')
        self.bg = hx(v.get('bg'), '#F5F6FA')
        self.ink = hx(v.get('ink'), '#1B1F3B')
        self.surface = hx(v.get('surface'), '#FFFFFF')
        self.dark = lum(self.bg) < .4
        self.line = '#FFFFFF' if self.dark else self.ink


def D(c1, c2):
    return ('<defs><linearGradient id="g1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
            '<linearGradient id="g2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s" stop-opacity=".5"/><stop offset="1" stop-color="%s" stop-opacity="0"/></linearGradient>'
            '<filter id="sh" x="-20%%" y="-20%%" width="140%%" height="150%%"><feDropShadow dx="0" dy="10" stdDeviation="9" flood-color="#000" flood-opacity=".22"/></filter>'
            '<filter id="gl" x="-30%%" y="-30%%" width="160%%" height="160%%"><feGaussianBlur stdDeviation="3.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'
            % (c1, c2, c1, c1))


def panel(p, x, y, w, h, r=22, fill=None, col=None):
    f = fill or p.surface
    col = col or p.inv
    s = p.style
    if s == 'soft':
        return '<g filter="url(#sh)"><rect x="%g" y="%g" width="%g" height="%g" rx="%d" fill="%s"/></g>' % (x, y, w, h, r, f)
    if s == 'geo':
        return ('<rect x="%g" y="%g" width="%g" height="%g" fill="%s"/>' % (x + 9, y + 9, w, h, p.ink) +
                '<rect x="%g" y="%g" width="%g" height="%g" fill="%s" stroke="%s" stroke-width="3"/>' % (x, y, w, h, f, p.ink))
    if s == 'pop':
        return ('<rect x="%g" y="%g" width="%g" height="%g" rx="12" fill="%s"/>' % (x + 8, y + 8, w, h, p.ink) +
                '<rect x="%g" y="%g" width="%g" height="%g" rx="12" fill="%s" stroke="%s" stroke-width="5"/>' % (x, y, w, h, f, p.ink))
    if s == 'line':
        return '<rect x="%g" y="%g" width="%g" height="%g" rx="6" fill="%s" fill-opacity=".04" stroke="%s" stroke-width="2.5"/>' % (x, y, w, h, p.line, p.line)
    return '<rect x="%g" y="%g" width="%g" height="%g" rx="10" fill="%s" fill-opacity=".07" stroke="%s" stroke-width="2.5" filter="url(#gl)"/>' % (x, y, w, h, col, col)


def dcoin(p, x, y, r):
    t = ('<text x="%g" y="%g" font-family="Arial,sans-serif" font-weight="700" font-size="%g" text-anchor="middle" fill="%%s">\u20ac</text>'
         % (x, y + r * .36, r * 1.05))
    s = p.style
    if s in ('soft', 'geo'):
        return coin(x, y, r)
    if s == 'pop':
        return '<circle cx="%g" cy="%g" r="%g" fill="#FFD93D" stroke="%s" stroke-width="4"/>' % (x, y, r, p.ink) + t % p.ink
    col = p.inv if s == 'glow' else p.line
    f = ' filter="url(#gl)"' if s == 'glow' else ''
    return '<g%s><circle cx="%g" cy="%g" r="%g" fill="none" stroke="%s" stroke-width="3"/>' % (f, x, y, r, col) + t % col + '</g>'


def circ(cx, cy, r, col, op, p):
    if p.style in ('line', 'glow'):
        return ''.join('<circle cx="%g" cy="%g" r="%g" fill="none" stroke="%s" stroke-width="2.5" opacity="%g"/>'
                       % (cx, cy, r * k, col, min(op * 3 / (1 + i), .6)) for i, k in enumerate((1, .74, .48)))
    if p.style == 'geo':
        return '<polygon points="%g,%g %g,%g %g,%g %g,%g" fill="%s" opacity="%g"/>' % (cx, cy - r, cx + r, cy, cx, cy + r, cx - r, cy, col, op)
    return '<circle cx="%g" cy="%g" r="%g" fill="%s" opacity="%g"/>' % (cx, cy, r, col, op)
