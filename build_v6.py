"""Postavi 5 mockupov v6 (kazdy samostatny priecinok) + vyberovu stranku."""
import importlib
import os
import re
import subprocess
import sys

NAMES = ['aurora', 'swiss', 'zen', 'ocean', 'noir']
BASE_CSS = open('static/theme/style.css', encoding='utf-8').read()
cut = BASE_CSS.find('/* ===== DIZAJN v')
BASE_CSS = BASE_CSS[:cut].rstrip() + '\n\n' if cut > 0 else BASE_CSS
BASE_CSS = re.sub(r"@import url\('https://fonts\.googleapis\.com/css2\?family=Fraunces[^;]*;\n?", '', BASE_CSS)
SKEL = ''.join(open(f, encoding='utf-8').read() + '\n' for f in ('skel_a.css', 'skel_b.css', 'skel_c.css'))

cards = []
for name in NAMES:
    m = importlib.import_module(f'd6_{name}')
    out = f'mockup-v6-{name}'
    subprocess.run([sys.executable, 'build_mockup.py'], env=dict(os.environ, MOCKUP_OUT=out), check=True)
    vars_css = ':root{' + ''.join(f'--{k}:{v};' for k, v in m.VARS.items()) + '}\n'
    font = f"@import url('https://fonts.googleapis.com/css2?family={m.FONTS}&display=swap');\n"
    open(f'{out}/assets/hero-art.svg', 'w', encoding='utf-8').write(m.ART)
    css = font + BASE_CSS + vars_css + SKEL + m.CSS
    css += "\nbody .hero-visual{--vis-img:url('hero-art.svg');}\n"
    open(f'{out}/assets/style.css', 'w', encoding='utf-8').write(css)
    cards.append((out, m.TITLE, m.DESC))

items = ''.join(
    f'<a href="{o}/index.html"><b>{t}</b><span>{d}</span></a>' for o, t, d in cards)
items += ('<a href="mockup-v5-smaragd/index.html"><b>V5-A Private banking - smaragd</b>'
          '<span>ulozeny, slonovina + zlato</span></a>'
          '<a href="mockup-v5-burgundy/index.html"><b>V5-B Private banking - burgundy</b>'
          '<span>ulozeny</span></a>'
          '<a href="mockup-v4-hravy/index.html"><b>V4 Hravy</b><span>ulozeny</span></a>')
style = ('body{font-family:system-ui;max-width:820px;margin:40px auto;padding:0 16px;color:#222}'
         'a{display:block;padding:16px 20px;margin:12px 0;border:1px solid #ccc;border-radius:10px;'
         'text-decoration:none;color:#111}a b{display:block;font-size:17px}'
         'a span{color:#666;font-size:14px}a:hover{border-color:#111}')
open('mockup-vyber.html', 'w', encoding='utf-8').write(
    '<!DOCTYPE html><html lang="sk"><head><meta charset="UTF-8">'
    '<meta name="viewport" content="width=device-width, initial-scale=1">'
    f'<title>Mockupy - vyber</title><style>{style}</style></head><body>'
    f'<h1>Mockupy - vyber</h1>{items}</body></html>')
print('hotovo', len(cards), 'dizajnov')
