"""Postavi dve farebne verzie mockupu v5 + vyberovu stranku."""
import os
import subprocess
import sys

PALETTE_B = """
/* ===== Paleta B: Burgundy + Sampanske ===== */
:root{--ink:#2A0A18;--brand:#6B1B3A;--hero:#4A1229;--accent:#D8B98A;--accent-d:#8C6A3F;--accent-rgb:216,185,138;
  --paper:#FBF8F5;--soft:#F3ECE6;--line:#E6DAD0;--muted:#6E5F63;--red:#B3261E;--borrower-bg:#F6EBDC;}
body .hero-visual{background-image:url('hero-art-b.svg');}
body .site-header,body.role-investor .site-header{border-top-color:var(--brand);}
"""

for out, extra in (('mockup-v5-smaragd', ''), ('mockup-v5-burgundy', PALETTE_B)):
    env = dict(os.environ, MOCKUP_OUT=out)
    subprocess.run([sys.executable, 'build_mockup.py'], env=env, check=True)
    if extra:
        with open(f'{out}/assets/style.css', 'a', encoding='utf-8') as fh:
            fh.write(extra)

page = ('<!DOCTYPE html><html lang="sk"><head><meta charset="UTF-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<title>Mockupy - vyber</title><style>body{font-family:system-ui;max-width:760px;'
        'margin:40px auto;padding:0 16px;color:#222}a{display:block;padding:16px 20px;margin:12px 0;'
        'border:1px solid #ccc;border-radius:8px;text-decoration:none;color:#111;font-weight:600}'
        'a span{display:block;font-weight:400;color:#666;font-size:14px}</style></head><body>'
        '<h1>Mockupy - vyber</h1>'
        '<a href="mockup-v5-smaragd/index.html">V5-A Private banking: Smaragd a zlato'
        '<span>slonovina, tmavozelena, zlaty akcent, serifove nadpisy</span></a>'
        '<a href="mockup-v5-burgundy/index.html">V5-B Private banking: Burgundy a sampanske'
        '<span>ten isty dizajn vo vinovej palete</span></a>'
        '<a href="mockup-v4-hravy/index.html">V4 Hravy (ulozeny)'
        '<span>kremova, zlta, koralova, nalepky s tvrdym tienom</span></a>'
        '</body></html>')
open('mockup-vyber.html', 'w', encoding='utf-8').write(page)
print('hotovo')
