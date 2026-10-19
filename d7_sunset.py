from d7_common import NAVFIX, base, svg

NAME = 'sunset'
TITLE = 'Sunset - vlny a zapad slnka (ruzova / modra)'
DESC = 'Teply gradient zapadu, vlnite hrany a plavajuce bubliny. Investor: modra, Dlznik: korálová.'
FONTS = 'Outfit:wght@500;600;700;800&family=Nunito:wght@400;600;700'


def build():
    b = ('<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FF9A8B"/>'
         '<stop offset=".55" stop-color="#FF6A88"/><stop offset="1" stop-color="#7C5CFF"/></linearGradient></defs>')
    b += '<rect width="520" height="420" rx="30" fill="url(#g)"/>'
    b += '<circle cx="360" cy="190" r="86" fill="#FFE29A"/><circle cx="360" cy="190" r="116" stroke="#FFE29A" stroke-opacity=".45" stroke-width="4"/>'
    b += '<path d="M0 250 Q70 215 140 250 T280 250 T420 250 T520 235 V420 H0Z" fill="#6D4BE0" fill-opacity=".75"/>'
    b += '<path d="M0 300 Q90 265 180 300 T360 300 T520 285 V420 H0Z" fill="#3B2DB5"/>'
    b += '<path d="M0 350 Q110 322 220 350 T440 350 T520 340 V420 H0Z" fill="#1E1A6B"/>'
    for i, x in enumerate([70, 150, 230, 310, 390]):
        h = 40 + i * 26
        b += '<rect x="%d" y="%d" width="38" height="%d" rx="12" fill="%s"/>' % (
            x, 340 - h, h, '#FFE29A' if i % 2 == 0 else '#fff')
    b += '<path d="M70 280 C150 250 230 230 410 120" stroke="#fff" stroke-width="6"/>'
    b += '<circle cx="410" cy="120" r="11" fill="#FF6A88" stroke="#fff" stroke-width="5"/>'
    b += '<circle cx="90" cy="90" r="16" fill="#fff" fill-opacity=".35"/><circle cx="140" cy="60" r="8" fill="#fff" fill-opacity=".35"/>'
    return svg(520, 420, b)


ART = build()
VARS = base(
    fh="'Outfit'", fb="'Nunito'", bg='#FFF7F3', surface='#FFFFFF', soft='#FFEDE6', line='#FFD9CC',
    ink='#2A1A4A', muted='#7A6A92', radius='30px', radius_sm='18px', rb='999px',
    shadow='0 20px 40px -26px rgba(124,92,255,.5)',
    brand='#7C5CFF', brand_ink='#fff', brand_text='#5B3FE0',
    inv='#3B7BFF', inv_ink='#fff', inv_text='#2A62DB',
    bor='#FF6A88', bor_ink='#fff', bor_text='#E0436A',
    hdr_bg='rgba(255,247,243,.85)', hdr_ink='#2A1A4A', hdr_top='0', hdr_bd='1px solid #FFD9CC', hdr_blur='blur(10px)',
    hero_bg='linear-gradient(180deg,#FF9A8B 0%,#FF6A88 55%,#7C5CFF 100%)', hero_bg_solid='#FF6A88',
    hero_ink='#fff', hero_sub='#FFF0EA', hero_em='#FFE29A', hero_chip='#fff', hero_chip_ink='#E0436A',
    hero_btn='#fff', hero_btn_ink='#5B3FE0', cta_bg='linear-gradient(120deg,#FF6A88,#7C5CFF)',
    sb_bg='#fff', sb_bd='1px solid #FFD9CC', sb_ink='#2A1A4A', sb_sub='#8A7AA3', sb_line='#FFD9CC', sb_hover='#FFEDE6',
    wal_bg='linear-gradient(120deg,#FF6A88,#7C5CFF)', wal_ink='#FFF0EA', wal_num='#fff',
    wal_btn='#fff', wal_btn_ink='#5B3FE0', ft_bg='#1E1A6B', ft_ink='#C9C4F2', ft_h='#FFE29A',
    ft_line='rgba(255,255,255,.18)', focus='rgba(124,92,255,.25)', vis_bg='transparent', vis_bd='0',
    vis_r='30px', h1='58px',
)
CSS = """
body .hero,body .picker-hero{padding-bottom:120px;}
body .hero .wrap::after,body .picker-hero .wrap::after{content:'';position:absolute;left:0;right:0;bottom:-120px;height:110px;background:#FFF7F3;-webkit-mask:radial-gradient(60px 36px at 50% 100%,#000 98%,transparent 100%) -30px 0/120px 100% repeat-x;mask:radial-gradient(60px 36px at 50% 100%,#000 98%,transparent 100%) -30px 0/120px 100% repeat-x;}
body .hero::before,body .picker-hero::before{content:'';position:absolute;right:8%;top:14%;width:150px;height:150px;border-radius:50%;background:#FFE29A;opacity:.75;box-shadow:0 0 70px 24px rgba(255,226,154,.5);animation:flt 8s ease-in-out infinite;pointer-events:none;}
body .hero::after,body .picker-hero::after{content:'';position:absolute;left:6%;top:20%;width:70px;height:70px;border-radius:50%;background:#fff;opacity:.25;animation:flt 6s ease-in-out infinite reverse;pointer-events:none;}
body .btn{box-shadow:0 12px 22px -14px rgba(42,26,74,.8);}
body .step-card,body .benefit-card,body .picker-card{border-radius:30px 30px 30px 80px;}
body .picker-card:hover{transform:translateY(-6px) rotate(-1deg);}
body .stat-tile{border-left:0;border-top:6px solid var(--inv);border-radius:24px;}
body .stat-grid .stat-tile:nth-child(even){border-left:0;border-top-color:var(--bor);}
body .wallet-card{border-radius:30px 80px 30px 30px;}
body .hero-visual{background:transparent var(--vis-img) no-repeat center/100%;min-height:400px;}
body .hero-visual .float-card{border-radius:24px;}
body .eyebrow{font-weight:800;}
""" + NAVFIX
