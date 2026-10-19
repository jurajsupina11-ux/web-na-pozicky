from d7_common import NAVFIX, base, svg

NAME = 'skyline'
TITLE = 'Skyline - mestska noc (ocelova / cyan)'
DESC = 'Panorama mesta, zrezane rohy, mriezka a technicke linky. Investor: cyan, Dlznik: gula (magenta).'
FONTS = 'Chakra+Petch:wght@500;600;700&family=Barlow:wght@400;500;600'


def build():
    b = '<rect width="520" height="420" fill="#0F2233"/>'
    b += '<g stroke="#22D3EE" stroke-opacity=".12"><path d="M0 70H520M0 140H520M0 210H520M0 280H520M0 350H520"/></g>'
    b += '<circle cx="420" cy="86" r="34" fill="#F472B6" fill-opacity=".9"/>'
    towers = [(40, 220, 70), (120, 150, 80), (210, 90, 90), (310, 170, 74), (394, 130, 86)]
    for i, (x, top, w) in enumerate(towers):
        col = '#1B3A57' if i % 2 else '#16324B'
        b += ('<polygon points="%d,380 %d,%d %d,%d %d,%d %d,380" fill="%s" stroke="#22D3EE" '
              'stroke-opacity=".7" stroke-width="2.5"/>' % (x, x, top + 14, x + 14, top, x + w, top, x + w, col))
        for r in range(int((380 - top) / 26) - 1):
            for c in range(int(w / 20)):
                if (r * 7 + c * 3 + i) % 3:
                    b += '<rect x="%d" y="%d" width="9" height="10" fill="%s"/>' % (
                        x + 10 + c * 18, top + 24 + r * 26, '#22D3EE' if (r + c) % 4 else '#F472B6')
    b += '<path d="M30 300 L130 250 L220 270 L320 190 L420 130 L490 70" stroke="#22D3EE" stroke-width="5"/>'
    b += '<circle cx="490" cy="70" r="10" fill="#22D3EE"/><rect x="0" y="380" width="520" height="40" fill="#0A1622"/>'
    return svg(520, 420, b)


ART = build()
VARS = base(
    fh="'Chakra Petch'", fb="'Barlow'", bg='#0B1824', surface='#10243A', soft='#163049',
    line='rgba(34,211,238,.28)', ink='#E6F6FF', muted='#8FB0C7', radius='0px', radius_sm='0px', rb='0px',
    shadow='none', brand='#22D3EE', brand_ink='#04222B', brand_text='#67E8F9',
    inv='#22D3EE', inv_ink='#04222B', inv_text='#67E8F9',
    bor='#F472B6', bor_ink='#3A0820', bor_text='#F9A8D4',
    hdr_bg='#0B1824', hdr_ink='#E6F6FF', hdr_top='4px solid var(--acc)', hdr_bd='1px solid rgba(34,211,238,.3)',
    hero_bg='linear-gradient(180deg,#0B1824 0%,#12304A 100%)', hero_bg_solid='#0B1824',
    hero_ink='#fff', hero_sub='#A9C6DA', hero_em='#67E8F9', hero_chip='transparent', hero_chip_ink='#67E8F9',
    hero_btn='var(--acc)', hero_btn_ink='var(--acc-ink)', cta_bg='#10243A',
    sb_bg='#10243A', sb_bd='1px solid rgba(34,211,238,.3)', sb_ink='#E6F6FF', sb_sub='#8FB0C7',
    sb_line='rgba(34,211,238,.25)', sb_hover='rgba(34,211,238,.1)',
    wal_bg='linear-gradient(135deg,#12304A,#0B1824)', wal_bd='1px solid rgba(34,211,238,.45)',
    wal_ink='#BFE6F5', wal_num='#67E8F9', wal_btn='#22D3EE', wal_btn_ink='#04222B',
    ft_bg='#070F18', ft_ink='#8FB0C7', ft_h='#22D3EE', ft_line='rgba(34,211,238,.2)', th_ink='#67E8F9',
    focus='rgba(34,211,238,.25)', card_bd='1px solid rgba(34,211,238,.28)', vis_bg='#0F2233',
    vis_bd='1px solid rgba(34,211,238,.5)', vis_r='0px', h1='54px',
)
CSS = """
h1,h2,h3{text-transform:uppercase;letter-spacing:.02em;}
body .hero,body .picker-hero{background-image:linear-gradient(rgba(34,211,238,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(34,211,238,.07) 1px,transparent 1px),linear-gradient(180deg,#0B1824,#12304A);background-size:44px 44px,44px 44px,auto;}
body .hero::before,body .picker-hero::before{content:'';position:absolute;left:0;right:0;bottom:0;height:3px;background:linear-gradient(90deg,#22D3EE,#F472B6);}
body .hero::after,body .picker-hero::after{content:'';position:absolute;left:0;top:-20%;width:100%;height:30%;background:linear-gradient(180deg,transparent,rgba(34,211,238,.08),transparent);animation:scn 7s linear infinite;pointer-events:none;}
@keyframes scn{from{transform:translateY(-100%);}to{transform:translateY(500%);}}
body .btn{clip-path:polygon(10px 0,100% 0,100% calc(100% - 10px),calc(100% - 10px) 100%,0 100%,0 10px);text-transform:uppercase;letter-spacing:.08em;}
body .card,body .stat-tile,body .step-card,body .benefit-card,body .picker-card,body .market-card,body .float-card,body .calc-box,body .stat-chip{clip-path:polygon(0 0,calc(100% - 18px) 0,100% 18px,100% 100%,18px 100%,0 calc(100% - 18px));}
body .stat-tile{border-left:0;border-top:3px solid var(--inv);}
body .stat-grid .stat-tile:nth-child(even){border-left:0;border-top-color:var(--bor);}
body .hero-visual{clip-path:polygon(0 0,calc(100% - 26px) 0,100% 26px,100% 100%,0 100%);}
body .eyebrow{border:1px solid var(--acc);text-transform:uppercase;letter-spacing:.14em;}
body .main-nav a{text-transform:uppercase;letter-spacing:.1em;font-size:12.5px;}
body .logo{background:#fff;padding:2px 10px;}
body .footer-brand .logo-full-img{background:none;}
body .wallet-actions input{background:#E6F6FF;}
""" + NAVFIX
