from a8_blueprint import build
from d7_common import NAVFIX, base

NAME = 'blueprint'
TITLE = 'Blueprint - technicky vykres (modra / zlta)'
DESC = 'Kresliace pauzovanie: modry vykres, kotovacie ciary, ziadne zaoblenia. Investor: cyan, Dlznik: zlta.'
FONTS = 'Barlow+Condensed:wght@500;600;700&family=Barlow:wght@400;500;600&family=Roboto+Mono:wght@400;500'
ART, EXTRA = build()
VARS = base(
    fh="'Barlow Condensed'", fb="'Barlow'", bg='#0E3A7A', surface='#12468F', soft='#0F3F82',
    line='rgba(207,232,255,.4)', ink='#EAF4FF', muted='#A9C6EA', radius='0px', radius_sm='0px', rb='0px',
    shadow='none', brand='#CFE8FF', brand_ink='#0E3A7A', brand_text='#CFE8FF',
    inv='#7FE3FF', inv_ink='#06284F', inv_text='#7FE3FF', bor='#FFD166', bor_ink='#3A2A00', bor_text='#FFD166',
    hdr_bg='#0B2E64', hdr_ink='#EAF4FF', hdr_top='4px solid var(--acc)', hdr_bd='1px dashed rgba(207,232,255,.5)',
    hero_bg='#0B2E64', hero_bg_solid='#0B2E64', hero_ink='#fff', hero_sub='#B9D3F0', hero_em='#FFD166',
    hero_chip='transparent', hero_chip_ink='#FFD166', hero_btn='#FFD166', hero_btn_ink='#3A2A00', cta_bg='#0B2E64',
    sb_bg='#0B2E64', sb_bd='1px dashed rgba(207,232,255,.55)', sb_ink='#EAF4FF', sb_sub='#9DBAE0',
    sb_line='rgba(207,232,255,.3)', sb_hover='rgba(207,232,255,.1)', wal_bg='#0B2E64',
    wal_bd='1px dashed rgba(207,232,255,.6)', wal_ink='#CFE8FF', wal_num='#FFD166', wal_btn='#FFD166',
    wal_btn_ink='#3A2A00', ft_bg='#08224B', ft_ink='#9DBAE0', ft_h='#FFD166', ft_line='rgba(207,232,255,.25)',
    th_ink='#7FE3FF', focus='rgba(127,227,255,.3)', card_bd='1px dashed rgba(207,232,255,.55)',
    inp_bd='1px solid rgba(207,232,255,.6)', vis_bg='transparent', vis_bd='1px dashed rgba(207,232,255,.6)',
    vis_r='0px', h1='60px',
)
CSS = """
body{background:#0E3A7A url('img-grid.svg') 0 0/80px 80px;}
h1,h2,h3{text-transform:uppercase;letter-spacing:.03em;}
body .hero,body .picker-hero{background:url('img-crane.svg') no-repeat 94% 8%/260px,url('img-grid.svg') 0 0/80px 80px,#0B2E64;}
body .hero::before,body .picker-hero::before{content:'';position:absolute;left:0;right:0;bottom:0;height:3px;background:repeating-linear-gradient(90deg,#CFE8FF 0 12px,transparent 12px 20px);}
body .btn{text-transform:uppercase;letter-spacing:.1em;font-family:'Roboto Mono',monospace;font-size:12.5px;}
body .btn-primary{box-shadow:5px 5px 0 rgba(0,0,0,.35);}
body .main-nav a,body .eyebrow{font-family:'Roboto Mono',monospace;text-transform:uppercase;letter-spacing:.08em;font-size:12px;}
body .eyebrow{border:1px dashed var(--acc);}
body .card,body .stat-tile,body .step-card,body .benefit-card,body .picker-card,body .market-card{position:relative;overflow:hidden;}
body .step-card::after,body .benefit-card::after{content:'';position:absolute;right:-8px;bottom:-8px;width:96px;height:96px;opacity:.55;background:no-repeat center/contain;pointer-events:none;}
body .step-card:nth-child(1)::after,body .benefit-card:nth-child(1)::after{background-image:url('img-ic1.svg');}
body .step-card:nth-child(2)::after,body .benefit-card:nth-child(2)::after{background-image:url('img-ic2.svg');}
body .step-card:nth-child(3)::after,body .benefit-card:nth-child(3)::after{background-image:url('img-ic3.svg');}
body .benefit-card:nth-child(4)::after{background-image:url('img-ic4.svg');}
body .cta-band{background:url('img-crane.svg') no-repeat 96% 100%/300px,#0B2E64;border:1px dashed rgba(207,232,255,.6);}
body .wallet-card{background:url('img-ic1.svg') no-repeat right 20px bottom -20px/150px,#0B2E64;}
body .site-footer{background:url('img-foot.svg') no-repeat center top/auto 140px,#08224B;padding-top:160px;border-top:0;}
body .stat-tile{border-left:0;border-top:3px solid var(--inv);}
body .stat-grid .stat-tile:nth-child(even){border-left:0;border-top-color:var(--bor);}
body .logo{background:#fff;padding:2px 10px;}
body .footer-brand .logo-full-img{background:none;}
body .wallet-actions input{background:#EAF4FF;}
body .hero-visual{background:rgba(255,255,255,.04) var(--vis-img) no-repeat center/92%;}
""" + NAVFIX
