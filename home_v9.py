from home_v8 import HOME

HOME['v9-neobank'] = """
@C{border-radius:32px;box-shadow:0 24px 50px rgba(91,91,240,.2);}@C .picker-cta{background:var(--soft);padding:10px 18px;border-radius:999px;display:inline-block;}
@C.role-card-investor{background:linear-gradient(160deg,#fff,#ECEEFF);}@C.role-card-borrower{background:linear-gradient(160deg,#fff,#FFEEE3);}
@I .ic{border-radius:18px;box-shadow:0 10px 20px rgba(91,91,240,.25);}
@S{border-radius:26px;}@N{border-radius:14px;background:linear-gradient(135deg,#5B5BF0,#8B5CF6);}
@T{border-radius:34px;background:linear-gradient(135deg,#14173A,#2B2F7A);}@B{color:#fff;}@T span{color:#A9B0D6;}
"""

HOME['v9-privatebank'] = """
@H{border-bottom:6px double #C9A24B;}@H .picker-head{max-width:640px;}
@C{border-radius:2px;border:1px solid #C9A24B;outline:1px solid #C9A24B;outline-offset:-9px;padding:52px 44px;text-align:center;}@I .ic{margin:0 auto;border-radius:50%;}
@C.role-card-investor,@C.role-card-borrower{border-top-width:1px;}
@S{border-radius:2px;border-top:4px solid #C9A24B;text-align:center;}@N{margin:0 auto 14px;border-radius:50%;background:#0F2A5C;color:#E3B84F;}
@T{border-radius:0;background:#0F2A5C;border-top:4px solid #C9A24B;border-bottom:4px solid #C9A24B;}@B{color:#E3B84F;}@T span{color:#C9D6F0;}
@A{border-radius:0;border-top:6px double #C9A24B;}
"""

HOME['v9-mintfin'] = """
@C{border-radius:44px;}@C.role-card-investor{background:linear-gradient(160deg,#fff,#D1FAE5);}@C.role-card-borrower{background:linear-gradient(160deg,#fff,#FCE7F3);}
@I .ic{border-radius:50%;width:64px;height:64px;}
@S{border-radius:36px;}@N{border-radius:50%;background:#10B981;}@S:nth-child(2) @N{background:#FBBF24;}@S:nth-child(3) @N{background:#EC4899;}
@T{border-radius:44px;background:#10B981;margin:0 16px;}@B{color:#04281E;}@T span{color:#064E3B;}@A{border-radius:44px;margin:0 16px 40px;}
"""

HOME['v9-trader'] = """
@C{border-radius:8px;padding-top:64px;}@C::before{content:'\\25CF  \\25CF  \\25CF   LIVE';position:absolute;left:0;right:0;top:0;padding:8px 16px;background:#0E1417;border-bottom:1px solid #23323A;font:11px 'IBM Plex Mono',monospace;color:#8DA3AB;letter-spacing:.15em;}
@S{border-radius:8px;border-left:3px solid var(--inv);}@S:nth-child(2){border-left-color:#22D3EE;}@S:nth-child(3){border-left-color:var(--bor);}
@N{font-family:'IBM Plex Mono',monospace;border-radius:4px;}
@T{border-radius:8px;border:1px solid #2E4650;background:#0E1417;}@B{font-family:'IBM Plex Mono',monospace;text-shadow:0 0 16px rgba(198,255,61,.5);}@A{border-radius:8px;}
"""

HOME['v9-pastel'] = """
@C{border-radius:44px;box-shadow:0 20px 40px rgba(129,140,248,.25);}@C.role-card-investor{background:#DCEEFB;}@C.role-card-borrower{background:#FDE2E4;}
@C .picker-stat{background:rgba(255,255,255,.7);display:inline-block;padding:8px 16px;border-radius:999px;}
@S{border-radius:44px;}@S:nth-child(1){background:#FFF1C9;}@S:nth-child(2){background:#DCEEFB;}@S:nth-child(3){background:#FDE2E4;}
@N{background:#fff;color:var(--ink);box-shadow:0 6px 14px rgba(0,0,0,.1);}
@T{border-radius:60px;background:linear-gradient(135deg,#DCEEFB,#FDE2E4);margin:0 16px;}@B{color:#2A2F4A;}@A{border-radius:60px;margin:0 16px 40px;}
"""
