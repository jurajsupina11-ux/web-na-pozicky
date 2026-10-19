import a9_designs as A
from d9_common import img_css
from d9_defs import DESIGNS, mk

DESIGNS['mintfin'] = dict(
    title='Mint - svieza fintech (zelena / ruzova)',
    desc='Svetly zeleny fintech s koláčovými a stlpcovymi grafmi. Investor: smaragdova, Dlznik: ruzova.',
    fonts='Manrope:wght@500;600;700;800&family=Inter:wght@400;500;600',
    art=A.mint(), extra=A.extras('mint'),
    vars=mk(fh="'Manrope'", fb="'Inter'", bg='#F3FBF7', surface='#FFFFFF', soft='#E3F6EC', line='#CFEBDD',
            ink='#06382B', muted='#4D6F63', radius='26px', radius_sm='16px', rb='999px',
            shadow='0 14px 30px rgba(16,185,129,.16)', brand='#10B981', brand_ink='#04281E', brand_text='#0B7A57',
            inv='#10B981', inv_ink='#04281E', inv_text='#0B7A57', bor='#EC4899', bor_ink='#fff', bor_text='#BE1F76',
            hdr_bg='#FFFFFF', hdr_ink='#06382B', hdr_bd='1px solid #CFEBDD',
            hero_bg='linear-gradient(160deg,#D1FAE5,#ECFDF5)', hero_bg_solid='#D1FAE5', hero_ink='#06382B',
            hero_sub='#2F5B4C', hero_em='#0B9C6D', hero_chip='#fff', hero_chip_ink='#0B7A57', hero_btn='#06382B',
            hero_btn_ink='#fff', cta_bg='#10B981', sb_bg='#fff', sb_bd='1px solid #CFEBDD', sb_ink='#06382B',
            sb_sub='#4D6F63', sb_line='#CFEBDD', sb_hover='#E3F6EC', wal_bg='#06382B', wal_bd='0', wal_ink='#D1FAE5',
            wal_num='#6EE7B7', wal_btn='#6EE7B7', ft_bg='#06382B', ft_ink='#A7DCC8', ft_h='#6EE7B7',
            ft_line='rgba(255,255,255,.15)', th_ink='#0B7A57', card_bd='1px solid #CFEBDD', inp_bd='1.5px solid #B5DECB',
            vis_bg='transparent', vis_bd='0', vis_r='26px', h1='56px'),
    css=img_css('#06382B', '#10B981', '#06382B') +
    "body .cta-band,body .cta-band h2{color:#04281E;}body .btn{font-weight:800;}body .hero .btn-primary{color:#fff;}",
)

DESIGNS['trader'] = dict(
    title='Trader - tmava obchodna platforma (limetkova / ruzova)',
    desc='Tmava trading platforma so sviecovym grafom a mriezkou. Investor: limetkova, Dlznik: ruzova.',
    fonts='Sora:wght@500;600;700;800&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@500',
    art=A.trading(), extra=A.extras('trading'),
    vars=mk(fh="'Sora'", fb="'IBM Plex Sans'", bg='#0A0F11', surface='#12191C', soft='#0E1417', line='#23323A',
            ink='#E8F0F2', muted='#8DA3AB', radius='10px', radius_sm='6px', rb='6px', shadow='0 12px 30px rgba(0,0,0,.5)',
            brand='#C6FF3D', brand_ink='#101800', brand_text='#C6FF3D', inv='#C6FF3D', inv_ink='#101800',
            inv_text='#C6FF3D', bor='#FF4D8D', bor_ink='#fff', bor_text='#FF7FAE', hdr_bg='#0A0F11', hdr_ink='#E8F0F2',
            hdr_bd='1px solid #23323A', hero_bg='#0A0F11', hero_bg_solid='#0A0F11', hero_ink='#fff', hero_sub='#9DB2B9',
            hero_em='#C6FF3D', hero_chip='rgba(198,255,61,.12)', hero_chip_ink='#C6FF3D', hero_btn='#C6FF3D',
            hero_btn_ink='#101800', cta_bg='#12191C', sb_bg='#0E1417', sb_bd='1px solid #23323A', sb_ink='#E8F0F2',
            sb_sub='#8DA3AB', sb_line='#23323A', sb_hover='rgba(198,255,61,.08)', wal_bg='#12191C',
            wal_bd='1px solid #2E4650', wal_ink='#E8F0F2', wal_num='#C6FF3D', wal_btn='#C6FF3D',
            ft_bg='#06090A', ft_ink='#8DA3AB', ft_h='#C6FF3D', ft_line='#23323A', th_ink='#C6FF3D',
            card_bd='1px solid #23323A', inp_bd='1px solid #34505B', vis_bg='transparent', vis_bd='0', vis_r='10px', h1='56px'),
    css=img_css('#06090A', '#12191C', '#12191C') +
    "body{background:#0A0F11 url('img-dots.svg') 0 0/400px 300px;}body .btn{font-weight:700;}"
    "body .eyebrow,body .main-nav a{font-family:'IBM Plex Mono',monospace;letter-spacing:.04em;}"
    "body .cta-band{border:1px solid #2E4650;}",
)

DESIGNS['pastel'] = dict(
    title='Pastel - jemny a pratelsky financny dashboard (modra / koral)',
    desc='Mäkke pastelove farby, velke ikony a zaoblene karty. Investor: modra, Dlznik: koralova.',
    fonts='Outfit:wght@500;600;700&family=Nunito+Sans:wght@400;600;700',
    art=A.pastel(), extra=A.extras('pastel'),
    vars=mk(fh="'Outfit'", fb="'Nunito Sans'", bg='#FBF8F4', surface='#FFFFFF', soft='#F1EEF9', line='#E8E3EE',
            ink='#2A2F4A', muted='#6B7090', radius='28px', radius_sm='18px', rb='999px',
            shadow='0 12px 30px rgba(129,140,248,.18)', brand='#38BDF8', brand_ink='#04263A', brand_text='#0A78B0',
            inv='#38BDF8', inv_ink='#04263A', inv_text='#0A78B0', bor='#FB7185', bor_ink='#fff', bor_text='#D6304A',
            hdr_bg='#FFFFFF', hdr_ink='#2A2F4A', hdr_bd='0', hero_bg='linear-gradient(160deg,#DCEEFB,#FDE2E4)',
            hero_bg_solid='#DCEEFB', hero_ink='#2A2F4A', hero_sub='#4C5273', hero_em='#6366F1', hero_chip='#fff',
            hero_chip_ink='#0A78B0', hero_btn='#2A2F4A', hero_btn_ink='#fff', cta_bg='linear-gradient(135deg,#BAE6FD,#FBCFE8)',
            sb_bg='#fff', sb_bd='0', sb_ink='#2A2F4A', sb_sub='#6B7090', sb_line='#EEE9F3', sb_hover='#F1EEF9',
            wal_bg='linear-gradient(135deg,#38BDF8,#818CF8)', wal_bd='0', wal_ink='#fff', wal_num='#fff', wal_btn='#fff',
            ft_bg='#2A2F4A', ft_ink='#B9BEDB', ft_h='#FDE68A', ft_line='rgba(255,255,255,.15)', th_ink='#0A78B0',
            card_bd='0', inp_bd='1.5px solid #DAD4E6', vis_bg='transparent', vis_bd='0', vis_r='28px', h1='56px'),
    css=img_css('#2A2F4A', 'linear-gradient(135deg,#BAE6FD,#FBCFE8)', 'linear-gradient(135deg,#38BDF8,#818CF8)') +
    "body .site-header{box-shadow:0 6px 20px rgba(129,140,248,.14);}body .btn{font-weight:700;}",
)
