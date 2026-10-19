from home_v9 import HOME

HOME['v10-synthwave'] = """
@H{background:linear-gradient(#140630 0,#2B1060 60%,#6B1B7A 100%);}
@H::after{content:'';position:absolute;left:0;right:0;bottom:0;height:140px;background:repeating-linear-gradient(90deg,rgba(255,60,172,.5) 0 2px,transparent 2px 60px),repeating-linear-gradient(0deg,rgba(255,60,172,.5) 0 2px,transparent 2px 28px);transform:perspective(200px) rotateX(55deg);transform-origin:bottom;opacity:.6;pointer-events:none;}
@C{border-radius:0;clip-path:polygon(0 0,calc(100% - 24px) 0,100% 24px,100% 100%,24px 100%,0 calc(100% - 24px));box-shadow:none;border:0;background:linear-gradient(160deg,#2B1060,#1F0B47);outline:2px solid #28F2FF;}
@C.role-card-borrower{outline-color:#FF3CAC;}@S{border-radius:0;box-shadow:0 0 22px rgba(40,242,255,.25);}
@N{border-radius:0;box-shadow:0 0 18px currentColor;}@T{border-radius:0;background:linear-gradient(120deg,#2B1060,#6B1B7A);border:1px solid #FF3CAC;}
@B{text-shadow:0 0 18px currentColor;}@A{border-radius:0;box-shadow:0 0 40px rgba(255,60,172,.4);}
"""

HOME['v10-artdeco'] = """
@H{background:radial-gradient(circle at 50% 120%,rgba(212,175,55,.3),transparent 55%),#0C1A2B;border-bottom:6px double #D4AF37;}
@H .picker-head{border-top:1px solid #D4AF37;border-bottom:1px solid #D4AF37;padding:28px 0;}
@C{border-radius:0;clip-path:polygon(18px 0,calc(100% - 18px) 0,100% 18px,100% calc(100% - 18px),calc(100% - 18px) 100%,18px 100%,0 calc(100% - 18px),0 18px);border:0;outline:none;background:linear-gradient(160deg,#13263D,#0F2036);box-shadow:inset 0 0 0 2px #D4AF37;}
@C.role-card-investor,@C.role-card-borrower{border-top:0;}
@S{border-radius:0;clip-path:polygon(14px 0,calc(100% - 14px) 0,100% 14px,100% 100%,0 100%,0 14px);box-shadow:inset 0 0 0 1px #D4AF37;}
@N{border-radius:0;transform:rotate(45deg);}@N>*{transform:rotate(-45deg);}
@T{border-radius:0;background:#13263D;border-top:3px double #D4AF37;border-bottom:3px double #D4AF37;}@A{border-radius:0;border:3px double #D4AF37;}
"""

HOME['v10-botanical'] = """
@H{background:radial-gradient(circle at 90% 10%,#CFE2BF,transparent 40%),radial-gradient(circle at 5% 90%,#E6D9A8,transparent 40%),#EDF3E3;}
@C{border-radius:200px 200px 28px 28px;padding-top:64px;text-align:center;}@I .ic{margin:0 auto;border-radius:50%;}
@C.role-card-investor{box-shadow:0 14px 0 -6px #5BAA7A,0 22px 28px rgba(31,58,44,.2);}@C.role-card-borrower{box-shadow:0 14px 0 -6px #C96B4E,0 22px 28px rgba(31,58,44,.2);}
@S{border-radius:20px 80px 20px 80px;}@N{border-radius:50% 0 50% 0;background:#2F6B4F;}
@T{border-radius:30px 120px 30px 120px;margin:0 16px;}@A{border-radius:120px 30px 120px 30px;margin:0 16px 40px;}
"""

HOME['v10-watercolor'] = """
@H{background:radial-gradient(ellipse at 15% 25%,#BFE9E6 0,transparent 45%),radial-gradient(ellipse at 85% 65%,#F8D3E0 0,transparent 50%),radial-gradient(ellipse at 55% 5%,#FBE6B8 0,transparent 40%),#FBF7F2;}
@C{border-radius:62% 38% 55% 45%/48% 58% 42% 52%;background:rgba(255,255,255,.7);backdrop-filter:blur(3px);box-shadow:0 20px 40px rgba(143,156,232,.28);padding:56px 48px;}
@C.role-card-borrower{border-radius:40% 60% 45% 55%/55% 42% 58% 45%;}@S{border-radius:48% 52% 44% 56%/40% 46% 54% 60%;text-align:center;}
@N{margin:0 auto 14px;background:radial-gradient(circle at 35% 30%,#BFE9E6,#2FA8A4);}@S:nth-child(2) @N{background:radial-gradient(circle at 35% 30%,#FBE6B8,#E9A93A);}@S:nth-child(3) @N{background:radial-gradient(circle at 35% 30%,#F8D3E0,#D9628A);}
@T{border-radius:60% 40% 55% 45%/50% 60% 40% 50%;margin:0 16px;}@A{border-radius:50px;margin:0 16px 40px;}
"""

HOME['v10-pixel'] = """
@H{background-image:repeating-linear-gradient(0deg,rgba(255,255,255,.12) 0 4px,transparent 4px 8px);}
@C{border:4px solid #0C0D18;box-shadow:8px 8px 0 #0C0D18;border-radius:0;}@C.role-card-investor{border-top:12px solid #38B764;}@C.role-card-borrower{border-top:12px solid #F4A3C0;}
@C:hover{transform:translate(4px,4px);box-shadow:4px 4px 0 #0C0D18;}@C .picker-cta{background:#FFCD75;color:#1A1C2C;padding:6px 12px;display:inline-block;border:3px solid #0C0D18;}
@S{border:4px solid #0C0D18;box-shadow:6px 6px 0 #0C0D18;}@N{border-radius:0;border:4px solid #0C0D18;box-shadow:3px 3px 0 #0C0D18;}
@T{border:4px solid #566C86;border-radius:0;background:#222440;}@B{font-size:44px;}@A{border:4px solid #0C0D18;border-radius:0;box-shadow:8px 8px 0 #0C0D18;}
"""
