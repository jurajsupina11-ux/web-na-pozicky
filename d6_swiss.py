from d6_common import art, base

NAME = 'swiss'
TITLE = 'Swiss - editorial cierno-biely'
DESC = 'Cierno-biely, velke verzalky, ostre hrany, tvrde tiene. Investor: modra, Dlznik: cervena.'
FONTS = 'Archivo:wght@500;700;800;900&family=IBM+Plex+Sans:wght@400;500;600'
ART = art('#EDEDEA', '#1844FF', '#111111', '#FF3B1F', '#111111')
VARS = base(
    fh="'Archivo'", fb="'IBM Plex Sans'", bg='#F4F4F2', surface='#FFFFFF', soft='#EDEDEA',
    line='#111111', ink='#111111', muted='#4A4A4A', radius='0px', radius_sm='0px', rb='0px', shadow='none',
    brand='#111111', brand_ink='#fff', brand_text='#111111',
    inv='#1844FF', inv_ink='#fff', inv_text='#1844FF',
    bor='#FF3B1F', bor_ink='#fff', bor_text='#E02A10',
    hdr_bg='#F4F4F2', hdr_ink='#111', hdr_top='8px solid var(--acc)', hdr_bd='2px solid #111',
    hero_bg='#111111', hero_bg_solid='#111', hero_ink='#F4F4F2', hero_sub='#CFCFCB', hero_em='var(--acc)',
    hero_btn='var(--acc)', hero_btn_ink='#fff', cta_bg='#111',
    sb_bg='#fff', sb_bd='2px solid #111', sb_ink='#111', sb_sub='#555', sb_line='#111', sb_hover='#EDEDEA',
    wal_bg='#111', wal_ink='#F4F4F2', wal_num='#fff', wal_btn='var(--acc)', wal_btn_ink='#fff',
    ft_bg='#111', ft_ink='#BDBDB8', ft_h='#fff', ft_line='#444', th_ink='#111',
    focus='rgba(24,68,255,.2)', card_bd='2px solid #111', inp_bd='2px solid #111',
    vis_bg='#fff', vis_bd='3px solid #fff', vis_r='0px', h1='60px',
)
CSS = """
h1,h2{text-transform:uppercase;letter-spacing:-.02em;font-weight:900;}
body .hero h1,body .picker-hero h1{line-height:1;}
body .card,body .stat-tile,body .step-card,body .benefit-card,body .picker-card,body .market-card{box-shadow:6px 6px 0 #111;}
body .picker-card:hover,body .step-card:hover,body .benefit-card:hover{transform:translate(-3px,-3px);box-shadow:10px 10px 0 #111;}
body .btn{text-transform:uppercase;letter-spacing:.06em;font-weight:800;}
body .main-nav a{text-transform:uppercase;font-size:12.5px;letter-spacing:.08em;font-weight:700;}
body .hero::after,body .picker-hero::after{content:'';position:absolute;right:0;top:0;bottom:0;width:26%;background:repeating-linear-gradient(135deg,var(--acc) 0 14px,transparent 14px 28px);opacity:.95;}
body .hero .wrap,body .picker-hero .wrap{z-index:2;}
body .eyebrow{text-transform:uppercase;}
body .status-pill{border:2px solid #111;}
body .dash-top h1{font-size:44px;}
body .hero-visual{border-radius:0;}
"""
