from d7_common import NAVFIX, base, poly, svg

NAME = 'prism'
TITLE = 'Prism - geometricky (fialova / limetkova)'
DESC = 'Svetly, izometricke bloky, sikme rezy a rovnobezniky. Investor: fialova, Dlznik: limetkova.'
FONTS = 'Sora:wght@500;600;700;800&family=Inter:wght@400;500;600'


def prism(x, yb, s, h, top, left, right):
    lt, ft, rt, bt = (x - s, yb - s / 2 - h), (x, yb - h), (x + s, yb - s / 2 - h), (x, yb - s - h)
    lb, fb, rb = (x - s, yb - s / 2), (x, yb), (x + s, yb - s / 2)
    return ('<polygon points="%s" fill="%s"/><polygon points="%s" fill="%s"/>'
            '<polygon points="%s" fill="%s"/>' % (poly([bt, rt, ft, lt]), top,
                                                  poly([lt, ft, fb, lb]), left,
                                                  poly([ft, rt, rb, fb]), right))


def build():
    b = '<polygon points="%s" fill="#F1ECFF"/>' % poly([(60, 20), (500, 20), (470, 400), (20, 400)])
    b += '<polygon points="%s" fill="#DDD6FE"/>' % poly([(400, 40), (470, 90), (400, 140), (330, 90)])
    xs, hs, yb, s = [110, 210, 310, 410], [50, 95, 145, 205], 360, 44
    pal = [('#C4B5FD', '#7C3AED', '#5B21B6'), ('#D9F99D', '#84CC16', '#4D7C0F')]
    for i, (x, h) in enumerate(zip(xs, hs)):
        t, l, r = pal[i % 2]
        b += prism(x, yb, s, h, t, l, r)
    pts = ' '.join('%g,%g' % (x, yb - h - s - 26) for x, h in zip(xs, hs))
    b += '<polyline points="%s" stroke="#1E1B3A" stroke-width="6"/>' % pts
    b += '<circle cx="%g" cy="%g" r="11" fill="#BEF264" stroke="#1E1B3A" stroke-width="5"/>' % (
        xs[-1], yb - hs[-1] - s - 26)
    return svg(520, 420, b)


ART = build()
VARS = base(
    fh="'Sora'", fb="'Inter'", bg='#FAF8FF', surface='#FFFFFF', soft='#F1ECFF', line='#E3DDF7',
    ink='#1E1B3A', muted='#5E5A7D', radius='0px', radius_sm='0px', rb='0px', shadow='none',
    brand='#6D28D9', brand_ink='#fff', brand_text='#6D28D9',
    inv='#6D28D9', inv_ink='#fff', inv_text='#6D28D9',
    bor='#84CC16', bor_ink='#1A2E05', bor_text='#4D7C0F',
    hdr_bg='#fff', hdr_ink='#1E1B3A', hdr_top='6px solid var(--acc)', hdr_bd='1px solid #E3DDF7',
    hero_bg='linear-gradient(135deg,#2E1065 0%,#6D28D9 62%,#8B5CF6 100%)', hero_bg_solid='#2E1065',
    hero_ink='#fff', hero_sub='#DDD6FE', hero_em='#BEF264', hero_chip='#BEF264', hero_chip_ink='#1A2E05',
    hero_btn='#BEF264', hero_btn_ink='#1A2E05', cta_bg='#2E1065',
    sb_bg='#fff', sb_bd='1px solid #E3DDF7', sb_ink='#1E1B3A', sb_sub='#6B6790', sb_line='#E3DDF7',
    sb_hover='#F1ECFF', wal_bg='linear-gradient(135deg,#2E1065,#6D28D9)', wal_ink='#EDE9FE', wal_num='#fff',
    wal_btn='#BEF264', wal_btn_ink='#1A2E05', ft_bg='#1E1B3A', ft_ink='#B9B5D6', ft_h='#BEF264',
    ft_line='rgba(255,255,255,.14)', th_ink='#1E1B3A', focus='rgba(109,40,217,.22)', card_bd='0',
    vis_bg='transparent', vis_bd='0', vis_r='0px', h1='56px',
)
CSS = """
body .hero,body .picker-hero{clip-path:polygon(0 0,100% 0,100% 92%,0 100%);padding-bottom:110px;}
body .hero::before,body .picker-hero::before{content:'';position:absolute;right:-50px;top:-70px;width:340px;height:340px;background:#BEF264;opacity:.2;clip-path:polygon(50% 0,100% 50%,50% 100%,0 50%);animation:spn 60s linear infinite;pointer-events:none;}
body .hero::after,body .picker-hero::after{content:'';position:absolute;left:-60px;bottom:30px;width:200px;height:200px;background:#fff;opacity:.08;clip-path:polygon(50% 0,100% 50%,50% 100%,0 50%);pointer-events:none;}
body .btn{border-radius:0;padding:13px 32px;clip-path:polygon(12px 0,100% 0,calc(100% - 12px) 100%,0 100%);}
body .card,body .stat-tile,body .step-card,body .benefit-card,body .picker-card,body .market-card,body .float-card,body .calc-box,body .stat-chip{border:0;border-left:5px solid var(--acc);background:#fff;box-shadow:none;clip-path:polygon(0 0,calc(100% - 22px) 0,100% 22px,100% 100%,0 100%);}
body .picker-card:hover,body .step-card:hover,body .benefit-card:hover{transform:translateY(-5px);}
body .role-card-investor{border-top:0;border-left-color:var(--inv);}
body .role-card-borrower{border-top:0;border-left-color:var(--bor);}
body .eyebrow,body .role-badge{clip-path:polygon(8px 0,100% 0,calc(100% - 8px) 100%,0 100%);padding:6px 18px;}
body .sidebar-nav-link{clip-path:polygon(0 0,calc(100% - 10px) 0,100% 100%,0 100%);}
body .dash-top h1{text-transform:none;font-weight:800;}
""" + NAVFIX
