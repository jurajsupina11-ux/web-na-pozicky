from home_v6 import HOME

HOME['v7-prism'] = """
@C{clip-path:polygon(0 0,100% 0,100% 88%,92% 100%,0 100%);border:0;}@C.role-card-investor{transform:translateY(-12px);}
@S{clip-path:polygon(0 0,100% 0,100% 100%,8% 100%,0 92%);border:0;}
@T{clip-path:polygon(0 14%,100% 0,100% 86%,0 100%);padding:100px 0;border-radius:0;}
@A{clip-path:polygon(0 0,100% 9%,100% 100%,0 100%);padding-top:120px;}
"""

HOME['v7-terra'] = """
@C{border-radius:220px 220px 28px 28px;padding-top:70px;text-align:center;}@I .ic{margin:0 auto;border-radius:50%;}
@S{border-radius:140px 140px 22px 22px;text-align:center;padding-top:44px;}@N{margin:0 auto 14px;}
@T{border-radius:200px;padding:60px 40px;margin:0 16px;}@A{border-radius:36px 36px 240px 240px;padding-bottom:120px;}
"""

HOME['v7-skyline'] = """
@C{clip-path:polygon(0 0,calc(100% - 30px) 0,100% 30px,100% 100%,30px 100%,0 calc(100% - 30px));border:0;box-shadow:none;}
@C.role-card-investor{background:linear-gradient(160deg,var(--surface),rgba(0,200,255,.12));}
@C.role-card-borrower{background:linear-gradient(160deg,var(--surface),rgba(255,0,170,.12));}
@S{clip-path:polygon(0 0,calc(100% - 22px) 0,100% 22px,100% 100%,0 100%);border:0;}
@N{border-radius:0;clip-path:polygon(0 0,100% 0,100% 70%,70% 100%,0 100%);}
@T{border-radius:0;clip-path:polygon(0 0,100% 0,100% 70%,96% 100%,0 100%);}
@A{clip-path:polygon(0 0,100% 0,100% 100%,3% 100%,0 85%);border-radius:0;}
"""

HOME['v7-sunset'] = """
@H{padding-bottom:130px;}
@C{border-radius:44px;background:linear-gradient(160deg,var(--surface),rgba(255,160,120,.18));}
@S{border-radius:50px 50px 50px 8px;}@N{box-shadow:0 10px 0 rgba(0,0,0,.08);}
@T{border-radius:70px 70px 0 0;margin-top:30px;}@A{border-radius:0 0 70px 70px;}
"""

HOME['v7-ledger'] = """
@C{border-radius:0;background:repeating-linear-gradient(#fff 0 31px,rgba(40,90,70,.18) 31px 32px);border:2px solid var(--ink);box-shadow:8px 8px 0 rgba(0,0,0,.15);}
@C.role-card-investor{border-top:10px solid var(--inv);}@C.role-card-borrower{border-top:10px solid var(--bor);}
@C .picker-cta{border:2px dashed currentColor;padding:6px 12px;display:inline-block;transform:rotate(-2deg);}
@S{border-radius:0;border:2px solid var(--ink);background:repeating-linear-gradient(#fff 0 27px,rgba(40,90,70,.14) 27px 28px);}@N{border-radius:0;}
@T{border-radius:0;border:3px double var(--ink);background:transparent;}@A{border-radius:0;border:3px double #fff;outline:2px solid var(--ink);}
"""
