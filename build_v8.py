"""Postavi mockupy v8 (mockup-v8-*) s viacerymi obrazkami a doplni rozcestnik mockup-vyber.html.
Pouzitie: python build_v8.py [meno ...]  (bez argumentov postavi vsetky)"""
import importlib
import os
import re
import subprocess
import sys

ALL = ['blueprint', 'memphis', 'papercut', 'cosmos', 'gazette']
NAMES = [n for n in sys.argv[1:] if n in ALL] or ALL
src = open('static/theme/style.css', encoding='utf-8').read()
cut = src.find('/* ===== DIZAJN v')
BASE_CSS = (src[:cut].rstrip() + '\n\n') if cut > 0 else src
BASE_CSS = re.sub(r"@import url\('https://fonts\.googleapis\.com/css2\?family=Fraunces[^;]*;\n?", '', BASE_CSS)
SKEL = ''.join(open(f, encoding='utf-8').read() + '\n' for f in ('skel_a.css', 'skel_b.css', 'skel_c.css'))


def build(name):
    m = importlib.import_module(f'd8_{name}')
    out = f'mockup-v8-{name}'
    subprocess.run([sys.executable, 'build_mockup.py'], env=dict(os.environ, MOCKUP_OUT=out), check=True)
    vars_css = ':root{' + ''.join(f'--{k}:{v};' for k, v in m.VARS.items()) + '}\n'
    font = f"@import url('https://fonts.googleapis.com/css2?family={m.FONTS}&display=swap');\n"
    open(f'{out}/assets/hero-art.svg', 'w', encoding='utf-8').write(m.ART)
    for key, data in m.EXTRA.items():
        open(f'{out}/assets/img-{key}.svg', 'w', encoding='utf-8').write(data)
    css = font + BASE_CSS + vars_css + SKEL + m.CSS + "\nbody .hero-visual{--vis-img:url('hero-art.svg');}\n"
    open(f'{out}/assets/style.css', 'w', encoding='utf-8').write(css)
    return out, m.TITLE, m.DESC


done = {n: build(n) for n in NAMES}
cards = [done[n] if n in done else (f'mockup-v8-{n}', None, None) for n in ALL]

page = open('mockup-vyber.html', encoding='utf-8').read()
old = {}
for mt in re.finditer(r'<a href="(mockup-v8-[^/]*)/index.html"><b>(.*?)</b><span>(.*?)</span></a>', page, flags=re.S):
    old[mt.group(1)] = (mt.group(1), mt.group(2), mt.group(3))
page = re.sub(r'<h2>V8.*?</h2>(<a [^>]*mockup-v8-[^<]*<b>.*?</a>)+', '', page, flags=re.S)
cards = [c if c[1] else old.get(c[0]) for c in cards]
items = '<h2>V8 - nove dizajny (viac obrazkov)</h2>' + ''.join(
    f'<a href="{o}/index.html"><b>{t}</b><span>{d}</span></a>' for o, t, d in filter(None, cards))
page = page.replace('</body>', items + '</body>')
open('mockup-vyber.html', 'w', encoding='utf-8').write(page)
print('hotovo', list(done))
