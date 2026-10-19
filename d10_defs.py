import a10_a as A
import a10_b as B
from a9_common import svg
from d6_common import base
from d9_common import img_css

D = {}


def ic_neon(c):
    return '<rect x="14" y="14" width="112" height="112" rx="26" fill="#1B0B3A" stroke="%s" stroke-width="5"/>' % c


def ic_deco(c):
    return '<polygon points="70,8 132,70 70,132 8,70" fill="#0C1A2B" stroke="#D4AF37" stroke-width="5"/>'


def ic_leaf(c):
    return '<path d="M16 124C16 60 60 16 124 16 124 80 80 124 16 124Z" fill="%s"/>' % c


def ic_blob(c):
    return '<path d="M70 12C104 8 130 36 128 70 126 106 98 130 66 128 32 126 10 98 14 66 18 34 42 14 70 12Z" fill="%s" opacity=".85"/>' % c


def ic_pix(c):
    return '<rect x="14" y="14" width="112" height="112" fill="%s"/><rect x="14" y="14" width="112" height="112" fill="none" stroke="#1A1C2C" stroke-width="8"/>' % c


EX = {
    'synth': A.std_extras(A.icons(ic_neon, '#28F2FF', ['#FF3CAC']), '#FF3CAC', '#28F2FF', '#FFD93D', '#FF3CAC'),
    'deco': A.std_extras(A.icons(ic_deco, '#D4AF37', ['#D4AF37']), '#D4AF37', '#0C1A2B', '#D4AF37', '#7A5F12'),
    'botan': A.std_extras(A.icons(ic_leaf, '#fff', ['#2F6B4F', '#3F8A62', '#5BAA7A', '#2F6B4F']), '#3F8A62', '#B8D8A8'),
    'water': A.std_extras(A.icons(ic_blob, '#2B3A55', ['#4FC3C0', '#F5C26B', '#E98AA8', '#8E9CE8']), '#4FC3C0', '#E98AA8', '#F5C26B', '#C9871A'),
    'pixel': A.std_extras(A.icons(ic_pix, '#1A1C2C', ['#FFCD75', '#73EFF7', '#A7F070', '#F4A3C0']), '#38B764', '#41A6F6', '#FFD93D', '#C9810F'),
}
HDR = dict(hdr_top='0', wal_btn_ink='#0B1020')

D['synthwave'] = dict(
    title='Synthwave - neonove retro 80. roky (ruzova / cyan)',
    desc='Neonovy zapad slnka, mriezka a ziara na tmavom fialovom pozadi. Investor: cyan, Dlznik: ruzova.',
    fonts='Orbitron:wght@500;700;900&family=Rajdhani:wght@500;600;700',
    art=A.synth_hero(), extra=EX['synth'],
    vars=base(fh="'Orbitron'", fb="'Rajdhani'", bg='#140630', surface='#1F0B47', soft='#190838', line='rgba(40,242,255,.35)',
              ink='#F4EAFF', muted='#B9A5E8', radius='4px', radius_sm='2px', rb='2px', shadow='0 0 24px rgba(255,60,172,.35)',
              brand='#FF3CAC', brand_ink='#fff', brand_text='#FF7CC8', inv='#28F2FF', inv_ink='#062A33', inv_text='#28F2FF',
              bor='#FF3CAC', bor_ink='#fff', bor_text='#FF7CC8', hdr_bg='#140630', hdr_ink='#F4EAFF',
              hdr_bd='1px solid rgba(255,60,172,.6)', hero_bg='#140630', hero_bg_solid='#140630', hero_ink='#fff',
              hero_sub='#CDBBF5', hero_em='#28F2FF', hero_chip='rgba(40,242,255,.12)', hero_chip_ink='#28F2FF',
              hero_btn='#FF3CAC', hero_btn_ink='#fff', cta_bg='#1F0B47', sb_bg='#190838', sb_bd='1px solid rgba(40,242,255,.4)',
              sb_ink='#F4EAFF', sb_sub='#B9A5E8', sb_line='rgba(255,60,172,.3)', sb_hover='rgba(40,242,255,.1)',
              wal_bg='#2B1060', wal_bd='1px solid #FF3CAC', wal_ink='#F4EAFF', wal_num='#28F2FF', wal_btn='#28F2FF',
              ft_bg='#0C0320', ft_ink='#B9A5E8', ft_h='#28F2FF', ft_line='rgba(255,60,172,.35)', th_ink='#28F2FF',
              card_bd='1px solid rgba(40,242,255,.45)', inp_bd='1px solid rgba(255,60,172,.7)', vis_bg='transparent',
              vis_bd='0', vis_r='4px', h1='50px', **HDR),
    css=img_css('#0C0320', 'linear-gradient(135deg,#2B1060,#5A1580)', '#2B1060') +
    "h1,h2,h3,.btn{text-transform:uppercase;letter-spacing:.04em;}body .btn{font-weight:700;box-shadow:0 0 18px rgba(255,60,172,.5);}"
    "body .hero h1 em,body .hero h1 span{text-shadow:0 0 18px currentColor;}body .card{box-shadow:0 0 18px rgba(40,242,255,.18);}",
)

D['artdeco'] = dict(
    title='Art Deco - zlato a geometria 20. rokov (zlata / smaragd)',
    desc='Elegancia Great Gatsby: zlate vejare, geometricke linky, tmavomodre pozadie. Investor: zlata, Dlznik: smaragd.',
    fonts='Poiret+One&family=Josefin+Sans:wght@400;600;700&family=Cinzel:wght@500;700',
    art=A.deco_hero(), extra=EX['deco'],
    vars=base(fh="'Cinzel'", fb="'Josefin Sans'", bg='#0C1A2B', surface='#13263D', soft='#0F2036', line='rgba(212,175,55,.45)',
              ink='#F5ECD2', muted='#B5AE96', radius='0px', radius_sm='0px', rb='0px', shadow='0 0 0 1px rgba(212,175,55,.4)',
              brand='#D4AF37', brand_ink='#0C1A2B', brand_text='#E3C766', inv='#D4AF37', inv_ink='#0C1A2B', inv_text='#E3C766',
              bor='#1FA37A', bor_ink='#fff', bor_text='#4FD1A5', hdr_bg='#0C1A2B', hdr_ink='#F5ECD2',
              hdr_bd='3px double #D4AF37', hero_bg='#0C1A2B', hero_bg_solid='#0C1A2B', hero_ink='#F5ECD2', hero_sub='#C9C2A8',
              hero_em='#E3C766', hero_chip='transparent', hero_chip_ink='#E3C766', hero_btn='#D4AF37', hero_btn_ink='#0C1A2B',
              cta_bg='#13263D', sb_bg='#0F2036', sb_bd='1px solid #D4AF37', sb_ink='#F5ECD2', sb_sub='#B5AE96',
              sb_line='rgba(212,175,55,.35)', sb_hover='rgba(212,175,55,.1)', wal_bg='#13263D', wal_bd='3px double #D4AF37',
              wal_ink='#F5ECD2', wal_num='#E3C766', wal_btn='#D4AF37', ft_bg='#08121E', ft_ink='#B5AE96', ft_h='#E3C766',
              ft_line='rgba(212,175,55,.4)', th_ink='#E3C766', card_bd='1px solid rgba(212,175,55,.55)',
              inp_bd='1px solid #D4AF37', vis_bg='transparent', vis_bd='0', vis_r='0px', h1='54px', **HDR),
    css=img_css('#08121E', '#13263D', '#13263D') +
    "h1,h2,h3{letter-spacing:.06em;font-weight:700;}body .btn{border-radius:0;letter-spacing:.14em;text-transform:uppercase;font-size:12.5px;}"
    "body .card,body .stat-tile{outline:1px solid rgba(212,175,55,.35);outline-offset:-7px;}body .eyebrow{border:1px solid #D4AF37;letter-spacing:.2em;}",
)
