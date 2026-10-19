"""Spolocne CSS domovskej stranky v2 (sablona s tokenmi). @P = karta, @G = grid kariet, @CTA = cta-band."""

COMMON = r"""
body.home-page .picker-hero{background:url('img-home-hero.svg') center/cover no-repeat,var(--hero-bg,{BG});padding:96px 0 124px;}
body.home-page .picker-head{margin-bottom:54px;}
body.home-page .picker-hero h1{color:var(--hero-ink,{INK});}
body.home-page .picker-hero .picker-head p,body.home-page .picker-hero .lead{color:var(--hero-sub,{MUT});}
body.home-page .picker-hero .eyebrow{background:var(--hero-chip,{INV});color:var(--hero-chip-ink,{INVT});}
body.home-page .picker-head h1{font-size:clamp(38px,5.2vw,64px);}
@P{position:relative;display:flex;flex-direction:column;overflow:hidden;background:{SUR};color:{INK};border:{CB};border-radius:{CR};box-shadow:{CS};padding:0;text-decoration:none;transition:transform .2s,box-shadow .2s;}
@P:hover{transform:translateY(-8px);}
@P::before{content:'';display:block;background:url('img-home-inv.svg') center/contain no-repeat;}
@P.role-card-borrower::before{background-image:url('img-home-bor.svg');}
@P::after{content:'';position:absolute;left:0;right:0;top:0;height:9px;background:{INV};z-index:2;}
@P.role-card-borrower::after{background:{BOR};}
@P h2{color:{INK};font-size:30px;margin:0 0 10px;}
@P p{color:{MUT};font-size:16.5px;line-height:1.55;margin:0;}
@P .picker-icon{margin-top:26px;margin-bottom:14px;}
@P .picker-cta{display:inline-flex;align-items:center;gap:12px;margin-top:22px;padding:16px 30px;border-radius:{RB};font-weight:800;font-size:16px;align-self:flex-start;justify-self:start;box-shadow:0 12px 24px -10px rgba(0,0,0,.45);transition:gap .15s,transform .15s;}
@P.role-card-investor .picker-cta{background:{INV};color:{INVT};}
@P.role-card-borrower .picker-cta{background:{BOR};color:{BORT};}
@P:hover .picker-cta{gap:20px;}
@P .picker-stat{display:flex;align-items:baseline;gap:10px;margin-top:20px;padding-top:0;border-top:0;}
@P .picker-stat b{display:inline;font-size:30px;color:{INK};}
@P .picker-stat span{color:{MUT};}
@P .picker-stat::before{content:'';width:11px;height:11px;border-radius:50%;background:{INV};align-self:center;flex:none;}
@P.role-card-borrower .picker-stat::before{background:{BOR};}
{FLAV}
body.home-page .picker-links{margin-top:48px;}
body.home-page .picker-links a{display:inline-flex;align-items:center;gap:8px;padding:14px 30px;border:2px solid currentColor;border-radius:{RB};font-weight:800;color:var(--hero-ink,{INK});background:rgba(255,255,255,.08);backdrop-filter:blur(6px);}
body.home-page main>section:nth-of-type(2){background:url('img-home-bg.svg') center/cover no-repeat,{BG};padding:100px 0;}
body.home-page .step-card{position:relative;padding:34px 28px 32px;text-align:left;overflow:hidden;}
body.home-page .step-card::after{content:none;}
body.home-page .step-card::before{content:'';display:block;width:88px;height:88px;margin-bottom:18px;background:no-repeat center/contain;}
body.home-page .step-card:nth-child(1)::before{background-image:url('img-home-s1.svg');}
body.home-page .step-card:nth-child(2)::before{background-image:url('img-home-s2.svg');}
body.home-page .step-card:nth-child(3)::before{background-image:url('img-home-s3.svg');}
body.home-page .step-num{position:absolute;top:18px;right:18px;width:40px;height:40px;font-size:17px;}
body.home-page .stats-band{background:url('img-home-stats.svg') center/cover no-repeat,linear-gradient(120deg,{INVD},{INVDD});color:#fff;padding:84px 0;}
body.home-page .stats-grid b{color:#fff;font-size:clamp(34px,4.4vw,58px);background:none;-webkit-text-fill-color:#fff;}
body.home-page .stats-grid span{color:rgba(255,255,255,.88);}
@CTA{position:relative;overflow:hidden;background:url('img-home-cta.svg') center/cover no-repeat,linear-gradient(135deg,{INVDD},{INVD});color:#fff;padding:110px 0;}
@CTA .cta-inner{position:relative;z-index:1;}
@CTA h2,@CTA p{color:#fff;}
@CTA .btn-lg{padding:18px 38px;font-size:17px;font-weight:800;border:3px solid #fff;border-radius:{RB};box-shadow:0 16px 30px -10px rgba(0,0,0,.55);}
@CTA .btn-lg::after{content:'\2192';margin-left:8px;}
@CTA .btn-investor{background:{INV};color:{INVT};}
@CTA .btn-outline-borrower{background:{BOR};color:{BORT};}
"""

FLAVOR = {
    'soft': r"""@P{--x:0;}""",
    'geo': r"""@P{--x:0;}@P:hover{transform:translate(4px,4px);box-shadow:5px 5px 0 {INK};}""",
    'pop': r"""@P:hover{transform:translate(4px,4px);box-shadow:4px 4px 0 {INK};}@P .picker-cta{border:3px solid {INK};box-shadow:4px 4px 0 {INK};}""",
    'line': r"""@P{background:{SURA};}""",
    'glow': r"""@P.role-card-borrower{border-color:{BORA7};box-shadow:0 0 38px {BORA3};}@P .picker-cta{box-shadow:0 0 24px {INVA3};}""",
}

STYLE_VALUES = {
    'soft': dict(CB='0', CR='var(--radius,24px)', CS='0 18px 40px -12px rgba(0,0,0,.28)'),
    'geo': dict(CB='3px solid {INK}', CR='0', CS='9px 9px 0 {INK}'),
    'pop': dict(CB='4px solid {INK}', CR='14px', CS='8px 8px 0 {INK}'),
    'line': dict(CB='2px solid {INKA5}', CR='8px', CS='0 0 0 transparent'),
    'glow': dict(CB='1px solid {INVA7}', CR='10px', CS='0 0 38px {INVA3}'),
}
