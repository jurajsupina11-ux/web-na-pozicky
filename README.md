# Pôžičky Predlžníkov

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

## Ďalšie kroky (MVP backlog)

- [ ] KYC overenie identity užívateľov
- [ ] Automatické uzatváranie aukcií po uplynutí `ends_at` (Celery/cron alebo Render Cron Job)
- [ ] Platobná integrácia (napr. Stripe, alebo lokálny platobný gateway)
- [ ] REST API (django-rest-framework je už nainštalovaný) pre budúcu mobilnú appku (Google Play)
- [ ] E-mailové notifikácie (nová ponuka, koniec aukcie)
- [ ] Produkčné nastavenie statických súborov / médií (napr. S3-compatible storage)
