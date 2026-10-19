"""Domovska stranka v2: novy dizajn + obrazky vo vsetkych mockupoch. Spustat az po fix_tables.py."""
import os
import re

import home_art2 as A2
import home_art3 as A3
from home_art1 import Pal, deep, gcol, hx, lum, mix
from home_cfg import CFG
from home_css1 import COMMON, FLAVOR, STYLE_VALUES
from home_css2 import LAYOUT, MOBILE, MOBILE_A, MOBILE_D, MOBILE_E

OLD = '/* ===== DOMOVSKA STRANKA ===== */'
NEW = '/* ===== DOMOVSKA v2 ===== */'
SEL = {'@P': 'body.home-page .picker-card', '@G': 'body.home-page .picker-grid', '@CTA': 'body.home-page .cta-band'}


def read_vars(css):
    v = {}
    for blk in re.findall(r':root\s*\{([^}]*)\}', css):
        for k, val in re.findall(r'--([\w-]+)\s*:\s*([^;]+);', blk):
            v[k] = val.strip()
    return v


def resolve(v, name, depth=0):
    x = v.get(name, '')
    m = re.match(r'var\(--([\w-]+)', x)
    if m and depth < 4:
        return resolve(v, m.group(1), depth + 1)
    return x


def rgba(c, a):
    c = hx(c, '#888888').lstrip('#')
    return 'rgba(%d,%d,%d,%s)' % (int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16), a)


def pick(v, *names):
    for n in names:
        x = hx(resolve(v, n), '')
        if x:
            return x
    return None


def tokens(v, style):
    rv = {k: resolve(v, k) for k in v}
    rv['inv'] = pick(v, 'inv', 'investor', 'brand', 'violet') or '#2F6BFF'
    rv['bor'] = pick(v, 'bor', 'borrower') or '#FF6B4A'
    rv['bg'] = pick(v, 'bg') or '#F5F6FA'
    rv['ink'] = pick(v, 'ink') or '#1B1F3B'
    p = Pal(rv, style)
    sur = pick(v, 'surface') or ('#FFFFFF' if not p.dark else mix(p.bg, '#FFFFFF', .08))
    rb = resolve(v, 'rb')
    rad = resolve(v, 'radius')
    t = {
        'BG': p.bg, 'SUR': sur, 'INK': p.ink, 'MUT': pick(v, 'muted') or mix(p.ink, p.bg, .4),
        'INV': p.inv, 'BOR': p.bor, 'INVT': gcol(p.inv), 'BORT': gcol(p.bor),
        'INVD': deep(p.inv), 'BORD': deep(p.bor),
        'RB': rb if re.fullmatch(r'\d+px', rb or '') else '999px',
        'INVA3': rgba(p.inv, .3), 'INVA7': rgba(p.inv, .7), 'INVA14': rgba(p.inv, .14),
        'BORA3': rgba(p.bor, .3), 'BORA7': rgba(p.bor, .7), 'BORA14': rgba(p.bor, .14),
        'INKA5': rgba(p.ink, .5), 'SURA': rgba(sur, .06),
        'CR': rad if re.fullmatch(r'\d+px', rad or '') and int(rad[:-2]) >= 14 else '24px',
    }
    return p, t


def fill(s, t):
    for _ in range(4):
        for k in sorted(t, key=len, reverse=True):
            s = s.replace('{' + k + '}', t[k])
    for k, val in SEL.items():
        s = s.replace(k, val)
    return s


def build_css(style, lay, t):
    st = dict(STYLE_VALUES[style])
    t = dict(t)
    t.update(st)
    t['FLAV'] = FLAVOR[style]
    css = COMMON + LAYOUT[lay] + MOBILE + {'A': MOBILE_A, 'D': MOBILE_D, 'E': MOBILE_E}.get(lay, '')
    css = css.replace('{FLAV}', t['FLAV'])
    return fill(css, t)


def main():
    n = 0
    for key, (style, lay) in CFG.items():
        d = 'mockup-' + key
        sp = os.path.join(d, 'assets', 'style.css')
        page = os.path.join(d, 'pub-landing.html')
        if not (os.path.isfile(sp) and os.path.isfile(page)):
            print('preskocene', key)
            continue
        s = open(sp, encoding='utf-8').read()
        v = read_vars(s)
        p, t = tokens(v, style)
        cut = [s.index(m) for m in (OLD, NEW) if m in s]
        if cut:
            s = s[:min(cut)].rstrip() + '\n'
        open(sp, 'w', encoding='utf-8').write(s + '\n' + NEW + '\n' + build_css(style, lay, t))
        files = {'hero': A2.hero(p), 'bg': A2.bg2(p), 'inv': A3.inv_card(p), 'bor': A3.bor_card(p),
                 'cta': A3.cta(p), 'stats': A3.stats(p), 's1': A2.step_icon(p, 1), 's2': A2.step_icon(p, 2), 's3': A2.step_icon(p, 3)}
        for name, data in files.items():
            open(os.path.join(d, 'assets', 'img-home-%s.svg' % name), 'w', encoding='utf-8').write(data)
        h = open(page, encoding='utf-8-sig').read()
        if 'home-page' not in h:
            if re.search(r'<body[^>]*class="', h):
                h = re.sub(r'(<body[^>]*class=")', r'\1home-page ', h, count=1)
            else:
                h = h.replace('<body', '<body class="home-page"', 1)
            open(page, 'w', encoding='utf-8').write(h)
        n += 1
    print('hotovo', n, 'z', len(CFG))


main()
