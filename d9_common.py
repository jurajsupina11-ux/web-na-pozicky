"""Spolocne CSS pre financne dizajny v9: obrazky v kartach, pozadia sekcii, paticka."""
from d7_common import NAVFIX  # noqa: F401


def img_css(foot_bg, cta_bg, wal_bg, ic_op=1, ic_size=64):
    return """
body .step-card,body .benefit-card,body .card,body .stat-tile,body .picker-card,body .market-card{position:relative;overflow:hidden;}
body .step-card::after,body .benefit-card::after{content:'';position:absolute;right:14px;top:14px;width:%(s)dpx;height:%(s)dpx;opacity:%(o)s;background:no-repeat center/contain;pointer-events:none;}
body .step-card:nth-child(1)::after,body .benefit-card:nth-child(1)::after{background-image:url('img-ic1.svg');}
body .step-card:nth-child(2)::after,body .benefit-card:nth-child(2)::after{background-image:url('img-ic2.svg');}
body .step-card:nth-child(3)::after,body .benefit-card:nth-child(3)::after{background-image:url('img-ic3.svg');}
body .benefit-card:nth-child(4)::after{background-image:url('img-ic4.svg');}
body .cta-band{background:url('img-coins.svg') right 4%% center/220px no-repeat,url('img-wave.svg') bottom/cover no-repeat,%(c)s;}
body .wallet-card{background:url('img-chart.svg') right bottom/60%% auto no-repeat,%(w)s;}
body .site-footer{background:url('img-wave.svg') top center/cover no-repeat,%(f)s;padding-top:120px;}
body .stat-tile{border-left:0;border-top:4px solid var(--inv);}
body .stat-grid .stat-tile:nth-child(even){border-top-color:var(--bor);}
body .hero-visual{background:var(--vis-img) no-repeat center/100%%;}
body .logo{background:#fff;padding:3px 10px;border-radius:10px;}
@media(max-width:700px){body .step-card::after,body .benefit-card::after{width:48px;height:48px;}body .cta-band{background-size:130px,cover,auto;}}
""" % {'s': ic_size, 'o': ic_op, 'c': cta_bg, 'w': wal_bg, 'f': foot_bg}
