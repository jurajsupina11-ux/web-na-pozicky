from d6_common import art, base

NAME = 'aurora'
TITLE = 'Aurora - tmavy neon'
DESC = 'Tmavy fintech, neonovy gradient, sklenene karty. Investor: tyrkys, Dlznik: oranzova.'
FONTS = 'Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700'
ART = art('#18223D', '#19E3C0', '#8B7BFF', '#FF8A4C', '#F2F5FF')
VARS = base(
    fh="'Space Grotesk'", fb="'Inter'", bg='#0A0F1E', surface='#121A30', soft='#18223D',
    line='rgba(255,255,255,.12)', ink='#F2F5FF', muted='#9AA6C7', radius='22px', rb='999px',
    shadow='0 18px 40px -22px rgba(0,0,0,.8)',
    brand='#8B7BFF', brand_ink='#0A0F1E', brand_text='#B7ADFF',
    inv='#19E3C0', inv_ink='#04201A', inv_text='#4EF0D2',
    bor='#FF8A4C', bor_ink='#2A1004', bor_text='#FFA877',
    hdr_bg='rgba(10,15,30,.78)', hdr_ink='#E6EBFF', hdr_blur='blur(14px)', hdr_bd='1px solid rgba(255,255,255,.08)',
    hero_bg='radial-gradient(ellipse at 15% 20%,#2B2A6B 0%,transparent 55%),radial-gradient(ellipse at 85% 30%,#0E5C58 0%,transparent 55%),#0A0F1E',
    hero_bg_solid='#0A0F1E', hero_ink='#fff', hero_sub='#B7C0DE', hero_em='#4EF0D2',
    cta_bg='linear-gradient(120deg,#2B2A6B,#0E5C58)',
    sb_bg='#101830', sb_bd='1px solid rgba(255,255,255,.08)', sb_ink='#E6EBFF', sb_sub='#8E9AC0',
    sb_line='rgba(255,255,255,.1)', sb_hover='rgba(255,255,255,.07)',
    wal_bg='linear-gradient(135deg,#2B2A6B,#0E5C58)', wal_ink='#E6EBFF', wal_num='#fff',
    wal_btn='#19E3C0', wal_btn_ink='#04201A', ft_bg='#060A16', ft_ink='#8E9AC0', ft_h='#fff',
    ft_line='rgba(255,255,255,.1)', th_ink='#9AA6C7', focus='rgba(78,240,210,.25)',
    btn_sh='0 0 22px -4px var(--acc)', card_bd='1px solid rgba(255,255,255,.12)',
    vis_bg='rgba(255,255,255,.04)', vis_bd='1px solid rgba(255,255,255,.14)',
)
CSS = """
body{background:#0A0F1E;}
body .card,body .stat-tile,body .step-card,body .benefit-card,body .picker-card,body .market-card{backdrop-filter:blur(8px);}
body .hero::before,body .picker-hero::before{content:'';position:absolute;right:-8%;top:-30%;width:560px;height:560px;background:conic-gradient(from 0deg,#19E3C0,#8B7BFF,#FF8A4C,#19E3C0);filter:blur(120px);opacity:.3;animation:spn 28s linear infinite;pointer-events:none;}
body .btn-primary:hover{box-shadow:0 0 30px -2px var(--acc);}
body .logo{background:#fff;padding:2px 12px;border-radius:14px;}
body .footer-brand .logo-full-img{background:none;}
body .wallet-actions input{background:rgba(255,255,255,.95);}
body .logo{padding:2px 8px;}
body .logo-full-img{height:70px;}
body{--nav-gap:12px;}
body .main-nav a{font-size:13px;padding:8px 2px;}
body .main-nav .btn-primary{padding:11px 18px;}
"""

