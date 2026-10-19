# Pôžičky pre Dlžníkov

Aukčný systém na krátkodobé pôžičky (P2P lending) – web (Django) + budúca mobilná appka.

Domain: www.pozickypredlznikov.sk

## Lokálne spustenie

```bash
python -m venv venv
venv\Scripts\activate         # Windows
pip install -r requirements.txt
cp .env.example .env           # a uprav podľa potreby
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Appka bude dostupná na http://127.0.0.1:8000/, admin na /admin/.

## Štruktúra projektu

- `config/` – Django settings, root urls, wsgi/asgi
- `users/` – custom User model, registrácia, login/logout
- `auctions/` – aukcie (žiadosti o pôžičku)
- `bids/` – ponuky veriteľov na aukcie
- `templates/` – spoločné šablóny (base.html)
- `build.sh` – build skript pre Render (install, collectstatic, migrate)
- `render.yaml` – Render Blueprint (web service + PostgreSQL databáza)

## Deployment na Render

1. Repo je napojené na GitHub (`web-na-pozicky`).
2. Na Render vytvor **Blueprint** z `render.yaml` alebo ručne:
   - Web Service (Python), build command `./build.sh`, start command `gunicorn config.wsgi:application`
   - PostgreSQL databázu a pripoj `DATABASE_URL` cez env var
3. Nastav env premenné: `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`.
4. V DNS nastaveniach domény `pozickypredlznikov.sk` nasmeruj na Render (Custom Domain v Render dashboarde).

## Pravidelné úlohy (Render Cron Jobs)

`render.yaml` už obsahuje definíciu dvoch Cron Job služieb (`pozicky-splatnosti-pripomienky` a
`pozicky-automaticky-odkup`), ktoré sa vytvoria automaticky pri ďalšom **Blueprint sync** na Render
(Dashboard → príslušný Blueprint → "Sync"). Ak boli služby vytvorené ručne pred touto zmenou, over si
v Render Dashboarde, že:

1. Obe cron služby majú nastavenú premennú `SECRET_KEY` (keďže `sync: false`, treba ju doplniť ručne
   rovnakou hodnotou ako vo web service, inak Django pri štarte zlyhá).
2. Schedule je v UTC: `0 6 * * *` (06:00 UTC = 08:00 SEČ) pre pripomienky, `30 6 * * *` pre odkup.

Manuálne spustenie pre test: v Render Dashboarde otvor danú cron službu → záložka **Runs** → **Trigger Run**.

Príkazy, ktoré cron joby spúšťajú:

- `python manage.py send_due_date_reminders` - e-mailové pripomienky blížiacej sa/prekročenej splatnosti.
- `python manage.py process_buybacks` - garancia odkúpenia: automaticky odkúpi pôžičky nesplatené > 90 dní po splatnosti.
- `python manage.py close_expired_auctions` - automaticky zruší žiadosti o pôžičku, ktoré neboli vyfinancované do konca lehoty (ends_at).

## Ďalšie kroky (MVP backlog)

- [ ] KYC overenie identity užívateľov
- [x] Automatické uzatváranie aukcií po uplynutí `ends_at` (Render Cron Job - `close_expired_auctions`)
- [x] Platobný proces: žiadne platobné brány - manuálne bankové prevody (vklad investor -> náš účet, výber náš účet -> investor)
- [ ] REST API (django-rest-framework je už nainštalovaný) pre budúcu mobilnú appku (Google Play)
- [x] E-mailové notifikácie (nová ponuka, koniec aukcie, bezpečnostný kód pri registrácii)
- [ ] Produkčné nastavenie statických súborov / médií (napr. S3-compatible storage)
