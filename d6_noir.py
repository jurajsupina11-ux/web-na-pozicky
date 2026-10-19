from d6_common import art, base

NAME = 'noir'
TITLE = 'Noir - cierna a zlata (luxus)'
DESC = 'Luxusny tmavy dizajn, zlate linky, serif. Investor: zlata, Dlznik: medena.'
FONTS = 'Cormorant+Garamond:wght@500;600;700&family=Jost:wght@400;500;600'
ART = art('#1B1B1F', '#D4AF37', '#8B7440', '#B4684A', '#F1E7C8')
VARS = base(
    fh="'Cormorant Garamond'", fb="'Jost'", bg='#0E0E10', surface='#18181B', soft='#212126',
    line='rgba(212,175,55,.28)', ink='#F1E7C8', muted='#A79F88', radius='4px', radius_sm='3px', rb='2px',
    shadow='0 20px 40px -26px rgba(0,0,0,.9)',
    brand='#D4AF37', brand_ink='#0E0E10', brand_text='#D4AF37',
    inv='#D4AF37', inv_ink='#0E0E10', inv_text='#E3C463',
    bor='#C9764F', bor_ink='#fff', bor_text='#E39A74',
    hdr_bg='#0E0E10', hdr_ink='#F1E7C8', hdr_top='3px solid var(--acc)', hdr_bd='1px solid rgba(212,175,55,.3)',
    hero_bg='radial-gradient(ellipse at 80% 0%,#3A2F10 0%,transparent 55%),#0E0E10', hero_bg_solid='#0E0E10',
    hero_ink='#F1E7C8', hero_sub='#B9B096', hero_em='#E3C463', hero_chip='transparent', hero_chip_ink='#E3C463',
    hero_btn='var(--acc)', hero_btn_ink='var(--acc-ink)', hero_bd='1px solid rgba(212,175,55,.3)',
    cta_bg='#18181B', sb_bg='#18181B', sb_bd='1px solid rgba(212,175,55,.28)', sb_ink='#F1E7C8', sb_sub='#A79F88',
    sb_line='rgba(212,175,55,.25)', sb_hover='rgba(212,175,55,.1)',
    wal_bg='linear-gradient(135deg,#2A220A,#14110A)', wal_bd='1px solid rgba(212,175,55,.4)', wal_ink='#E7DDBB',
    wal_num='#E3C463', wal_btn='#D4AF37', wal_btn_ink='#0E0E10', ft_bg='#08080A', ft_ink='#A79F88', ft_h='#D4AF37',
    ft_line='rgba(212,175,55,.2)', th_ink='#D4AF37', focus='rgba(212,175,55,.25)', card_bd='1px solid rgba(212,175,55,.28)',
    vis_bg='#18181B', vis_bd='1px solid rgba(212,175,55,.45)', vis_r='4px', h1='58px',
)
CSS = """
h1,h2,h3{font-weight:600;letter-spacing:.01em;}
body .eyebrow{background:transparent;border:1px solid var(--acc);color:var(--acc-text);text-transform:uppercase;letter-spacing:.2em;font-size:11px;}
body .btn{text-transform:uppercase;letter-spacing:.14em;font-size:12px;font-weight:600;}
body .main-nav a{text-transform:uppercase;letter-spacing:.14em;font-size:12px;}
body .hero::before,body .picker-hero::before{content:'';position:absolute;right:-120px;top:-120px;width:440px;height:440px;border:1px solid rgba(212,175,55,.4);border-radius:50%;box-shadow:0 0 0 36px rgba(212,175,55,.06),0 0 0 72px rgba(212,175,55,.03);animation:spn 90s linear infinite;pointer-events:none;}
body .logo{background:#fff;padding:2px 12px;border-radius:6px;}
body .footer-brand .logo-full-img{background:none;}
body .stat-tile{border-left:0;border-top:2px solid var(--inv);}
body .stat-grid .stat-tile:nth-child(even){border-left:0;border-top-color:var(--bor);}
body .picker-hero .picker-card h2{color:#F1E7C8;}
body .picker-hero .role-card-investor .picker-stat b{color:#E3C463;}
body .wallet-actions input{background:#F1E7C8;}
body .status-pill{background:transparent;border:1px solid var(--acc);color:var(--acc-text);}
body .logo{padding:2px 8px;}
body .logo-full-img{height:70px;}
body{--nav-gap:12px;}
body .main-nav a{font-size:13px;padding:8px 2px;}
body .main-nav .btn-primary{padding:11px 18px;}
"""

