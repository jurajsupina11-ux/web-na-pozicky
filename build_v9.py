"""Postavi financne mockupy v9 (mockup-v9-*). Pouzitie: python build_v9.py [meno ...]"""
import os
import re
import subprocess
import sys

import d9_defs2  # noqa: F401  (doplni DESIGNS)
from d9_defs import DESIGNS

NAMES = [n for n in sys.argv[1:] if n in DESIGNS] or list(DESIGNS)
src = open('static/theme/style.css', encoding='utf-8').read()
cut = src.find('/* ===== DIZAJN v')
BASE_CSS = (src[:cut].rstrip() + '\n\n') if cut > 0 else src
BASE_CSS = re.sub(r"@import url\('https://fonts\.googleapis\.com/css2\?family=Fraunces[^;]*;\n?", '', BASE_CSS)
SKEL = ''.join(open(f, encoding='utf-8').read() + '\n' for f in ('skel_a.css', 'skel_b.css', 'skel_c.css'))
NAVFIX = ("body .logo-full-img{height:70px;}body{--nav-gap:12px;}body .main-nav a{font-size:13px;padding:8px 2px;}"
          "body .main-nav .btn-primary{padding:11px 18px;}\n")

for name in NAMES:
    m = DESIGNS[name]
    out = f'mockup-v9-{name}'
    subprocess.run([sys.executable, 'build_mockup.py'], env=dict(os.environ, MOCKUP_OUT=out), check=True)
    vars_css = ':root{' + ''.join(f'--{k}:{v};' for k, v in m['vars'].items()) + '}\n'
    font = f"@import url('https://fonts.googleapis.com/css2?family={m['fonts']}&display=swap');\n"
    open(f'{out}/assets/hero-art.svg', 'w', encoding='utf-8').write(m['art'])
    for key, data in m['extra'].items():
        open(f'{out}/assets/img-{key}.svg', 'w', encoding='utf-8').write(data)
    css = font + BASE_CSS + vars_css + SKEL + m['css'] + NAVFIX + "\nbody .hero-visual{--vis-img:url('hero-art.svg');}\n"
    open(f'{out}/assets/style.css', 'w', encoding='utf-8').write(css)

page = open('mockup-vyber.html', encoding='utf-8').read()
page = re.sub(r'<h2>V9.*?</h2>(<a [^>]*mockup-v9-[^<]*<b>.*?</a>)+', '', page, flags=re.S)
items = '<h2>V9 - financne a moderne dizajny</h2>' + ''.join(
    f'<a href="mockup-v9-{n}/index.html"><b>{DESIGNS[n]["title"]}</b><span>{DESIGNS[n]["desc"]}</span></a>' for n in DESIGNS)
page = page.replace('</body>', items + '</body>')
open('mockup-vyber.html', 'w', encoding='utf-8').write(page)
print('hotovo', NAMES)
