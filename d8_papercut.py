from a8_papercut import build
from d7_common import NAVFIX, base

NAME = 'papercut'
TITLE = 'Papercut - vrstvy vystrihnuteho papiera (mint / korall)'
DESC = 'Mäkke vrstvy s tienmi ako papierova krajina. Investor: mint-zelena, Dlznik: korall.'
FONTS = 'Nunito:wght@500;700;800;900&family=Nunito+Sans:wght@400;600'
ART, EXTRA = build()
VARS = base(
    fh="'Nunito'", fb="'Nunito Sans'", bg='#F6F1E7', surface='#FFFFFF', soft='#EEF6F1',
    line='#E3DDD0', ink='#23332E', muted='#5E6E68', radius='18px', radius_sm='12px', rb='999px',
    shadow='0 8px 18px rgba(35,51,46,.18)', brand='#2F8F78', brand_ink='#fff', brand_text='#23775F',
    inv='#2F8F78', inv_ink='#fff', inv_text='#23775F', bor='#F4693F', bor_ink='#fff', bor_text='#C9461B',
    hdr_bg='#FFFFFF', hdr_ink='#23332E', hdr_top='0', hdr_bd='0',
    hero_bg='#BFE3D4', hero_bg_solid='#BFE3D4', hero_ink='#12362D', hero_sub='#25483F', hero_em='#E24E1B',
    hero_chip='#fff', hero_chip_ink='#23775F', hero_btn='#F4693F', hero_btn_ink='#fff', cta_bg='#FFD27A',
    sb_bg='#fff', sb_bd='0', sb_ink='#23332E', sb_sub='#5E6E68',
    sb_line='#E3DDD0', sb_hover='#EEF6F1', wal_bg='#2F8F78',
    wal_bd='0', wal_ink='#fff', wal_num='#FFE9B0', wal_btn='#FFD27A',
    wal_btn_ink='#23332E', ft_bg='#134D40', ft_ink='#CDE8DF', ft_h='#FFD27A', ft_line='rgba(255,255,255,.2)',
    th_ink='#23775F', focus='rgba(47,143,120,.3)', card_bd='0',
    inp_bd='2px solid #D5CFC0', vis_bg='transparent', vis_bd='0',
    vis_r='18px', h1='56px',
)
CSS = """
body{background:#F6F1E7;}
body .hero,body .picker-hero{background:url('img-sky.svg') top right/900px no-repeat,linear-gradient(#CDEBDD,#BFE3D4);position:relative;}
body .btn{font-weight:800;box-shadow:0 5px 0 rgba(0,0,0,.18),0 10px 14px rgba(0,0,0,.12);}
body .btn:active{transform:translateY(3px);box-shadow:0 2px 0 rgba(0,0,0,.18);}
body .site-header{box-shadow:0 6px 16px rgba(35,51,46,.15);position:relative;z-index:5;}
body .card,body .stat-tile,body .step-card,body .benefit-card,body .picker-card,body .market-card{position:relative;overflow:hidden;box-shadow:0 8px 18px rgba(35,51,46,.16),0 2px 0 #fff inset;}
body .step-card::after,body .benefit-card::after{content:'';position:absolute;right:-6px;top:-6px;width:76px;height:76px;background:no-repeat center/contain;pointer-events:none;}
body .step-card:nth-child(1)::after,body .benefit-card:nth-child(1)::after{background-image:url('img-ic1.svg');}
body .step-card:nth-child(2)::after,body .benefit-card:nth-child(2)::after{background-image:url('img-ic2.svg');}
body .step-card:nth-child(3)::after,body .benefit-card:nth-child(3)::after{background-image:url('img-ic3.svg');}
body .benefit-card:nth-child(4)::after{background-image:url('img-ic4.svg');}
body .cta-band{background:url('img-cta.svg') bottom center/100% auto no-repeat,#FFE9B0;color:#23332E;box-shadow:0 12px 24px rgba(35,51,46,.2);padding-bottom:110px;}
body .cta-band h2{color:#23332E;}
body .wallet-card{background:url('img-ic1.svg') right 16px bottom -24px/140px no-repeat,#2F8F78;box-shadow:0 10px 22px rgba(35,51,46,.3);}
body .site-footer{background:url('img-foot.svg') top center/cover no-repeat,#134D40;padding-top:150px;}
body .stat-tile{border-left:0;border-bottom:6px solid var(--inv);}
body .stat-grid .stat-tile:nth-child(even){border-bottom-color:var(--bor);}
body .hero-visual{background:var(--vis-img) no-repeat center/100%;}
body .eyebrow{box-shadow:0 3px 6px rgba(0,0,0,.15);}
""" + NAVFIX
