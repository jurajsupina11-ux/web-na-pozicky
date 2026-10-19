"""Vygeneruje klikatelny staticky mockup (mockup-v2/) z realnych sablon.
Bez funkcii: formulare sa neodosielaju, odkazy vedu medzi statickymi subormi.
CSS/JS/obrazky sa kopiruju zo static/theme - jediny zdroj dizajnu."""
import os
import re
import shutil

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
os.environ.setdefault('ALLOWED_HOSTS', 'testserver,localhost,127.0.0.1')
django.setup()

from django.core.management import call_command
from django.template.loader import render_to_string
from django.test import Client

from auctions.models import Auction
from mockup_pages import all_pages
from users.models import User

OUT = 'mockup-v2'
STAMP = str(int(__import__('time').time()))
PREVENT = (
    '<script>document.addEventListener("submit",function(e){e.preventDefault();});'
    'document.addEventListener("click",function(e){var a=e.target.closest("a");'
    'if(a&&a.getAttribute("href")==="#"){e.preventDefault();}});</script>'
)
LABELS = {'pub': 'Verejné stránky', 'inv': 'Investor', 'bor': 'Dlžník', 'adm': 'Admin'}


def make_clients():
    call_command('ensure_test_users')
    call_command('ensure_test_admin')
    clients = {'pub': Client()}
    for role, uname in (('inv', 'demo_investor'), ('bor', 'demo_dlznik')):
        c = Client()
        c.force_login(User.objects.get(username=uname))
        clients[role] = c
    c = Client()
    c.force_login(User.objects.filter(is_superuser=True).first())
    clients['adm'] = c
    return clients


def extra_pages():
    pages = []
    act = Auction.objects.filter(status=Auction.Status.ACTIVE).first()
    if act:
        pages.append(('inv', 'detail-aukcie', f'/aukcie/{act.pk}/'))
    app = Auction.objects.order_by('-pk').first()
    if app:
        pages.append(('adm', 'detail-ziadosti', f'/sprava/ziadosti/{app.pk}/'))
        pages.append(('adm', 'detail-pouzivatela', f'/sprava/pouzivatelia/{app.borrower_id}/'))
    return pages


def transform(html, role, mapping):
    def link(href):
        path = href.split('#')[0].split('?')[0]
        for r in (role, 'pub'):
            if (r, path) in mapping:
                return mapping[(r, path)]
        return '#'

    html = html.replace('/static/theme/', 'assets/')
    # verzia v URL, aby prehliadac nikdy nepouzil staru kopiu loga/CSS z cache
    html = re.sub(r'(assets/[\w.-]+\.(?:svg|css|js))', lambda m: f'{m.group(1)}?v={STAMP}', html)
    html = re.sub(r'(href|action)="(/[^"]*)"',
                  lambda m: f'{m.group(1)}="{link(m.group(2))}"', html)
    html = re.sub(r'src="/[^"]*qr-platba[^"]*"', 'src="assets/logo-icon.svg"', html)
    html = re.sub(r'<input[^>]*csrfmiddlewaretoken[^>]*>', '', html)
    return html.replace('</body>', PREVENT + '</body>')


def build_index(mapping):
    parts = []
    for role, label in LABELS.items():
        files = sorted(f for (r, _u), f in mapping.items() if r == role)
        if role == 'pub':
            files += [f'pub-chyba-{c}.html' for c in (403, 404, 500)]
        items = ''.join(f'<li><a href="{f}">{f[:-5]}</a></li>' for f in files)
        parts.append(f'<h2>{label}</h2><ul>{items}</ul>')
    style = ('body{font-family:system-ui;max-width:780px;margin:30px auto;padding:0 16px;'
             'color:#12203F;background:#F5F7FA}a{color:#0f9d83;font-weight:600}ul{columns:2}')
    with open(f'{OUT}/index.html', 'w', encoding='utf-8') as fh:
        fh.write(
            '<!DOCTYPE html><html lang="sk"><head><meta charset="UTF-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>Mockup v2</title><style>{style}</style></head><body>'
            '<h1>Mockup v2 – prehľad stránok</h1>' + ''.join(parts) + '</body></html>')


def main():
    clients = make_clients()
    pages = all_pages() + extra_pages()
    mapping = {(role, url): f'{role}-{name}.html' for role, name, url in pages}
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    shutil.copytree('static/theme', f'{OUT}/assets')
    ok, bad = 0, []
    for role, name, url in pages:
        r = clients[role].get(url, follow=True)
        if r.status_code != 200:
            bad.append((role, url, r.status_code))
            continue
        html = transform(r.content.decode('utf-8'), role, mapping)
        with open(f'{OUT}/{role}-{name}.html', 'w', encoding='utf-8') as fh:
            fh.write(html)
        ok += 1
    for code in ('403', '404', '500'):
        html = transform(render_to_string(f'{code}.html'), 'pub', mapping)
        with open(f'{OUT}/pub-chyba-{code}.html', 'w', encoding='utf-8') as fh:
            fh.write(html)
        ok += 1
    build_index(mapping)
    print('hotovo', ok, 'stranok; chyby:', bad)


if __name__ == '__main__':
    main()
