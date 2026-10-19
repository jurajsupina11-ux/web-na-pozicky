from d7_common import NAVFIX, base, svg

NAME = 'ledger'
TITLE = 'Ledger - uctovna kniha (papier / zelena a bordova)'
DESC = 'Papier s mriezkou, pisaci stroj, peciatky a perforacia. Investor: zelena, Dlznik: bordova.'
FONTS = 'Special+Elite&family=IBM+Plex+Mono:wght@400;500;600&family=Lora:wght@500;600;700'


def build():
    b = '<rect width="520" height="420" rx="6" fill="#F4EFDF"/>'
    b += '<g stroke="#9BB8A4" stroke-opacity=".55" stroke-width="1.5">'
    for i in range(1, 11):
        b += '<path d="M20 %d H500"/>' % (i * 38)
    b += '</g><path d="M70 20 V400" stroke="#C06A6A" stroke-width="2.5"/>'
    b += '<path d="M90 300 L170 250 L250 270 L330 190 L420 130 L490 80" stroke="#1F5C3F" stroke-width="6"/>'
    for i, (x, h) in enumerate([(110, 70), (190, 110), (270, 150), (350, 200), (430, 250)]):
        b += '<rect x="%d" y="%d" width="40" height="%d" fill="%s" stroke="#1F3A2B" stroke-width="3"/>' % (
            x, 372 - h, h, '#2E7D5B' if i % 2 == 0 else '#8C2F39')
    b += '<g transform="rotate(-14 410 130)"><circle cx="410" cy="130" r="58" stroke="#8C2F39" stroke-width="6"/>'
    b += '<circle cx="410" cy="130" r="46" stroke="#8C2F39" stroke-width="2.5"/>'
    b += '<path d="M382 130h56M410 104v52" stroke="#8C2F39" stroke-width="6"/></g>'
    b += '<g fill="#F4EFDF"><circle cx="38" cy="90" r="9"/><circle cx="38" cy="210" r="9"/><circle cx="38" cy="330" r="9"/></g>'
    return svg(520, 420, b)


ART = build()
VARS = base(
    fh="'Lora'", fb="'IBM Plex Mono'", bg='#EFE9D6', surface='#FBF8EC', soft='#EAE3CB', line='#CFC6A6',
    ink='#1F3A2B', muted='#5F6B5A', radius='2px', radius_sm='2px', rb='2px', shadow='none',
    brand='#1F5C3F', brand_ink='#fff', brand_text='#1F5C3F',
    inv='#1F5C3F', inv_ink='#fff', inv_text='#1F5C3F',
    bor='#8C2F39', bor_ink='#fff', bor_text='#8C2F39',
    hdr_bg='#FBF8EC', hdr_ink='#1F3A2B', hdr_top='0', hdr_bd='3px double #1F3A2B',
    hero_bg='#1F3A2B', hero_bg_solid='#1F3A2B', hero_ink='#F4EFDF', hero_sub='#CFD8C8', hero_em='#E8C766',
    hero_chip='#E8C766', hero_chip_ink='#1F3A2B', hero_btn='#E8C766', hero_btn_ink='#1F3A2B', cta_bg='#1F3A2B',
    sb_bg='#FBF8EC', sb_bd='2px solid #1F3A2B', sb_ink='#1F3A2B', sb_sub='#6B7566', sb_line='#CFC6A6', sb_hover='#EAE3CB',
    wal_bg='#1F3A2B', wal_ink='#DCE5D4', wal_num='#E8C766', wal_btn='#E8C766', wal_btn_ink='#1F3A2B',
    ft_bg='#1F3A2B', ft_ink='#B9C6B2', ft_h='#E8C766', ft_line='rgba(244,239,223,.25)', th_bg='#EAE3CB',
    th_ink='#1F3A2B', focus='rgba(31,92,63,.2)', card_bd='1px solid #1F3A2B', inp_bd='1.5px solid #1F3A2B',
    vis_bg='#F4EFDF', vis_bd='3px double #E8C766', vis_r='2px', h1='50px',
)
CSS = """
body{background-image:linear-gradient(rgba(31,58,43,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(31,58,43,.06) 1px,transparent 1px);background-size:26px 26px;}
h1,h2,h3{font-family:'Special Elite','Lora',serif;font-weight:400;letter-spacing:.01em;}
body .hero::before,body .picker-hero::before{content:'';position:absolute;right:5%;top:12%;width:150px;height:150px;border:5px double #E8C766;border-radius:50%;transform:rotate(-14deg);opacity:.55;animation:stm 6s ease-in-out infinite;pointer-events:none;}
@keyframes stm{0%,100%{transform:rotate(-14deg) scale(1);}50%{transform:rotate(-8deg) scale(1.05);}}
body .hero::after,body .picker-hero::after{content:'';position:absolute;left:0;right:0;bottom:0;height:14px;background:radial-gradient(circle at 10px 14px,#EFE9D6 7px,transparent 8px) 0 0/20px 14px repeat-x;}
body .card,body .stat-tile,body .step-card,body .benefit-card,body .picker-card,body .market-card,body .float-card,body .calc-box,body .stat-chip{border:1px solid #1F3A2B;box-shadow:4px 4px 0 rgba(31,58,43,.25);}
body .btn{text-transform:uppercase;letter-spacing:.06em;font-size:12.5px;border:2px solid #1F3A2B;font-family:'IBM Plex Mono',monospace;}
body .btn-primary{border-color:var(--acc);}
body .eyebrow{background:transparent;border:2px solid var(--acc);color:var(--acc-text);text-transform:uppercase;letter-spacing:.12em;transform:rotate(-2deg);display:inline-block;}
body .hero .eyebrow,body .picker-hero .eyebrow{border-color:#E8C766;color:#E8C766;}
body .stat-tile b,body .wallet-card .balance,body .stats-grid b{font-family:'IBM Plex Mono',monospace;font-weight:600;}
body .stat-tile{border-left:5px solid var(--inv);}
body .stat-grid .stat-tile:nth-child(even){border-left-color:var(--bor);}
body th{font-family:'IBM Plex Mono',monospace;border-bottom:2px solid #1F3A2B;}
body .main-nav a{font-family:'IBM Plex Mono',monospace;text-transform:uppercase;font-size:12.5px;letter-spacing:.06em;}
body .status-pill{border:2px solid currentColor;background:transparent;text-transform:uppercase;transform:rotate(-2deg);display:inline-block;}
""" + NAVFIX
