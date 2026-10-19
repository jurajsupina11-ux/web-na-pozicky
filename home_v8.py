from home_v7 import HOME

HOME['v8-blueprint'] = """
@C{border:2px dashed rgba(207,232,255,.7);border-radius:0;background:rgba(18,70,143,.55);}@C::before{content:'A-1';position:absolute;top:8px;right:12px;font:12px monospace;color:#7FE3FF;}
@C.role-card-investor{border-top:2px dashed #7FE3FF;}@C.role-card-borrower{border-top:2px dashed #FFD166;}
@S{border:2px dashed rgba(207,232,255,.6);background:rgba(18,70,143,.4);}@N{border-radius:0;background:transparent;border:2px solid var(--acc);color:var(--acc);}
@T{background:transparent;border:2px dashed rgba(207,232,255,.6);border-radius:0;}@A{border-radius:0;}
"""

HOME['v8-memphis'] = """
@C{border-radius:4px;}@C.role-card-investor{transform:rotate(-2.5deg);background:#fff;}@C.role-card-borrower{transform:rotate(2deg) translateY(18px);background:#FFD60A;}
@C::before{content:'';position:absolute;right:-24px;top:-24px;width:90px;height:90px;border-radius:50%;background:var(--inv);border:4px solid #14110F;}
@C.role-card-borrower::before{background:var(--bor);border-radius:0;transform:rotate(20deg);}
@S{transform:rotate(-1deg);}@S:nth-child(2){transform:rotate(1.5deg);background:#FFD60A;}@N{border:3px solid #14110F;border-radius:50%;}
@T{background:#FF4FA3;border:4px solid #14110F;border-radius:4px;box-shadow:8px 8px 0 #14110F;}@T span,@B{color:#14110F;}
@A{transform:rotate(-1deg);}
"""

HOME['v8-papercut'] = """
@C{box-shadow:0 2px 0 #fff inset,0 10px 0 -2px #BFE3D4,0 18px 0 -4px #8FCFB8,0 28px 24px rgba(35,51,46,.25);margin-bottom:34px;}
@S{box-shadow:0 8px 0 -2px #BFE3D4,0 14px 0 -4px #8FCFB8,0 20px 20px rgba(35,51,46,.2);margin-bottom:20px;}
@T{box-shadow:0 8px 0 #BFE3D4,0 16px 0 #8FCFB8,0 26px 30px rgba(35,51,46,.25);margin-bottom:40px;}
@A{box-shadow:0 10px 0 #FFD27A,0 20px 0 #FFB48F,0 32px 30px rgba(35,51,46,.3);margin-bottom:40px;}
"""

HOME['v8-cosmos'] = """
@C{box-shadow:0 0 0 1px rgba(110,231,255,.35),0 0 40px rgba(110,231,255,.18);}@C.role-card-borrower{box-shadow:0 0 0 1px rgba(255,138,76,.45),0 0 40px rgba(255,138,76,.2);}
@C::after{content:'';position:absolute;right:-70px;bottom:-70px;width:200px;height:200px;border:1px dashed rgba(110,231,255,.5);border-radius:50%;}
@N{border-radius:50%;box-shadow:0 0 0 6px rgba(110,231,255,.18),0 0 24px rgba(110,231,255,.5);}
@T{background:url('img-stars.svg'),linear-gradient(120deg,#1B1F6B,#4A1B8A);border-radius:999px;padding:50px 20px;}@A{border-radius:40px;}
"""

HOME['v8-gazette'] = """
@H .picker-head{border-top:3px double #1A1A1A;border-bottom:3px double #1A1A1A;padding:26px 0;max-width:none;}@H h1{font-size:76px;}
@H .picker-grid{gap:0;max-width:none;}@C{border-radius:0;box-shadow:none;border:0;border-right:1px solid #1A1A1A;padding:30px 36px;}@C:last-child{border-right:0;}
@C p::first-letter{font-size:52px;font-weight:900;float:left;line-height:.9;padding-right:8px;font-family:'Playfair Display',serif;}
@G{gap:0;}@S{box-shadow:none;border-radius:0;border:0;border-right:1px solid #1A1A1A;}@S:last-child{border-right:0;}@N{border-radius:0;font-family:'Playfair Display',serif;}
@T{border-radius:0;border-top:3px double #1A1A1A;border-bottom:3px double #1A1A1A;background:transparent;}@A{border-radius:0;}
"""
