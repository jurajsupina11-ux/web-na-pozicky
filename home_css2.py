"""Rozlozenia kariet domovskej stranky: A split, B wide, C stagger, D solid, E orbit + mobil."""

LAYOUT = {}

LAYOUT['A'] = r"""
@G{display:grid;grid-template-columns:1fr 1fr;gap:34px;max-width:1040px;margin:0 auto;}
@P{padding:0 38px 40px;}
@P::before{height:240px;margin:0 -38px 8px;}
@P.role-card-investor::before{background-color:{INVA14};}
@P.role-card-borrower::before{background-color:{BORA14};}
@P .picker-icon{margin-top:14px;}
"""

LAYOUT['B'] = r"""
@G{display:grid;grid-template-columns:1fr;gap:34px;max-width:1040px;margin:0 auto;}
@P{display:grid;grid-template-columns:1fr 360px;column-gap:34px;align-items:center;padding:46px 50px;}
@P>*{grid-column:1;}
@P::before{grid-column:2;grid-row:1/7;height:290px;}
@P.role-card-investor{grid-template-columns:360px 1fr;}
@P.role-card-investor>*{grid-column:2;}
@P.role-card-investor::before{grid-column:1;}
"""

LAYOUT['C'] = r"""
@G{display:grid;grid-template-columns:1fr 1fr;gap:34px;max-width:1080px;margin:0 auto;align-items:start;}
@P{padding:48px 38px 0;min-height:600px;}
@P::before{order:9;height:260px;margin:auto -14px 0;background-position:center bottom;}
@P.role-card-investor{margin-top:74px;}
"""

LAYOUT['D'] = r"""
@G{display:grid;grid-template-columns:1fr 1fr;gap:0;max-width:1120px;margin:0 auto;}
@P{padding:50px 42px 320px;border-radius:{CR};}
@P.role-card-borrower{background:{BOR};color:{BORT};}
@P.role-card-investor{background:{INV};color:{INVT};}
@P h2,@P p,@P .picker-stat b,@P .picker-stat span{color:inherit;}
@P::before{position:absolute;left:0;right:0;bottom:0;height:300px;pointer-events:none;}
@P::after{background:rgba(255,255,255,.4);}
@P.role-card-investor .picker-cta,@P.role-card-borrower .picker-cta{background:#fff;color:#14110F;}
@P .picker-stat::before{background:currentColor;}
@P .picker-icon .ic{background:rgba(255,255,255,.22);color:inherit;}
"""

LAYOUT['E'] = r"""
@G{display:grid;grid-template-columns:1fr 1fr;gap:110px 34px;max-width:1040px;margin:84px auto 0;}
@P{overflow:visible;padding:160px 34px 40px;text-align:center;align-items:center;border-top:9px solid {INV};}
@P.role-card-borrower{border-top-color:{BOR};}
@P::after{display:none;}
@P::before{position:absolute;top:-76px;left:50%;width:240px;height:240px;margin-left:-120px;border-radius:50%;background:url('img-home-inv.svg') center/80% no-repeat,{SUR};border:{CB};box-shadow:0 14px 30px -10px rgba(0,0,0,.35);}
@P.role-card-borrower::before{background:url('img-home-bor.svg') center/80% no-repeat,{SUR};}
@P .picker-icon{display:none;}
@P .picker-cta{align-self:center;justify-self:center;}
@P .picker-stat{justify-content:center;}
"""

MOBILE = r"""
body.home-page .picker-hero::before,body.home-page .picker-hero::after{z-index:0;pointer-events:none;}
body.home-page .picker-hero .picker-links{position:relative;z-index:2;}
@media(max-width:820px){
  body.home-page .picker-hero::after{width:10% !important;opacity:.55;}
  body.home-page .picker-hero::before{opacity:.6;}
  body.home-page .picker-hero{padding:64px 0 90px;}
  @G{grid-template-columns:1fr !important;gap:26px !important;margin-top:0;}
  @P{grid-template-columns:1fr !important;padding-left:24px;padding-right:24px;margin-top:0 !important;min-height:0;}
  @P>*{grid-column:1 !important;}
  @P::before{grid-column:1 !important;grid-row:auto !important;order:-1;height:210px;margin-bottom:12px;}
  @P.role-card-investor{padding-left:24px;}
  @P h2{font-size:25px;}
  body.home-page .step-card::before{width:70px;height:70px;}
  body.home-page .stats-band,@CTA{padding:60px 0;}
  @CTA .btn-lg{width:100%;padding:16px 20px;}
}
@media(max-width:820px){
  body.home-page .layout-d-fix{display:none;}
}
"""

MOBILE_D = r"""
@media(max-width:820px){@P{padding-bottom:290px !important;}@P::before{position:absolute !important;order:0 !important;left:0;right:0;bottom:0;height:260px !important;margin:0 !important;}}
"""

MOBILE_E = r"""
@media(max-width:820px){@G{margin-top:70px !important;gap:110px !important;}@P{padding-top:160px !important;}@P::before{position:absolute !important;order:0 !important;height:240px !important;margin:0 0 0 -120px !important;top:-76px;}}
"""

MOBILE_A = r"""
@media(max-width:820px){@P{padding-left:24px !important;padding-right:24px !important;}@P::before{margin-left:-24px !important;margin-right:-24px !important;}}
"""
