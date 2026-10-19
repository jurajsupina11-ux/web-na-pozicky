from d6_common import art, base

NAME = 'zen'
TITLE = 'Zen - mekky pastel'
DESC = 'Svetly, vzdusny, pastelove blobky, velke zaoblenia. Investor: saliova zelena, Dlznik: broskyna.'
FONTS = 'DM+Serif+Display&family=DM+Sans:wght@400;500;600;700'
ART = art('#EAF3EC', '#7FB99A', '#E9B8A0', '#F3D9A4', '#2F4A3C')
VARS = base(
    fh="'DM Serif Display'", fb="'DM Sans'", bg='#FBF8F3', surface='#FFFFFF', soft='#F1ECE3',
    line='#E8E0D2', ink='#2F4A3C', muted='#6C7C72', radius='34px', radius_sm='20px', rb='999px',
    shadow='0 22px 44px -30px rgba(47,74,60,.45)',
    brand='#2F4A3C', brand_ink='#fff', brand_text='#2F4A3C',
    inv='#7FB99A', inv_ink='#17382A', inv_text='#3E7A5C',
    bor='#E9A47F', bor_ink='#4A2210', bor_text='#B8623A',
    hdr_bg='#FBF8F3', hdr_ink='#2F4A3C', hdr_top='0', hdr_bd='1px solid #E8E0D2',
    hero_bg='linear-gradient(160deg,#EAF3EC 0%,#FBF3EA 100%)', hero_bg_solid='#EAF3EC',
    hero_ink='#2F4A3C', hero_sub='#5F7367', hero_em='#3E7A5C', hero_chip='#fff', hero_chip_ink='#2F4A3C',
    hero_btn='#2F4A3C', hero_btn_ink='#fff', cta_bg='#EAF3EC',
    sb_bg='#fff', sb_bd='1px solid #E8E0D2', sb_ink='#2F4A3C', sb_sub='#7B8B80', sb_line='#E8E0D2', sb_hover='#F1ECE3',
    wal_bg='linear-gradient(135deg,#CFE6D8,#F6DCCB)', wal_ink='#2F4A3C', wal_num='#2F4A3C',
    wal_btn='#2F4A3C', wal_btn_ink='#fff', ft_bg='#2F4A3C', ft_ink='#C9D8CE', ft_h='#F3D9A4',
    ft_line='rgba(255,255,255,.18)', focus='rgba(127,185,154,.35)',
    vis_bg='#fff', vis_bd='0', vis_r='44px', h1='56px',
)
CSS = """
h1,h2,h3{font-weight:400;}
body .hero::before,body .picker-hero::before{content:'';position:absolute;right:-90px;top:-80px;width:380px;height:380px;border-radius:62% 38% 55% 45%/48% 58% 42% 52%;background:#CFE6D8;animation:blobz 16s ease-in-out infinite;pointer-events:none;}
body .hero::after,body .picker-hero::after{content:'';position:absolute;left:-80px;bottom:-90px;width:300px;height:300px;border-radius:45% 55% 40% 60%/55% 45% 55% 45%;background:#F6DCCB;animation:blobz 20s ease-in-out infinite reverse;pointer-events:none;}
@keyframes blobz{0%,100%{border-radius:62% 38% 55% 45%/48% 58% 42% 52%;transform:rotate(0);}50%{border-radius:40% 60% 45% 55%/58% 42% 58% 42%;transform:rotate(14deg);}}
body .btn{box-shadow:0 8px 18px -10px rgba(47,74,60,.6);}
body .picker-card:hover,body .card:hover{box-shadow:0 30px 50px -28px rgba(47,74,60,.55);}
body .stat-tile{border-left:0;border-top:6px solid var(--inv);}
body .stat-grid .stat-tile:nth-child(even){border-top-color:var(--bor);border-left:0;}
body .hero-visual{background:#fff var(--vis-img) no-repeat center/88%;}
body .main-nav a:hover,body .main-nav a.active{border-bottom-color:var(--acc);}
"""
