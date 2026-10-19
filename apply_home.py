"""Domovska stranka (pub-landing.html) podla stylu kazdeho mockupu.
Prida body.home-page a blok CSS na koniec assets/style.css. Idempotentne."""
import glob
import os
import re

from home_v10 import HOME

MARK = '/* ===== DOMOVSKA STRANKA ===== */'
TOK = {'@H': 'body.home-page .picker-hero', '@C': 'body.home-page .picker-card', '@S': 'body.home-page .step-card',
       '@N': 'body.home-page .step-num', '@G': 'body.home-page .steps-grid', '@T': 'body.home-page .stats-band',
       '@B': 'body.home-page .stats-grid b', '@A': 'body.home-page .cta-band', '@I': 'body.home-page .picker-icon'}
MOBILE = """
@media(max-width:700px){
  body.home-page .picker-hero h1{font-size:38px;line-height:1.1;}
  body.home-page .picker-hero .picker-grid{gap:20px;border-width:0;}
  body.home-page .picker-card{transform:none !important;border-right:0 !important;margin-bottom:0;padding:34px 24px;}
  body.home-page .steps-grid{gap:16px;}
  body.home-page .step-card{border-right:0 !important;transform:none !important;}
  body.home-page .stats-band{border-radius:28px;padding:50px 0;}
  body.home-page .stats-grid b{font-size:34px;}
  body.home-page .cta-band{padding-bottom:70px;}
}
"""


def conv(css):
    for k in sorted(TOK, key=len, reverse=True):
        css = css.replace(k, TOK[k])
    return css


n = 0
for key, css in HOME.items():
    d = 'mockup-' + key
    if not os.path.isdir(d):
        print('chyba priecinok', d)
        continue
    page = os.path.join(d, 'pub-landing.html')
    h = open(page, encoding='utf-8-sig').read()
    if 'home-page' not in h:
        if re.search(r'<body[^>]*class="', h):
            h = re.sub(r'(<body[^>]*class=")', r'\1home-page ', h, count=1)
        else:
            h = h.replace('<body', '<body class="home-page"', 1)
        open(page, 'w', encoding='utf-8').write(h)
    sp = os.path.join(d, 'assets', 'style.css')
    s = open(sp, encoding='utf-8').read()
    if MARK in s:
        s = s[:s.index(MARK)].rstrip() + '\n'
    open(sp, 'w', encoding='utf-8').write(s + '\n' + MARK + '\n' + conv(css) + MOBILE)
    n += 1
print('upravenych', n, 'z', len(HOME))
