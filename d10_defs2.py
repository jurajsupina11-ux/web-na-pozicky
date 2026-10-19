import a10_b as B
from d6_common import base
from d9_common import img_css
from d10_defs import D, EX, HDR

D['botanical'] = dict(
    title='Botanical - rastlinny svet, peniaze rastu (zelena / terakota)',
    desc='Listy, ratolesti a kvetinace na krémovom papieri. Investor: lesna zelena, Dlznik: terakota.',
    fonts='Lora:wght@500;600;700&family=Karla:wght@400;500;700',
    art=B.botanical_hero(), extra=EX['botan'],
    vars=base(fh="'Lora'", fb="'Karla'", bg='#F8F4E8', surface='#FFFDF6', soft='#EDF3E3', line='#D9DEC8',
              ink='#1F3A2C', muted='#5D7266', radius='20px', radius_sm='12px', rb='999px', shadow='0 10px 24px rgba(47,107,79,.14)',
              brand='#2F6B4F', brand_ink='#fff', brand_text='#2F6B4F', inv='#2F6B4F', inv_ink='#fff', inv_text='#2F6B4F',
              bor='#C2593A', bor_ink='#fff', bor_text='#A8431F', hdr_bg='#FFFDF6', hdr_ink='#1F3A2C', hdr_bd='1px solid #D9DEC8',
              hero_bg='linear-gradient(160deg,#EDF3E3,#F8F4E8)', hero_bg_solid='#EDF3E3', hero_ink='#1F3A2C', hero_sub='#46604F',
              hero_em='#C2593A', hero_chip='#fff', hero_chip_ink='#2F6B4F', hero_btn='#2F6B4F', hero_btn_ink='#fff',
              cta_bg='#2F6B4F', sb_bg='#FFFDF6', sb_bd='1px solid #D9DEC8', sb_ink='#1F3A2C', sb_sub='#5D7266',
              sb_line='#E3E6D2', sb_hover='#EDF3E3', wal_bg='#2F6B4F', wal_bd='0', wal_ink='#EAF3DD', wal_num='#F5E3A6',
              wal_btn='#F5E3A6', ft_bg='#1F3A2C', ft_ink='#B8CBB5', ft_h='#F5E3A6', ft_line='rgba(255,255,255,.18)',
              th_ink='#2F6B4F', card_bd='1px solid #D9DEC8', inp_bd='1.5px solid #C9D0B4', vis_bg='transparent', vis_bd='0',
              vis_r='20px', h1='54px', **HDR),
    css=img_css('#1F3A2C', '#2F6B4F', '#2F6B4F') +
    "body .cta-band,body .cta-band h2{color:#fff;}body .btn{font-weight:700;}body .wallet-btn,body .wallet-card .btn{color:#1F3A2C;}",
)

D['watercolor'] = dict(
    title='Watercolor - akvarel a masti (tyrkys / ruzova)',
    desc='Rozmazane akvarelove machule na papieri, jemne a umelecke. Investor: tyrkysova, Dlznik: ruzova.',
    fonts='Caveat+Brush&family=Quicksand:wght@500;600;700&family=Mulish:wght@400;600',
    art=B.watercolor_hero(), extra=EX['water'],
    vars=base(fh="'Quicksand'", fb="'Mulish'", bg='#FBF7F2', surface='#FFFFFF', soft='#F4EEF6', line='#E9E2EE',
              ink='#2B3A55', muted='#68728C', radius='30px', radius_sm='18px', rb='999px', shadow='0 14px 30px rgba(143,156,232,.2)',
              brand='#2FA8A4', brand_ink='#fff', brand_text='#1F7F7B', inv='#2FA8A4', inv_ink='#fff', inv_text='#1F7F7B',
              bor='#D9628A', bor_ink='#fff', bor_text='#B23C66', hdr_bg='#FFFFFF', hdr_ink='#2B3A55', hdr_bd='0',
              hero_bg='linear-gradient(160deg,#E4F6F4,#FBEAF0)', hero_bg_solid='#E4F6F4', hero_ink='#2B3A55', hero_sub='#50607E',
              hero_em='#D9628A', hero_chip='rgba(255,255,255,.8)', hero_chip_ink='#1F7F7B', hero_btn='#2B3A55', hero_btn_ink='#fff',
              cta_bg='linear-gradient(135deg,#BFE9E6,#F8D3E0)', sb_bg='#fff', sb_bd='0', sb_ink='#2B3A55', sb_sub='#68728C',
              sb_line='#EEE8F2', sb_hover='#F4EEF6', wal_bg='linear-gradient(135deg,#2FA8A4,#8E9CE8)', wal_bd='0', wal_ink='#fff',
              wal_num='#fff', wal_btn='#fff', ft_bg='#2B3A55', ft_ink='#BCC6E0', ft_h='#F5C26B', ft_line='rgba(255,255,255,.16)',
              th_ink='#1F7F7B', card_bd='0', inp_bd='1.5px solid #DAD3E4', vis_bg='transparent', vis_bd='0', vis_r='30px', h1='56px', **HDR),
    css=img_css('#2B3A55', 'linear-gradient(135deg,#BFE9E6,#F8D3E0)', 'linear-gradient(135deg,#2FA8A4,#8E9CE8)') +
    "body .btn{font-weight:700;}h1,h2{font-weight:700;}body .hero{background:radial-gradient(circle at 15% 20%,#BFE9E6 0,transparent 40%),"
    "radial-gradient(circle at 85% 70%,#F8D3E0 0,transparent 45%),radial-gradient(circle at 60% 10%,#FBE6B8 0,transparent 35%),#FBF7F2;}",
)

D['pixel'] = dict(
    title='Pixel - 8-bitova hra (zelena / ruzova)',
    desc='Retro videohra: pixelove mince, stlpce ako v Mariovi, hrube okraje. Investor: zelena, Dlznik: ruzova.',
    fonts='Pixelify+Sans:wght@500;600;700&family=VT323',
    art=B.pixel_hero(), extra=EX['pixel'],
    vars=base(fh="'Pixelify Sans'", fb="'VT323'", bg='#1A1C2C', surface='#292B45', soft='#222440', line='#566C86',
              ink='#F4F4F4', muted='#94B0C2', radius='0px', radius_sm='0px', rb='0px', shadow='6px 6px 0 #0C0D18',
              brand='#38B764', brand_ink='#0C1A10', brand_text='#A7F070', inv='#38B764', inv_ink='#0C1A10', inv_text='#A7F070',
              bor='#F4A3C0', bor_ink='#2A0A18', bor_text='#F4A3C0', hdr_bg='#1A1C2C', hdr_ink='#F4F4F4', hdr_bd='4px solid #566C86',
              hero_bg='#41A6F6', hero_bg_solid='#41A6F6', hero_ink='#0C0D18', hero_sub='#10243F', hero_em='#FFFFFF',
              hero_chip='#FFCD75', hero_chip_ink='#1A1C2C', hero_btn='#38B764', hero_btn_ink='#0C1A10', cta_bg='#292B45',
              sb_bg='#222440', sb_bd='4px solid #566C86', sb_ink='#F4F4F4', sb_sub='#94B0C2', sb_line='#566C86',
              sb_hover='rgba(167,240,112,.12)', wal_bg='#292B45', wal_bd='4px solid #FFCD75', wal_ink='#F4F4F4',
              wal_num='#FFCD75', wal_btn='#FFCD75', ft_bg='#0C0D18', ft_ink='#94B0C2', ft_h='#FFCD75', ft_line='#566C86',
              th_ink='#A7F070', card_bd='4px solid #566C86', inp_bd='3px solid #94B0C2', vis_bg='transparent', vis_bd='0',
              vis_r='0px', h1='46px', **HDR),
    css=img_css('#0C0D18', '#292B45', '#292B45') +
    "body{font-size:19px;}h1,h2,h3{text-transform:uppercase;line-height:1.25;}body .btn{border:4px solid #0C0D18;box-shadow:4px 4px 0 #0C0D18;"
    "text-transform:uppercase;font-size:13px;}body .btn:active{transform:translate(4px,4px);box-shadow:none;}body .hero{border-bottom:6px solid #0C0D18;}"
    "body .main-nav a{font-size:12px;text-transform:uppercase;}*{image-rendering:pixelated;}",
)
