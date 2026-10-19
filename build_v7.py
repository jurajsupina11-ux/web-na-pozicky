"""Postavi 5 mockupov v7 (mockup-v7-*) a doplni rozcestnik mockup-vyber.html."""
import importlib
import os
import re
import subprocess
import sys

NAMES = ['prism', 'terra', 'skyline', 'sunset', 'ledger']
src = open('static/theme/style.css', encoding='utf-8').read()
cut = src.find('/* ===== DIZAJN v')
BASE_CSS = (src[:cut].rstrip() + '\n\n') if cut > 0 else src
BASE_CSS = re.sub(r"@import url\('https://fonts\.googleapis\.com/css2\?family=Fraunces[^;]*;\n?", '', BASE_CSS)
SKEL = ''.join(open(f, encoding='utf-8').read() + '\n' for f in ('skel_a.css', 'skel_b.css', 'skel_c.css'))

cards = []
for name in NAMES:
    m = importlib.import_module(f'd7_{name}')
    out = f'mockup-v7-{name}'
    subprocess.run([sys.executable, 'build_mockup.py'], env=dict(os.environ, MOCKUP_OUT=out), check=True)
    vars_css = ':root{' + ''.join(f'--{k}:{v};' for k, v in m.VARS.items()) + '}\n'
    font = f"@import url('https://fonts.googleapis.com/css2?family={m.FONTS}&display=swap');\n"
    open(f'{out}/assets/hero-art.svg', 'w', encoding='utf-8').write(m.ART)
    css = font + BASE_CSS + vars_css + SKEL + m.CSS + "\nbody .hero-visual{--vis-img:url('hero-art.svg');}\n"
    open(f'{out}/assets/style.css', 'w', encoding='utf-8').write(css)
    cards.append((out, m.TITLE, m.DESC))

page = open('mockup-vyber.html', encoding='utf-8').read()
page = re.sub(r'<h2>V7.*?</h2>(<a [^>]*mockup-v7-[^<]*<b>.*?</a>)+', '', page, flags=re.S)
items = '<h2>V7 - nove dizajny</h2>' + ''.join(
    f'<a href="{o}/index.html"><b>{t}</b><span>{d}</span></a>' for o, t, d in cards)
page = page.replace('</body>', items + '</body>')
page = page.replace('a:hover{border-color:#111}', 'a:hover{border-color:#111}h2{margin-top:34px}')
open('mockup-vyber.html', 'w', encoding='utf-8').write(page)
print('hotovo', len(cards), 'dizajnov')
