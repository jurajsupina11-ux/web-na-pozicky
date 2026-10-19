import a9_designs as A
from d6_common import base
from d9_common import NAVFIX, img_css

COMMON = dict(
    hdr_top='0', hero_chip_ink='#fff', hero_btn_ink='#fff', wal_btn_ink='#0B1020', focus='rgba(91,91,240,.25)',
)


def mk(**kw):
    d = dict(COMMON)
    d.update(kw)
    return base(**d)


DESIGNS = {}

DESIGNS['neobank'] = dict(
    title='Neobank - fialova appka (fialova / oranzova)',
    desc='Cista mobilna bankova aplikacia: karty, grafy, velke zaoblenia. Investor: indigo, Dlznik: oranzova.',
    fonts='Plus+Jakarta+Sans:wght@500;600;700;800&family=Inter:wght@400;500;600',
    art=A.neobank(), extra=A.extras('neobank'),
    vars=mk(fh="'Plus Jakarta Sans'", fb="'Inter'", bg='#F5F6FF', surface='#FFFFFF', soft='#ECEEFF', line='#E3E6F8',
            ink='#1B1F3B', muted='#667091', radius='22px', radius_sm='14px', rb='999px',
            shadow='0 14px 34px rgba(91,91,240,.14)', brand='#5B5BF0', brand_ink='#fff', brand_text='#4A4AD8',
            inv='#5B5BF0', inv_ink='#fff', inv_text='#4A4AD8', bor='#FF7A3D', bor_ink='#fff', bor_text='#D9540F',
            hdr_bg='#FFFFFF', hdr_ink='#1B1F3B', hdr_bd='1px solid #E3E6F8',
            hero_bg='linear-gradient(160deg,#EEF0FF,#F9F0FF)', hero_bg_solid='#EEF0FF', hero_ink='#1B1F3B',
            hero_sub='#4F5778', hero_em='#5B5BF0', hero_chip='#fff', hero_chip_ink='#4A4AD8', hero_btn='#5B5BF0',
            hero_btn_ink='#fff', cta_bg='linear-gradient(135deg,#5B5BF0,#8B5CF6)', sb_bg='#fff', sb_bd='1px solid #E3E6F8',
            sb_ink='#1B1F3B', sb_sub='#667091', sb_line='#E3E6F8', sb_hover='#ECEEFF',
            wal_bg='linear-gradient(135deg,#5B5BF0,#8B5CF6)', wal_bd='0', wal_ink='#fff', wal_num='#fff',
            wal_btn='#fff', ft_bg='#14173A', ft_ink='#A9B0D6', ft_h='#fff', ft_line='rgba(255,255,255,.14)',
            th_ink='#4A4AD8', card_bd='1px solid #E3E6F8', inp_bd='1.5px solid #D7DBF3', vis_bg='transparent',
            vis_bd='0', vis_r='22px', h1='56px'),
    css=img_css('#14173A', 'linear-gradient(135deg,#5B5BF0,#8B5CF6)', 'linear-gradient(135deg,#5B5BF0,#8B5CF6)') +
    "body .cta-band,body .cta-band h2{color:#fff;}body .btn{font-weight:700;}",
)

DESIGNS['privatebank'] = dict(
    title='Private Bank - elegantna banka (namornicka / zlata)',
    desc='Klasicka sukromna banka: serif, zlate detaily, stlpy. Investor: namornicka modra, Dlznik: zlata.',
    fonts='Cormorant+Garamond:wght@500;600;700&family=Lato:wght@400;700',
    art=A.private_bank(), extra=A.extras('bank'),
    vars=mk(fh="'Cormorant Garamond'", fb="'Lato'", bg='#F7F4EC', surface='#FFFFFF', soft='#EFEADB', line='#DDD5BE',
            ink='#0F2A5C', muted='#5B6685', radius='4px', radius_sm='2px', rb='2px', shadow='0 10px 26px rgba(15,42,92,.12)',
            brand='#0F2A5C', brand_ink='#fff', brand_text='#0F2A5C', inv='#0F2A5C', inv_ink='#fff', inv_text='#0F2A5C',
            bor='#B8891F', bor_ink='#fff', bor_text='#8A6410', hdr_bg='#FFFFFF', hdr_ink='#0F2A5C',
            hdr_bd='3px solid #C9A24B', hero_bg='linear-gradient(160deg,#0F2A5C,#1E4A8F)', hero_bg_solid='#0F2A5C',
            hero_ink='#fff', hero_sub='#C9D6F0', hero_em='#E3B84F', hero_chip='rgba(201,162,75,.2)',
            hero_chip_ink='#E3B84F', hero_btn='#C9A24B', hero_btn_ink='#0F2A5C', cta_bg='#0F2A5C', sb_bg='#fff',
            sb_bd='1px solid #DDD5BE', sb_ink='#0F2A5C', sb_sub='#5B6685', sb_line='#E7E0CC', sb_hover='#F7F4EC',
            wal_bg='#0F2A5C', wal_bd='2px solid #C9A24B', wal_ink='#fff', wal_num='#E3B84F', wal_btn='#C9A24B',
            ft_bg='#0A1D42', ft_ink='#AEBBDA', ft_h='#E3B84F', ft_line='rgba(201,162,75,.3)', th_ink='#0F2A5C',
            card_bd='1px solid #DDD5BE', inp_bd='1px solid #BDB291', vis_bg='transparent', vis_bd='0', vis_r='4px', h1='62px'),
    css=img_css('#0A1D42', '#0F2A5C', '#0F2A5C') +
    "h1,h2,h3{font-weight:700;}body .btn{border-radius:2px;letter-spacing:.06em;text-transform:uppercase;font-size:13px;}"
    "body .hero .btn-primary{color:#0F2A5C;}body .cta-band{color:#fff;}body .cta-band h2{color:#fff;}",
)
