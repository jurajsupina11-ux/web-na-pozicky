"""Nasadi dizajn Mint (mockup-v9-mintfin) do aplikacie: static/theme + trieda home-page na domovskej stranke."""
import glob
import os
import shutil

SRC = 'mockup-v9-mintfin/assets'
DST = 'static/theme'
out = []

# 1) zaloha povodneho style.css (mimo static, aby sa nenasadila)
os.makedirs('_backup_theme', exist_ok=True)
for f in ('style.css', 'hero-art.svg', 'hero-art-b.svg'):
    p = os.path.join(DST, f)
    if os.path.isfile(p):
        shutil.copy2(p, os.path.join('_backup_theme', f))

# 2) CSS bez cache-bust parametrov (v mockupe boli iba v HTML) + obrazky
shutil.copy2(os.path.join(SRC, 'style.css'), os.path.join(DST, 'style.css'))
out.append('style.css skopirovany')
n = 0
for f in glob.glob(os.path.join(SRC, '*.svg')):
    name = os.path.basename(f)
    if name.startswith('logo-'):
        continue  # logo je v aplikacii rovnake
    shutil.copy2(f, os.path.join(DST, name))
    n += 1
out.append('svg skopirovanych: %d' % n)

# 3) body trieda na domovskej stranke
p = 'core/templates/core/landing.html'
b = open(p, 'rb').read()
old = b'<body class="role-neutral">'
new = b'<body class="role-neutral home-page">'
if new in b:
    out.append('landing uz ma home-page')
elif b.count(old) == 1:
    open(p, 'wb').write(b.replace(old, new))
    out.append('landing: home-page pridane')
else:
    out.append('CHYBA: body tag v landing.html nenajdeny (%d)' % b.count(old))

open('_mint.txt', 'w', encoding='utf-8').write('\n'.join(out))
