"""Vytvori mockup-mobil.html: prehliadac vsetkych mockupov a ich stranok v ramceku telefonu (390x844)."""
import glob
import json
import os
import re

data = {}
titles = {}
vyber = open('mockup-vyber.html', encoding='utf-8').read()
for m in re.finditer(r'<a href="(mockup-[^/"]+)/index.html"><b>(.*?)</b>', vyber):
    titles[m.group(1)] = m.group(2)
for d in sorted(glob.glob('mockup-*/')):
    d = d.rstrip('/\\')
    pages = sorted(os.path.basename(p) for p in glob.glob(d + '/*.html'))
    if pages:
        data[d] = {'title': titles.get(d, d), 'pages': pages}

HTML = """<!DOCTYPE html><html lang="sk"><head><meta charset="utf-8"><title>Mobilny nahlad mockupov</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box}body{margin:0;font:14px system-ui,sans-serif;background:#e9ebf0;color:#111;display:flex;min-height:100vh}
aside{width:300px;background:#fff;border-right:1px solid #ccd;padding:16px;overflow:auto;height:100vh;position:sticky;top:0}
aside h1{font-size:16px;margin:0 0 10px}label{display:block;font-weight:600;margin:12px 0 4px}
select{width:100%;padding:8px;font-size:14px}.nav{display:flex;gap:6px;margin-top:10px}
button{flex:1;padding:8px;font-size:14px;cursor:pointer}a{color:#06c}.grp{margin:10px 0 0;font-size:12px;color:#555}
main{flex:1;display:flex;justify-content:center;align-items:flex-start;padding:24px;overflow:auto}
.phone{width:414px;height:868px;border:12px solid #111;border-radius:48px;background:#111;box-shadow:0 20px 50px rgba(0,0,0,.35);overflow:hidden;flex:none}
iframe{width:100%;height:100%;border:0;background:#fff;border-radius:34px}
</style></head><body>
<aside><h1>Mobilny nahlad (390 px)</h1>
<label>Dizajn</label><select id="d"></select>
<label>Stranka</label><select id="p"></select>
<div class="nav"><button id="prev">&larr; Predosla</button><button id="next">Dalsia &rarr;</button></div>
<p class="grp">Skupiny: pub = verejne, inv = investor, bor = dlznik, adm = admin-ukazky.</p>
<p><a id="open" target="_blank">Otvorit v novom okne</a> &middot; <a href="mockup-vyber.html">Spat na vyber</a></p></aside>
<main><div class="phone"><iframe id="f" title="mobil"></iframe></div></main>
<script>
const DATA=__DATA__;const d=document.getElementById('d'),p=document.getElementById('p'),f=document.getElementById('f'),o=document.getElementById('open');
Object.keys(DATA).forEach(k=>d.add(new Option(DATA[k].title,k)));
function fillPages(keep){p.innerHTML='';DATA[d.value].pages.forEach(x=>p.add(new Option(x.replace('.html',''),x)));
 if(keep&&DATA[d.value].pages.includes(keep))p.value=keep;else p.value=DATA[d.value].pages.includes('pub-investori.html')?'pub-investori.html':DATA[d.value].pages[0];}
function show(){const u=d.value+'/'+p.value;f.src=u;o.href=u;history.replaceState(null,'','?d='+d.value+'&p='+p.value);}
const q=new URLSearchParams(location.search);if(q.get('d')&&DATA[q.get('d')])d.value=q.get('d');
fillPages(q.get('p'));d.onchange=()=>{fillPages(p.value);show()};p.onchange=show;
function step(n){const i=p.selectedIndex+n;if(i>=0&&i<p.options.length){p.selectedIndex=i;show()}}
document.getElementById('prev').onclick=()=>step(-1);document.getElementById('next').onclick=()=>step(1);show();
</script></body></html>"""
open('mockup-mobil.html', 'w', encoding='utf-8').write(HTML.replace('__DATA__', json.dumps(data, ensure_ascii=False)))

page = open('mockup-vyber.html', encoding='utf-8').read()
if 'mockup-mobil.html' not in page:
    page = page.replace('<body>', '<body><p style="margin:12px"><a href="mockup-mobil.html"><b>&#128241; Mobilny nahlad vsetkych dizajnov a podstranok</b></a></p>', 1)
    open('mockup-vyber.html', 'w', encoding='utf-8').write(page)
print('hotovo', len(data), 'dizajnov,', sum(len(v['pages']) for v in data.values()), 'stranok')

