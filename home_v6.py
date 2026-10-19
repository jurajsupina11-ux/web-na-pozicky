"""Domovska stranka (pub-landing) podla stylu. Tokeny: @H hero, @C picker-card, @S step-card, @N step-num,
@G steps-grid, @T stats-band, @B stats-grid b, @A cta-band, @I picker-icon."""

HOME = {}

HOME['v6-aurora'] = """
@H{background-image:radial-gradient(circle at 15% 20%,rgba(124,92,255,.35),transparent 45%),radial-gradient(circle at 85% 75%,rgba(255,92,200,.3),transparent 45%),var(--hero-bg);}
@C{background:rgba(255,255,255,.55);backdrop-filter:blur(16px);border:1px solid rgba(255,255,255,.8);box-shadow:0 20px 50px rgba(124,92,255,.25);}
@C.role-card-investor{transform:rotate(-1.2deg);}@C.role-card-borrower{transform:rotate(1.2deg) translateY(14px);}
@S{background:linear-gradient(160deg,rgba(255,255,255,.9),rgba(240,232,255,.7));border-radius:28px;}
@N{box-shadow:0 0 0 8px rgba(124,92,255,.15);}
@T{background:linear-gradient(120deg,#7C5CFF,#FF5CC8);color:#fff;}@T span{color:rgba(255,255,255,.85);}@B{color:#fff;}
@A{background:radial-gradient(circle at 80% 20%,rgba(255,92,200,.5),transparent 50%),linear-gradient(135deg,#4B2FD6,#7C5CFF);}
"""

HOME['v6-swiss'] = """
@H{border-bottom:8px solid var(--ink);}@H .picker-head{text-align:left;margin-left:0;max-width:760px;}
@H h1{font-size:76px;line-height:.95;letter-spacing:-.04em;}
@H .picker-grid{gap:0;max-width:none;border:3px solid var(--ink);}
@C{border-radius:0;border:0;box-shadow:none;border-right:3px solid var(--ink);padding:52px 40px;}@C:last-child{border-right:0;}
@C.role-card-investor{border-top:0;box-shadow:inset 0 14px 0 var(--inv);}@C.role-card-borrower{border-top:0;box-shadow:inset 0 14px 0 var(--bor);}
@G{gap:0;border-top:3px solid var(--ink);}@S{border-radius:0;box-shadow:none;border:0;border-right:3px solid var(--ink);padding:36px 28px;}@S:last-child{border-right:0;}
@N{border-radius:0;width:64px;height:64px;font-size:34px;}
@T{border-radius:0;background:var(--ink);color:#fff;}@B{color:#fff;font-size:56px;letter-spacing:-.04em;}@T span{color:#cfcfcf;}
@A{border-radius:0;border-top:8px solid var(--acc);}
"""

HOME['v6-zen'] = """
@H{padding:120px 0 90px;}@H .picker-grid{gap:56px;}
@C{background:transparent;border:0;box-shadow:none;border-top:1px solid var(--ink);border-radius:0;padding:34px 6px 8px;}
@C:hover{transform:none;border-top-width:3px;}@C.role-card-investor,@C.role-card-borrower{border-top-color:var(--ink);}
@I .ic{background:none;border:1px solid currentColor;border-radius:50%;}
@G{gap:60px;}@S{background:none;box-shadow:none;border:0;border-left:1px solid var(--line);border-radius:0;padding:6px 0 6px 26px;}
@N{background:none;color:var(--ink);border:1px solid var(--ink);width:44px;height:44px;}
@T{background:none;border-top:1px solid var(--line);border-bottom:1px solid var(--line);border-radius:0;}
@A{background:none;border:0;color:var(--ink);text-align:center;}@A h2,@A p{color:var(--ink);}
"""

HOME['v6-ocean'] = """
@H{padding-bottom:120px;}
@C{border-radius:50px 50px 30px 30px;box-shadow:0 24px 40px rgba(0,60,120,.25);}
@S{border-radius:40px;}@N{border-radius:50%;box-shadow:0 0 0 10px rgba(255,255,255,.5);}
@T{border-radius:60px;margin:0 16px;}@A{border-radius:60px;margin:0 16px 40px;}
"""

HOME['v6-noir'] = """
@H{border-bottom:1px solid var(--acc);}@H h1{font-weight:300;letter-spacing:.02em;}
@C{background:linear-gradient(160deg,#17171b,#0d0d10);border:1px solid rgba(212,175,55,.45);border-radius:2px;}
@C.role-card-investor,@C.role-card-borrower{border-top:1px solid rgba(212,175,55,.45);}
@C.role-card-investor{box-shadow:inset 0 3px 0 var(--inv);}@C.role-card-borrower{box-shadow:inset 0 3px 0 var(--bor);}
@S{background:none;border:0;border-top:1px solid rgba(212,175,55,.45);border-radius:0;box-shadow:none;position:relative;padding-top:60px;}
@N{position:absolute;top:6px;left:0;background:none;color:var(--acc);font-size:44px;font-weight:300;width:auto;height:auto;}
@T{background:transparent;border:1px solid rgba(212,175,55,.45);border-radius:2px;}@B{font-weight:300;font-size:50px;}
@A{background:linear-gradient(120deg,#17171b,#0d0d10);border:1px solid rgba(212,175,55,.45);border-radius:2px;}
"""
