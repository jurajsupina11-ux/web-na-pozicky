from d6_common import art, base

NAME = 'ocean'
TITLE = 'Ocean - korporatna modra'
DESC = 'Dôveryhodna korporatna modra, farebne pruhy a ostre bloky. Investor: azurova, Dlznik: jantarova.'
FONTS = 'Plus+Jakarta+Sans:wght@500;600;700;800'
ART = art('#DCEBFA', '#0A66C2', '#0B2545', '#F2A71B', '#0B2545')
VARS = base(
    fh="'Plus Jakarta Sans'", fb="'Plus Jakarta Sans'", bg='#F2F6FB', surface='#FFFFFF', soft='#E6EEF8',
    line='#D5E0EE', ink='#0B2545', muted='#51647E', radius='12px', radius_sm='8px', rb='8px',
    shadow='0 10px 24px -16px rgba(11,37,69,.35)',
    brand='#0B2545', brand_ink='#fff', brand_text='#0B2545',
    inv='#0A66C2', inv_ink='#fff', inv_text='#0A66C2',
    bor='#F2A71B', bor_ink='#2B1B00', bor_text='#A86A00',
    hdr_bg='#fff', hdr_ink='#0B2545', hdr_top='6px solid var(--acc)', hdr_bd='1px solid #D5E0EE',
    hero_bg='linear-gradient(120deg,#0B2545 0%,#13417A 60%,#0A66C2 100%)', hero_bg_solid='#0B2545',
    hero_ink='#fff', hero_sub='#C6D6EC', hero_em='#7CC0FF', hero_chip='#F2A71B', hero_chip_ink='#2B1B00',
    hero_btn='#F2A71B', hero_btn_ink='#2B1B00', cta_bg='linear-gradient(120deg,#0B2545,#0A66C2)',
    sb_bg='#0B2545', sb_ink='#E6EEF8', sb_sub='#8FA6C6', sb_line='rgba(255,255,255,.15)', sb_hover='rgba(255,255,255,.08)',
    wal_bg='linear-gradient(120deg,#0B2545,#0A66C2)', wal_ink='#DCEBFA', wal_num='#fff',
    wal_btn='#F2A71B', wal_btn_ink='#2B1B00', ft_bg='#08192F', ft_ink='#8FA6C6', ft_h='#fff',
    ft_line='rgba(255,255,255,.14)', th_bg='#E6EEF8', th_ink='#0B2545', focus='rgba(10,102,194,.25)',
    vis_bg='rgba(255,255,255,.1)', vis_bd='1px solid rgba(255,255,255,.3)', vis_r='16px',
)
CSS = """
body .hero::before,body .picker-hero::before{content:'';position:absolute;right:0;top:0;bottom:0;width:36%;background:repeating-linear-gradient(115deg,rgba(255,255,255,.06) 0 38px,transparent 38px 76px);pointer-events:none;}
body .hero::after,body .picker-hero::after{content:'';position:absolute;left:0;right:0;bottom:0;height:6px;background:linear-gradient(90deg,#F2A71B,#0A66C2,#7CC0FF);}
body .dash-sidebar .sidebar-user span,body .dash-sidebar .sidebar-user b{color:#fff;}
body .stat-tile{border-left:0;border-top:5px solid var(--inv);}
body .stat-grid .stat-tile:nth-child(even){border-left:0;border-top-color:var(--bor);}
body .btn-primary{box-shadow:0 8px 16px -10px rgba(11,37,69,.7);}
body .picker-hero .picker-card h2{color:#0B2545;}
body .hero-visual{background:rgba(255,255,255,.12) var(--vis-img) no-repeat center/88%;}
"""
