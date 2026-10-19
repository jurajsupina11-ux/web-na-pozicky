from a9_common import (bank_card, bars, card, coin, defs, donut, grid_dots, icon_set, line_chart, pill, shield, svg, wave)


def neobank():
    c1, c2 = '#5B5BF0', '#8B5CF6'
    b = defs(c1, c2) + '<circle cx="270" cy="210" r="190" fill="url(#g1)" opacity=".12"/>'
    b += card(110, 90, 300, 230, '#fff', 24)
    b += '<text x="136" y="130" font-family="Arial" font-size="14" fill="#7A82A0">Celkový majetok</text>'
    b += '<text x="136" y="170" font-family="Arial" font-weight="700" font-size="34" fill="#1B1F3B">12 480 €</text>'
    b += '<rect x="318" y="108" width="74" height="26" rx="13" fill="#E3F8EE"/><text x="355" y="126" font-family="Arial" font-size="13" font-weight="700" fill="#12935B" text-anchor="middle">+8,4 %</text>'
    b += line_chart(136, 190, 248, 100, c1)
    b += bank_card(40, 250, 190, 118, c1, c2, -8) + bank_card(250, 300, 190, 112, '#FF7A59', '#FFB347', 7)
    b += coin(450, 100, 28) + coin(70, 120, 20)
    return svg(520, 420, b)


def private_bank():
    b = defs('#0F2A5C', '#1E4A8F')
    b += '<rect x="60" y="300" width="400" height="14" fill="#C9A24B"/><rect x="80" y="314" width="360" height="12" fill="#A8832F"/>'
    b += '<path d="M60 130 260 40 460 130z" fill="#0F2A5C"/><rect x="60" y="130" width="400" height="12" fill="#C9A24B"/>'
    for i in range(6):
        b += '<rect x="%d" y="150" width="34" height="150" rx="3" fill="#fff"/><rect x="%d" y="150" width="8" height="150" fill="#E6E9F2"/>' % (90 + i * 62, 90 + i * 62 + 26)
    b += '<circle cx="260" cy="88" r="22" fill="#C9A24B"/><text x="260" y="97" font-family="Georgia" font-size="26" font-weight="700" fill="#0F2A5C" text-anchor="middle">€</text>'
    for k, (x, n) in enumerate(((40, 4), (440, 6))):
        for j in range(n):
            b += '<ellipse cx="%d" cy="%d" rx="34" ry="10" fill="#E3B84F"/><rect x="%d" y="%d" width="68" height="12" fill="#C9A24B"/>' % (x, 380 - j * 12, x - 34, 380 - j * 12)
    b += '<g filter="url(#sh)"></g>'
    return svg(520, 420, b)


def mint():
    c1, c2 = '#10B981', '#34D399'
    b = defs(c1, c2) + '<circle cx="260" cy="210" r="180" fill="#D1FAE5"/>'
    b += card(70, 70, 210, 200, '#fff', 26) + donut(175, 170, 50, [(60, c1), (25, '#FBBF24'), (15, '#F472B6')], 22)
    b += '<text x="175" y="176" font-family="Arial" font-weight="700" font-size="22" fill="#064E3B" text-anchor="middle">60 %</text>'
    b += pill(100, 244, 120, '#A7F3D0')
    b += card(250, 150, 210, 190, '#fff', 26) + bars(276, 180, 158, 120, [c1, '#6EE7B7'], [.4, .6, .5, .8, .7, 1.0], 9)
    b += coin(430, 90, 34, '#FDE68A', '#F59E0B') + coin(90, 330, 26, '#FDE68A', '#F59E0B')
    b += shield(380, 370, .6, c1)
    return svg(520, 420, b)


def trading():
    c1 = '#C6FF3D'
    b = defs(c1, '#22D3EE') + grid_dots(520, 420, 28, '#fff', .12, 1.4)
    b += '<rect x="30" y="50" width="460" height="300" rx="18" fill="#0E1417" stroke="#23323A" stroke-width="2"/>'
    for i in range(14):
        h = 30 + (i * 37) % 90
        up = (i * 5) % 3 != 0
        col = c1 if up else '#FF4D8D'
        y = 260 - i * 7 - h / 2 + ((i * 13) % 30)
        b += '<path d="M%d %d v%d" stroke="%s" stroke-width="3"/><rect x="%d" y="%d" width="18" height="%d" rx="3" fill="%s"/>' % (62 + i * 31, y - 14, h + 28, col, 53 + i * 31, y, h, col)
    b += line_chart(50, 90, 420, 200, '#22D3EE', [.8, .7, .75, .5, .55, .35, .3, .15], False, 3)
    b += '<text x="52" y="82" font-family="monospace" font-size="16" fill="#C6FF3D">+22,1 % p.a.</text>'
    b += coin(450, 360, 30, '#C6FF3D', '#2B3A00') + coin(60, 372, 20, '#22D3EE', '#00323B')
    return svg(520, 420, b)


def pastel():
    c1, c2 = '#38BDF8', '#818CF8'
    b = defs(c1, c2) + '<circle cx="140" cy="130" r="110" fill="#FDE2E4"/><circle cx="400" cy="320" r="120" fill="#DCEEFB"/><circle cx="410" cy="100" r="60" fill="#FFF1C9"/>'
    b += card(80, 80, 360, 250, '#fff', 22)
    for i, (w, col) in enumerate(((220, c1), (160, '#FDA4AF'), (190, '#FCD34D'))):
        b += '<circle cx="118" cy="%d" r="14" fill="%s"/>' % (130 + i * 48, col) + pill(146, 124 + i * 48, w, '#E5E7EB') + pill(146, 124 + i * 48, w * .62, col)
    b += line_chart(110, 262, 300, 50, c2, [.7, .5, .6, .3, .4, .1])
    b += bank_card(300, 30, 150, 92, c1, c2, 6) + coin(70, 350, 30) + coin(460, 360, 22)
    return svg(520, 420, b)


def extras(kind):
    pal = {'neobank': ('#5B5BF0', '#8B5CF6', '#FFB347'), 'bank': ('#0F2A5C', '#1E4A8F', '#C9A24B'),
           'mint': ('#10B981', '#34D399', '#FBBF24'), 'trading': ('#C6FF3D', '#22D3EE', '#FF4D8D'),
           'pastel': ('#38BDF8', '#818CF8', '#FCD34D')}[kind]
    ex = icon_set(*pal)
    ex['wave'] = svg(1400, 200, wave(1400, 200, pal[0], .35, 30, 2) + wave(1400, 200, pal[1], .55, 24, 3, 1.5))
    ex['dots'] = svg(400, 300, grid_dots(400, 300, 26, pal[0], .35, 2))
    ex['chart'] = svg(600, 260, defs(pal[0], pal[1]) + line_chart(10, 20, 580, 220, pal[0], None, True, 5))
    ex['coins'] = svg(300, 220, coin(80, 120, 50) + coin(180, 90, 36) + coin(230, 160, 44, '#FDE68A', '#F59E0B'))
    return ex
