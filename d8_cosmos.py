from a8_cosmos import build
from d7_common import NAVFIX, base

NAME = 'cosmos'
TITLE = 'Cosmos - vesmir, planety a raketa (modra / oranzova)'
DESC = 'Tmavy vesmir s hviezdami, planetami a raketou. Investor: cyan, Dlznik: oranzova.'
FONTS = 'Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600'
ART, EXTRA = build()
VARS = base(
    fh="'Space Grotesk'", fb="'Inter'", bg='#070B24', surface='#101A47', soft='#0C1438',
    line='rgba(140,170,255,.25)', ink='#EEF2FF', muted='#A9B6E8', radius='16px', radius_sm='10px', rb='999px',
    shadow='0 10px 30px rgba(0,0,0,.45)', brand='#6EE7FF', brand_ink='#04122E', brand_text='#6EE7FF',
    inv='#6EE7FF', inv_ink='#04122E', inv_text='#6EE7FF', bor='#FF8A4C', bor_ink='#2A0F00', bor_text='#FFA877',
    hdr_bg='rgba(7,11,36,.92)', hdr_ink='#EEF2FF', hdr_top='0', hdr_bd='1px solid rgba(140,170,255,.25)',
    hero_bg='#070B24', hero_bg_solid='#070B24', hero_ink='#fff', hero_sub='#B8C4F0', hero_em='#6EE7FF',
    hero_chip='rgba(110,231,255,.15)', hero_chip_ink='#6EE7FF', hero_btn='#FF8A4C', hero_btn_ink='#2A0F00', cta_bg='#101A47',
    sb_bg='#0C1438', sb_bd='1px solid rgba(140,170,255,.25)', sb_ink='#EEF2FF', sb_sub='#9AA8DD',
    sb_line='rgba(140,170,255,.2)', sb_hover='rgba(110,231,255,.1)', wal_bg='#1B1F6B',
    wal_bd='1px solid rgba(140,170,255,.4)', wal_ink='#EEF2FF', wal_num='#6EE7FF', wal_btn='#6EE7FF',
    wal_btn_ink='#04122E', ft_bg='#04071A', ft_ink='#9AA8DD', ft_h='#6EE7FF', ft_line='rgba(140,170,255,.2)',
    th_ink='#6EE7FF', focus='rgba(110,231,255,.35)', card_bd='1px solid rgba(140,170,255,.3)',
    inp_bd='1px solid rgba(140,170,255,.4)', vis_bg='transparent', vis_bd='0',
    vis_r='16px', h1='58px',
)
CSS = """
body{background:#070B24 url('img-stars.svg') 0 0/560px 360px;}
body .hero,body .picker-hero{background:url('img-space.svg') center/cover,radial-gradient(circle at 80% 30%,#2A1B7A,#070B24 65%);}
body .btn{border-radius:999px;font-weight:700;box-shadow:0 0 20px rgba(110,231,255,.25);}
body .btn-primary:hover{box-shadow:0 0 26px rgba(255,138,76,.55);}
body .site-header{backdrop-filter:blur(8px);}
body .card,body .stat-tile,body .step-card,body .benefit-card,body .picker-card,body .market-card{position:relative;overflow:hidden;background-image:linear-gradient(160deg,rgba(255,255,255,.06),transparent 50%);}
body .step-card::after,body .benefit-card::after{content:'';position:absolute;right:-12px;top:-12px;width:90px;height:90px;background:no-repeat center/contain;pointer-events:none;opacity:.95;}
body .step-card:nth-child(1)::after,body .benefit-card:nth-child(1)::after{background-image:url('img-ic1.svg');}
body .step-card:nth-child(2)::after,body .benefit-card:nth-child(2)::after{background-image:url('img-ic2.svg');}
body .step-card:nth-child(3)::after,body .benefit-card:nth-child(3)::after{background-image:url('img-ic3.svg');}
body .benefit-card:nth-child(4)::after{background-image:url('img-ic4.svg');}
body .cta-band{background:url('img-space.svg') center/cover,linear-gradient(135deg,#1B1F6B,#4A1B8A);border:1px solid rgba(140,170,255,.4);}
body .wallet-card{background:url('img-ic3.svg') right 14px bottom -30px/150px no-repeat,url('img-stars.svg') center/cover,#1B1F6B;}
body .site-footer{background:url('img-horizon.svg') top center/cover no-repeat,#04071A;padding-top:170px;border-top:0;}
body .stat-tile{border-left:0;border-top:3px solid var(--inv);}
body .stat-grid .stat-tile:nth-child(even){border-top-color:var(--bor);}
body .logo{background:#fff;padding:3px 12px;border-radius:10px;}
body .hero-visual{background:var(--vis-img) no-repeat center/100%;}
body .eyebrow{border:1px solid rgba(110,231,255,.5);}
""" + NAVFIX
