from a9_common import coin, svg

LEAF = 'M0 0C25-38 85-38 115 0C85 38 25 38 0 0Z'


def leaf(x, y, rot, s, col):
    return ('<g transform="translate(%g %g) rotate(%g) scale(%g)"><path d="%s" fill="%s"/>'
            '<path d="M0 0H108" stroke="#1F4D38" stroke-width="3" opacity=".6"/></g>' % (x, y, rot, s, LEAF, col))


def botanical_hero():
    b = '<circle cx="260" cy="210" r="185" fill="#E6F0DF"/>'
    b += '<path d="M260 360C250 300 285 250 260 190 240 140 270 100 262 70" stroke="#2F6B4F" stroke-width="9" fill="none" stroke-linecap="round"/>'
    cols = ('#2F6B4F', '#3F8A62', '#5BAA7A')
    pts = ((257, 320, -150, .9), (262, 300, -20, .9), (266, 250, -160, .8), (262, 230, -15, .85),
           (258, 190, -155, .75), (260, 170, -25, .75), (262, 120, -145, .6), (262, 110, -35, .6))
    for i, p in enumerate(pts):
        b += leaf(p[0], p[1], p[2], p[3], cols[i % 3])
    b += leaf(150, 380, -60, .5, '#5BAA7A') + leaf(380, 380, -120, .5, '#3F8A62')
    b += '<path d="M200 360H320L305 410H215Z" fill="#B8553A"/><rect x="195" y="348" width="130" height="18" rx="4" fill="#C96B4E"/>'
    b += coin(262, 58, 26) + coin(150, 230, 17) + coin(380, 190, 20)
    b += '<path d="M150 247V270M380 210V232" stroke="#2F6B4F" stroke-width="3"/>'
    return svg(520, 420, b)


def watercolor_hero():
    b = ('<defs><filter id="wb" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="14"/></filter>'
         '<filter id="wb2"><feGaussianBlur stdDeviation="2.5"/></filter></defs>')
    blobs = ((170, 150, 120, '#4FC3C0', .7), (340, 130, 100, '#F5C26B', .8), (300, 280, 130, '#E98AA8', .6),
             (140, 300, 90, '#8E9CE8', .6), (410, 300, 80, '#4FC3C0', .5))
    b += '<g filter="url(#wb)">' + ''.join('<circle cx="%d" cy="%d" r="%d" fill="%s" opacity="%s"/>' % x for x in blobs) + '</g>'
    b += '<g filter="url(#wb2)" fill="none" stroke-width="3" opacity=".45">'
    b += ''.join('<circle cx="%d" cy="%d" r="%d" stroke="%s"/>' % (x[0], x[1], x[2] - 18, x[3]) for x in blobs) + '</g>'
    b += '<polyline points="60,330 140,290 200,305 270,230 340,250 420,150 470,120" fill="none" stroke="#2B3A55" stroke-width="6" '
    b += 'stroke-linecap="round" stroke-linejoin="round" opacity=".85"/>'
    for x, y in ((140, 290), (270, 230), (420, 150)):
        b += '<circle cx="%d" cy="%d" r="9" fill="#FBF7F2" stroke="#2B3A55" stroke-width="4"/>' % (x, y)
    return svg(520, 420, b + coin(110, 110, 30, '#F5C26B', '#C9871A') + coin(440, 360, 24, '#F5C26B', '#C9871A'))


def sprite(rows, pal, x, y, s):
    out = ''
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch in pal:
                out += '<rect x="%g" y="%g" width="%g" height="%g" fill="%s"/>' % (x + i * s, y + j * s, s + .4, s + .4, pal[ch])
    return out


COIN = ['..yyyy..', '.yYYYYy.', 'yYYoYYYy', 'yYoYYYYy', 'yYoYYYYy', 'yYYYYYYy', '.yYYYYy.', '..yyyy..']
CLOUD = ['...ww.....', '..wwww.ww.', '.wwwwwwwww', 'wwwwwwwwww']
COIN_PAL = {'y': '#C9810F', 'Y': '#FFD93D', 'o': '#FFF3A8'}


def pixel_hero():
    b = ''
    for i in range(18):
        b += '<rect x="%d" y="%d" width="6" height="6" fill="#F4F4F4" opacity=".7"/>' % ((i * 83) % 500, (i * 47) % 150)
    b += sprite(CLOUD, {'w': '#566C86'}, 30, 70, 8) + sprite(CLOUD, {'w': '#566C86'}, 380, 40, 6)
    for i in range(6):
        h = 40 + i * 40
        x = 90 + i * 55
        b += '<rect x="%d" y="%d" width="44" height="%d" fill="#38B764"/><rect x="%d" y="%d" width="44" height="8" fill="#A7F070"/>' % (x, 372 - h, h, x, 372 - h)
        b += '<rect x="%d" y="%d" width="8" height="%d" fill="#257179"/>' % (x + 36, 380 - h, h - 8)
    b += sprite(COIN, COIN_PAL, 330, 70, 7) + sprite(COIN, COIN_PAL, 100, 200, 5)
    for i in range(13):
        b += '<rect x="%d" y="372" width="40" height="40" fill="#B4783C"/><rect x="%d" y="372" width="40" height="10" fill="#5DA02F"/>' % (i * 40 - 10, i * 40 - 10)
        b += '<rect x="%d" y="394" width="10" height="10" fill="#7A4A1F"/>' % (i * 40 + 8)
    return svg(520, 420, b)
