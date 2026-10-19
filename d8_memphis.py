from a8_memphis import build
from d7_common import NAVFIX, base

NAME = 'memphis'
TITLE = 'Memphis - pop tvary a konfety (ruzova+zlta / tyrkys)'
DESC = 'Hrube ciary, kruhy, trojuholniky, cik-cak a konfety. Investor: tyrkysova, Dlznik: ruzova.'
FONTS = 'Rubik:wght@500;700;800;900&family=DM+Sans:wght@400;500;700'
ART, EXTRA = build()
VARS = base(
    fh="'Rubik'", fb="'DM Sans'", bg='#FFF4E0', surface='#FFFFFF', soft='#FFE9C2',
    line='#14110F', ink='#14110F', muted='#4A433B', radius='4px', radius_sm='2px', rb='999px',
    shadow='6px 6px 0 #14110F', brand='#14110F', brand_ink='#FFD60A', brand_text='#14110F',
    inv='#00C2A8', inv_ink='#14110F', inv_text='#007A69', bor='#FF4FA3', bor_ink='#14110F', bor_text='#C2186F',
    hdr_bg='#FFD60A', hdr_ink='#14110F', hdr_top='0', hdr_bd='4px solid #14110F',
    hero_bg='#FF4FA3', hero_bg_solid='#FF4FA3', hero_ink='#14110F', hero_sub='#14110F', hero_em='#FFFFFF',
    hero_chip='#FFD60A', hero_chip_ink='#14110F', hero_btn='#14110F', hero_btn_ink='#FFD60A', cta_bg='#00C2A8',
    sb_bg='#FFD60A', sb_bd='4px solid #14110F', sb_ink='#14110F', sb_sub='#4A433B',
    sb_line='#14110F', sb_hover='rgba(20,17,15,.1)', wal_bg='#14110F',
    wal_bd='4px solid #14110F', wal_ink='#FFF4E0', wal_num='#FFD60A', wal_btn='#FFD60A',
    wal_btn_ink='#14110F', ft_bg='#14110F', ft_ink='#FFF4E0', ft_h='#FFD60A', ft_line='rgba(255,244,224,.3)',
    th_ink='#14110F', focus='rgba(255,79,163,.4)', card_bd='3px solid #14110F',
    inp_bd='3px solid #14110F', vis_bg='#FFD60A', vis_bd='4px solid #14110F',
    vis_r='4px', h1='64px',
)
CSS = """
body{background:#FFF4E0 url('img-dots.svg') 0 0/120px 120px;}
h1,h2,h3{font-weight:900;letter-spacing:-.02em;}
body .hero,body .picker-hero{background:url('img-confetti.svg') right bottom/560px no-repeat,#FF4FA3;border-bottom:4px solid #14110F;}
body .btn{border:3px solid #14110F;font-weight:800;box-shadow:4px 4px 0 #14110F;transition:transform .12s,box-shadow .12s;}
body .btn:hover{transform:translate(2px,2px);box-shadow:2px 2px 0 #14110F;}
body .btn-primary{color:#14110F;}
body .main-nav a{font-weight:700;}
body .eyebrow{border:3px solid #14110F;box-shadow:3px 3px 0 #14110F;transform:rotate(-2deg);}
body .card,body .stat-tile,body .step-card,body .benefit-card,body .picker-card,body .market-card{position:relative;overflow:hidden;box-shadow:6px 6px 0 #14110F;}
body .step-card:nth-child(odd),body .benefit-card:nth-child(odd){transform:rotate(-.6deg);}
body .step-card:nth-child(even),body .benefit-card:nth-child(even){transform:rotate(.6deg);}
body .step-card::after,body .benefit-card::after{content:'';position:absolute;right:-10px;top:-10px;width:84px;height:84px;background:no-repeat center/contain;pointer-events:none;}
body .step-card:nth-child(1)::after,body .benefit-card:nth-child(1)::after{background-image:url('img-ic1.svg');}
body .step-card:nth-child(2)::after,body .benefit-card:nth-child(2)::after{background-image:url('img-ic2.svg');}
body .step-card:nth-child(3)::after,body .benefit-card:nth-child(3)::after{background-image:url('img-ic3.svg');}
body .benefit-card:nth-child(4)::after{background-image:url('img-ic4.svg');}
body .cta-band{background:url('img-confetti.svg') left top/520px no-repeat,#00C2A8;border:4px solid #14110F;box-shadow:8px 8px 0 #14110F;}
body .wallet-card{background:url('img-zig.svg') left bottom/220px no-repeat,#14110F;border:4px solid #14110F;}
body .site-footer{background:url('img-band.svg') top left/1400px 90px repeat-x,#14110F;padding-top:130px;border-top:4px solid #14110F;}
body .stat-tile{border-left:3px solid #14110F;border-bottom:8px solid var(--inv);}
body .stat-grid .stat-tile:nth-child(even){border-bottom-color:var(--bor);}
body .logo{background:#fff;padding:2px 10px;border:3px solid #14110F;}
body .hero-visual{background:#FFD60A var(--vis-img) no-repeat center/92%;box-shadow:8px 8px 0 #14110F;}
body .alert{border:3px solid #14110F;}
""" + NAVFIX
