# Návrhy nových funkcií platformy

Prehľad možných vylepšení/doplnkov na základe analýzy aktuálneho stavu
platformy (P2P požičiavanie - aukcie, sekundárny trh, peňaženka, KYC,
zmluvy/PDF, referral program, vernostné stupne, notifikácie, daňové výkazy).
Zoradené podľa odhadovanej hodnoty pre používateľa a náročnosti implementácie.

## 1. Rýchle vylepšenia (nízka náročnosť, vysoká hodnota)

- **E-mailové notifikácie pri zmene stavu žiadosti/investície** - momentálne
  existujú interné notifikácie (zvonček) aj niektoré e-maily (schválenie,
  investícia), ale nie všetky stavové zmeny posielajú e-mail (napr. odklad
  splátky, nahlásenie úhrady, zmena IBAN). Zjednotiť, aby kľúčové udalosti
  vždy poslali aj e-mail, nielen internú notifikáciu.
- **Push/e-mail pripomienka splatnosti** - automatická pripomienka dlžníkovi
  3 dni pred splatnosťou a investorovi deň po splatnosti, ak pôžička nebola
  označená ako splatená (cez `management command` + cron/Celery beat).
- **Filtrovanie a triedenie v aukčnej miestnosti** - `open_auctions_view`
  momentálne vracia všetky otvorené žiadosti bez možnosti filtrovať podľa
  úroku, sumy alebo splatnosti. Pridať jednoduché query-param filtre (podobne
  ako `investor_history` má dátumový filter).
- **Potvrdzovací e-mail/SMS pri väčších sumách** - pri výberoch nad určitú
  sumu (napr. 500 €) pridať dodatočné overenie (napr. e-mailový odkaz na
  potvrdenie), nielen bezpečnostný kód.
- **Štatistiky vo vlastnom dashboarde** - investor aj dlžník majú k
  dispozícii `core:public_stats` (globálne čísla), ale nie osobný graf
  vývoja portfólia/splátok v čase. Jednoduchý graf (napr. Chart.js) na
  `investor_dashboard` a `my_applications`.

## 2. Stredne náročné funkcie

- **Automatické reinvestovanie (auto-invest)** - investor nastaví pravidlá
  (napr. "automaticky financuj žiadosti do 300 € s úrokom nad 20 %") a
  systém mu ponúkne/automaticky vytvorí `Bid` pri splnení podmienok. Zníži
  potrebu manuálne sledovať aukčnú miestnosť a zrýchli financovanie žiadostí
  pre dlžníkov.
- **Čiastočné spolufinancovanie pôžičiek** - aktuálne platí "all-or-nothing"
  (jedna pôžička = jeden investor). Rozdelenie pôžičky medzi viacero
  investorov (ako pri klasických P2P platformách) by zvýšilo likviditu a
  umožnilo menším investorom participovať na väčších pôžičkách. Ide o
  väčší zásah do `Bid`/`Auction` modelu (viacero čiastočných `Bid` na jednu
  `Auction`, proporčné úroky a splátky).
- **Hodnotenie/rating dlžníkov pri opakovanej žiadosti** - `loan_application_repeat`
  už existuje pre overených dlžníkov, ale nemá viditeľný "credit score" alebo
  históriu spoľahlivosti (počet včas splatených pôžičiek), ktorú by investor
  videl pri rozhodovaní o financovaní. Pridať jednoduché skóre na základe
  histórie splácania.
- **Automatické upomienky a eskalácia omeškania** - pri `is_overdue` aukciách
  pridať odstupňovaný proces (e-mail po 1 dni, 7 dňoch, SMS, atď.) pred tým,
  než nastúpi garancia odkúpenia (90 dní).
- **Mobilná PWA (Progressive Web App)** - pridať `manifest.json` a service
  worker, aby si mohli používatelia "nainštalovať" appku na plochu telefónu
  ako natívnu aplikáciu (offline fallback stránka, ikonka). Nadväzuje na
  tohtosezónnu mobilnú responzivitu.

## 3. Väčšie strategické funkcie

- **Online platobná brána (napr. GoPay, Stripe, Tatra banka platobné API)** -
  najväčšia UX bolesť je manuálny bankový prevod pre vklady aj výbery
  (vyžaduje ručné potvrdenie adminom). Napojenie platobnej brány by
  automatizovalo vklady (okamžité pripísanie na peňaženku) a zrýchlilo výbery.
  Vyžaduje zmluvu s poskytovateľom a webhook spracovanie.
- **Dvojfaktorová autentifikácia (2FA)** pre investorov s vyšším zostatkom
  na peňaženke - TOTP (Google Authenticator) alebo SMS kód pri prihlásení,
  nad rámec súčasného e-mailového bezpečnostného kódu.
- **API pre inštitucionálnych investorov** - REST API (napr. cez Django REST
  Framework, ktorý je už v `requirements.txt` ako `djangorestframework`
  podľa `staticfiles/rest_framework/`) na automatizované investovanie pre
  väčších/firemných investorov.
- **Verejný "marketplace" prehľad výkonnosti fondu** - rozšíriť
  `core:public_stats` o historické grafy výnosov, mieru defaultov po
  rokoch/štvrťrokoch - zvyšuje dôveryhodnosť pre nových investorov.
- **Odporúčací/affiliate program s viacúrovňovou odmenou** - súčasný referral
  program dáva jednorazový bonus 10 € po prvej investícii pozvaného. Možnosť
  rozšíriť o percentuálnu odmenu z objemu investícií pozvaného počas prvého
  roka (affiliate model) pre "ambasádorov" platformy.

## 4. Menšie UX doplnky všimnuté počas auditu

- **Breadcrumbs / "späť" tlačidlo** v detailoch (napr. `auction_detail`,
  `application_detail` na admin strane) pre jednoduchšiu navigáciu späť na
  zoznam bez použitia tlačidla prehliadača.
- **Potvrdzovacie dialógy pred nebezpečnými akciami** - napr. zrušenie
  predaja investície, žiadosť o výber - momentálne idú priamo cez POST bez
  JS potvrdenia (`confirm()`), čo pri náhodnom kliknutí môže prekvapiť.
- **Export histórie do CSV** (popri existujúcom PDF exporte v
  `investor_history_pdf`/`tax_statement_pdf`) pre používateľov, ktorí chcú
  dáta spracovať v Exceli.
- **Vyhľadávanie v histórii/zoznamoch** - `investor_history` má dátumový
  filter, ale napr. `my_contracts`/`my_applications` nemajú žiadne
  vyhľadávanie/filtrovanie pri väčšom počte záznamov.

---

*Poznámka: Zoznam vychádza z preskúmania existujúcich modelov
(`Auction`, `Bid`, `WalletTransaction`, `Notification`, `User` s KYC/loyalty
poľami) a views/templates vo `core`, `users`, `auctions`, `adminpanel`.
Admin backend (`/sprava/`, `/admin/`) je mimo rozsahu tejto session podľa
pôvodnej požiadavky, preto návrhy cielia najmä na dlžnícke a investorské
prostredie.*
