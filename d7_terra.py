from d7_common import NAVFIX, base, svg

NAME = 'terra'
TITLE = 'Terra - zemita, oblúky (olivova / terakota)'
DESC = 'Piesok, oblúky a slnko, teple zemite farby. Investor: olivova, Dlznik: terakota.'
FONTS = 'Young+Serif&family=Karla:wght@400;500;600;700'


def arch(x, y, w, h, fill, extra=''):
    r = w / 2
    return ('<path d="M%g,%gV%gA%g,%g 0 0 1 %g,%gV%gZ" fill="%s" %s/>'
            % (x, y + h, y + r, r, r, x + w, y + r, y + h, fill, extra))


def build():
    b = '<rect width="520" height="420" rx="0" fill="#F6EFE4"/>'
    b += '<circle cx="390" cy="130" r="74" fill="#E8A33D"/>'
    b += '<circle cx="390" cy="130" r="104" stroke="#E8A33D" stroke-opacity=".4" stroke-width="3"/>'
    b += arch(50, 170, 130, 230, '#C4552B') + arch(74, 200, 82, 200, '#E7D3B5')
    b += arch(200, 110, 130, 290, '#4D5F2A') + arch(224, 140, 82, 260, '#6B7D3E')
    b += arch(350, 220, 130, 180, '#E7D3B5') + arch(374, 250, 82, 150, '#C4552B')
    b += '<path d="M0 392 Q130 360 260 388 T520 380 V420 H0Z" fill="#4D5F2A" fill-opacity=".25"/>'
    b += '<g stroke="#3B2A1E" stroke-width="4"><path d="M95 150c8-10 16-10 24 0M440 70c8-10 16-10 24 0"/></g>'
    return svg(520, 420, b)


ART = build()
VARS = base(
    fh="'Young Serif'", fb="'Karla'", bg='#F6EFE4', surface='#FFFBF5', soft='#EFE3D0', line='#E2D3BA',
    ink='#3B2A1E', muted='#7A6652', radius='28px', radius_sm='16px', rb='999px',
    shadow='0 18px 36px -26px rgba(59,42,30,.5)',
    brand='#3B2A1E', brand_ink='#fff', brand_text='#3B2A1E',
    inv='#4D5F2A', inv_ink='#fff', inv_text='#4D5F2A',
    bor='#C4552B', bor_ink='#fff', bor_text='#B4441A',
    hdr_bg='#F6EFE4', hdr_ink='#3B2A1E', hdr_top='0', hdr_bd='1px solid #E2D3BA',
    hero_bg='#EFE3D0', hero_bg_solid='#EFE3D0', hero_ink='#3B2A1E', hero_sub='#6B5842', hero_em='#C4552B',
    hero_chip='#4D5F2A', hero_chip_ink='#fff', hero_btn='#3B2A1E', hero_btn_ink='#F6EFE4', cta_bg='#EFE3D0',
    sb_bg='#3B2A1E', sb_ink='#F6EFE4', sb_sub='#CDB89A', sb_line='rgba(246,239,228,.2)', sb_hover='rgba(246,239,228,.1)',
    wal_bg='#4D5F2A', wal_ink='#EFE9CF', wal_num='#FFF3D6', wal_btn='#F6EFE4', wal_btn_ink='#3B2A1E',
    ft_bg='#3B2A1E', ft_ink='#D9C7AA', ft_h='#E8A33D', ft_line='rgba(246,239,228,.2)',
    focus='rgba(77,95,42,.25)', vis_bg='#EFE3D0', vis_bd='0', vis_r='240px 240px 28px 28px', h1='58px',
)
CSS = """
body .hero::before,body .picker-hero::before{content:'';position:absolute;right:6%;top:-70px;width:260px;height:260px;border-radius:50%;background:#E8A33D;opacity:.8;animation:flt 9s ease-in-out infinite;pointer-events:none;}
body .hero::after,body .picker-hero::after{content:'';position:absolute;left:-40px;bottom:-70px;width:380px;height:190px;border-radius:380px 380px 0 0;background:#4D5F2A;opacity:.2;pointer-events:none;}
body .picker-card{border-radius:170px 170px 28px 28px;padding:76px 38px 40px;text-align:center;border-top:6px solid var(--inv);}
body .role-card-borrower{border-top-color:var(--bor);}
body .picker-icon{display:flex;justify-content:center;}
body .hero-visual{border-radius:240px 240px 28px 28px;background:#EFE3D0 var(--vis-img) no-repeat center bottom/92%;min-height:470px;}
body .step-card,body .benefit-card{border-radius:90px 28px 28px 28px;padding-top:34px;}
body .stat-tile{border-left:0;border-bottom:6px solid var(--inv);border-radius:28px 28px 6px 6px;}
body .stat-grid .stat-tile:nth-child(even){border-left:0;border-bottom-color:var(--bor);}
body .btn{box-shadow:0 8px 16px -10px rgba(59,42,30,.7);}
body h1,body h2,body h3{font-weight:400;}
body .wallet-card{border-radius:28px 28px 28px 120px;}
""" + NAVFIX
