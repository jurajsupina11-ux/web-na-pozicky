"""Programova kontrola domovskej stranky: kontrast nadpisu hero, existencia obrazkov, home-page trieda, zatvorky CSS."""
import os
import re

from apply_home2 import read_vars, resolve
from home_art1 import hx, lum
from home_cfg import CFG


def first_hex(val):
    for m in re.findall(r'#[0-9a-fA-F]{3,8}', val or ''):
        c = hx(m[:7] if len(m) >= 7 else m, '')
        if c:
            return c
    return None


def ratio(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + .05) / (lo + .05)


out = []
for key in CFG:
    d = 'mockup-' + key
    css = open(d + '/assets/style.css', encoding='utf-8').read()
    v = read_vars(css)
    ink = first_hex(resolve(v, 'hero-ink')) or first_hex(resolve(v, 'ink')) or '#000000'
    bg = first_hex(resolve(v, 'hero-bg')) or first_hex(resolve(v, 'bg')) or '#FFFFFF'
    r = ratio(ink, bg)
    imgs = [f for f in ('hero', 'bg', 'inv', 'bor', 'cta', 'stats', 's1', 's2', 's3') if os.path.isfile('%s/assets/img-home-%s.svg' % (d, f))]
    home = 'home-page' in open(d + '/pub-landing.html', encoding='utf-8-sig').read()
    br = css.count('{') == css.count('}')
    flag = []
    if r < 3.5:
        flag.append('NIZKY KONTRAST %.1f (%s na %s)' % (r, ink, bg))
    if len(imgs) != 9:
        flag.append('chyba obrazky %d/9' % len(imgs))
    if not home:
        flag.append('bez home-page')
    if not br:
        flag.append('CSS zatvorky')
    out.append('%-16s %s' % (key, '; '.join(flag) or 'OK (kontrast %.1f)' % r))
open('_chk.txt', 'w', encoding='utf-8').write('\n'.join(out))
