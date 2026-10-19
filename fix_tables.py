"""Prida mobilnu opravu tabuliek do skel_c.css a do vsetkych zostavenych mockup-*/assets/style.css."""
import glob

MARK = '/* ===== MOBIL: tabulky ===== */'
CSS = MARK + """
@media(max-width:700px){
  body table{display:block;width:100%;max-width:100%;overflow-x:auto;white-space:nowrap;-webkit-overflow-scrolling:touch;border-collapse:collapse;}
  body table th,body table td{white-space:nowrap;padding:10px 9px;word-break:normal;overflow-wrap:normal;hyphens:none;vertical-align:middle;}
  body table th{font-size:10.5px;letter-spacing:.03em;}\n  body table td{font-size:12.5px;}\n  body table{background:linear-gradient(to right,var(--surface,#fff) 30%,rgba(255,255,255,0)) left center/40px 100% no-repeat local,linear-gradient(to left,var(--surface,#fff) 30%,rgba(255,255,255,0)) right center/40px 100% no-repeat local,radial-gradient(farthest-side at 0 50%,rgba(0,0,0,.18),rgba(0,0,0,0)) left center/12px 100% no-repeat scroll,radial-gradient(farthest-side at 100% 50%,rgba(0,0,0,.18),rgba(0,0,0,0)) right center/12px 100% no-repeat scroll;}
  body table td .badge,body table td [class*="badge"],body table td [class*="status"],body table td [class*="pill"]{white-space:nowrap;display:inline-block;width:auto;height:auto;line-height:1.3;padding:4px 12px;word-break:normal;}
  body table td .btn{white-space:nowrap;width:auto;padding:8px 14px;border-radius:999px;}
  body .card:has(table),body .table-wrap,body .table-responsive{overflow-x:auto;}
  body .card h2,body .card h3{overflow-wrap:break-word;}
  body .section-title-row,body .card-head{flex-wrap:wrap;gap:6px 12px;}\n  body .dash-shell{grid-template-columns:minmax(0,1fr);gap:16px;}\n  body .dash-shell>*,body .dash-main,body .dash-content{min-width:0;max-width:100%;}\n  body .dash-top{min-width:0;}\n  body .dash-top .btn,body .toprow .btn{width:100%;max-width:100%;box-sizing:border-box;}\n  body .btn,body .wallet-card,body .card{max-width:100%;box-sizing:border-box;}\n  body .btn{white-space:normal;}
}
"""

targets = ['skel_c.css'] + glob.glob('mockup-*/assets/style.css')
n = 0
for t in targets:
    s = open(t, encoding='utf-8').read()
    if MARK in s:
        s = s[:s.index(MARK)].rstrip() + '\n\n'
    elif not s.endswith('\n'):
        s += '\n'
    # stare pravidlo z predosleho opravenia nahradime novym
    s = s.replace('  body table{display:block;overflow-x:auto;max-width:100%;}\n', '')
    open(t, 'w', encoding='utf-8').write(s + CSS)
    n += 1
print('upravenych', n)


