from a8_gazette import build
from d7_common import NAVFIX, base

NAME = 'gazette'
TITLE = 'Gazette - noviny a rastrove obrazky (cierna / cervena)'
DESC = 'Papier, dvojite linky, serifove titulky a rastrove bodky. Investor: cierna/zelena, Dlznik: cervena.'
FONTS = 'Playfair+Display:wght@600;700;900&family=Source+Serif+4:wght@400;600&family=Inter:wght@500;600'
ART, EXTRA = build()
VARS = base(
    fh="'Playfair Display'", fb="'Source Serif 4'", bg='#F4EEDF', surface='#FBF7EC', soft='#EBE4D1',
    line='#1A1A1A', ink='#1A1A1A', muted='#4B463B', radius='0px', radius_sm='0px', rb='0px',
    shadow='none', brand='#1A1A1A', brand_ink='#F4EEDF', brand_text='#1A1A1A',
    inv='#1F5E3A', inv_ink='#F4EEDF', inv_text='#1F5E3A', bor='#B3261E', bor_ink='#F4EEDF', bor_text='#B3261E',
    hdr_bg='#F4EEDF', hdr_ink='#1A1A1A', hdr_top='0', hdr_bd='3px double #1A1A1A',
    hero_bg='#F4EEDF', hero_bg_solid='#F4EEDF', hero_ink='#1A1A1A', hero_sub='#3A362D', hero_em='#B3261E',
    hero_chip='#1A1A1A', hero_chip_ink='#F4EEDF', hero_btn='#1A1A1A', hero_btn_ink='#F4EEDF', cta_bg='#1A1A1A',
    sb_bg='#EBE4D1', sb_bd='2px solid #1A1A1A', sb_ink='#1A1A1A', sb_sub='#4B463B',
    sb_line='#1A1A1A', sb_hover='rgba(26,26,26,.08)', wal_bg='#1A1A1A',
    wal_bd='3px double #1A1A1A', wal_ink='#F4EEDF', wal_num='#FFFFFF', wal_btn='#F4EEDF',
    wal_btn_ink='#1A1A1A', ft_bg='#1A1A1A', ft_ink='#CFC8B4', ft_h='#F4EEDF', ft_line='rgba(244,238,223,.3)',
    th_ink='#1A1A1A', focus='rgba(179,38,30,.3)', card_bd='1px solid #1A1A1A',
    inp_bd='1px solid #1A1A1A', vis_bg='transparent', vis_bd='0',
    vis_r='0px', h1='62px',
)
CSS = """
body{background:#F4EEDF url('img-paper.svg') 0 0/400px 400px;}
h1,h2,h3{letter-spacing:-.01em;}
h1{line-height:1.02;}
body .hero,body .picker-hero{background:url('img-ht.svg') right top/340px no-repeat,#F4EEDF;border-bottom:3px double #1A1A1A;opacity:1;}
body .hero::after,body .picker-hero::after{opacity:.1;}
body .btn{font-family:'Inter',sans-serif;text-transform:uppercase;letter-spacing:.12em;font-size:12px;font-weight:600;border:2px solid #1A1A1A;}
body .btn-primary{box-shadow:4px 4px 0 rgba(26,26,26,.35);}
body .main-nav a{font-family:'Inter',sans-serif;text-transform:uppercase;letter-spacing:.1em;font-size:11.5px;}
body .eyebrow{font-family:'Inter',sans-serif;text-transform:uppercase;letter-spacing:.14em;}
body .site-header::after{content:'';display:block;height:20px;background:url('img-rule.svg') center/auto 20px repeat-x;}
body .card,body .stat-tile,body .step-card,body .benefit-card,body .picker-card,body .market-card{position:relative;overflow:hidden;border:1px solid #1A1A1A;box-shadow:5px 5px 0 rgba(26,26,26,.2);}
body .step-card::after,body .benefit-card::after{content:'';position:absolute;right:-8px;top:-8px;width:80px;height:80px;background:no-repeat center/contain;pointer-events:none;opacity:.85;}
body .step-card:nth-child(1)::after,body .benefit-card:nth-child(1)::after{background-image:url('img-ic1.svg');}
body .step-card:nth-child(2)::after,body .benefit-card:nth-child(2)::after{background-image:url('img-ic2.svg');}
body .step-card:nth-child(3)::after,body .benefit-card:nth-child(3)::after{background-image:url('img-ic3.svg');}
body .benefit-card:nth-child(4)::after{background-image:url('img-ic4.svg');}
body .cta-band{background:url('img-ht.svg') right center/300px no-repeat,#1A1A1A;color:#F4EEDF;border:3px double #F4EEDF;outline:2px solid #1A1A1A;}
body .wallet-card{background:url('img-ic1.svg') right 14px bottom -26px/150px no-repeat,#1A1A1A;}
body .site-footer{background:url('img-foot.svg') top center/1400px 100px repeat-x,#1A1A1A;padding-top:130px;}
body .stat-tile{border-left:0;border-top:6px solid var(--inv);}
body .stat-grid .stat-tile:nth-child(even){border-top-color:var(--bor);}
body .logo{background:#fff;padding:2px 10px;}
body .hero-visual{background:var(--vis-img) no-repeat center/94%;}
body .hero-visual,body .hero-art{filter:contrast(1.05);}
""" + NAVFIX
