"""Komplexny smoke test - simuluje registraciu/pouzivanie uctu dlznika aj
investora cez Django test client a hlasi vsetky chyby (500, nespravne
presmerovania, chybajuce odkazy, formularove chyby)."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from decimal import Decimal
from django.test import Client
from django.urls import reverse
from users.models import User
from auctions.models import Auction
from bids.models import Bid

errors = []

def check(label, resp, expect=(200, 302)):
    code = resp.status_code
    ok = code in expect
    if ok:
        print(f"OK   {label} -> {code}")
    else:
        errors.append(f"[{label}] status={code} (expected {expect})")
        print(f"FAIL {label} -> {code}")
    return resp

print("=== CISTENIE testovacich uctov ===")
User.objects.filter(username__in=['9001011234', 'testinvestor1', 'fundertest1', '9002022222']).delete()

# ---------------------------------------------------------------------------
print("\n=== BORROWER (DLZNIK) JOURNEY ===")
c = Client()

check('landing', c.get('/'))
check('borrower landing', c.get(reverse('core:borrower')))
check('loan_application GET (anon)', c.get(reverse('users:loan_application')))

form_data = {
    'first_name': 'Ján', 'last_name': 'Testovací', 'email': 'jan.test@example.com',
    'phone_number': '+421900123456', 'date_of_birth': '1990-01-01',
    'id_card_number': 'AB123456', 'birth_number': '9001011234',
    'street_address': 'Hlavná 1', 'city': 'Bratislava', 'postal_code': '81101',
    'bank_account_iban': 'SK8909000000000000000000',
    'amount_requested': '200', 'duration_days': '20',
    'purpose': 'Testovacia žiadosť o pôžičku na overenie funkčnosti.',
    'gdpr_consent': 'on',
}
resp = check('loan_application POST (new borrower)', c.post(reverse('users:loan_application'), form_data))
if resp.status_code == 200:
    form = resp.context['form'] if resp.context and 'form' in resp.context else None
    if form:
        print("   FORM ERRORS:", form.errors)

borrower = User.objects.filter(username='9001011234').first()
if not borrower:
    errors.append("[borrower creation] user 9001011234 was NOT created after loan_application POST")
else:
    print(f"   borrower created: {borrower.username}, kyc_completed={borrower.kyc_completed}")
    auction = Auction.objects.filter(borrower=borrower).first()
    print(f"   auction created: {auction}, status={auction.status if auction else None}")

    check('application_status (logged in via session)', c.get(reverse('users:application_status')))
    check('my_applications before approval (should redirect)', c.get(reverse('users:my_applications')))
    check('my_contracts before approval', c.get(reverse('users:my_contracts')))
    check('my_offers before approval', c.get(reverse('users:my_offers')))
    check('account_settings before approval', c.get(reverse('users:account_settings')))
    check('referral before approval', c.get(reverse('users:referral')))

    admin_c = Client()
    admin_user = User.objects.filter(is_superuser=True).first()
    admin_c.force_login(admin_user)
    check('admin dashboard', admin_c.get(reverse('adminpanel:dashboard')))
    check('admin applications_list', admin_c.get(reverse('adminpanel:applications_list')))
    check('admin application_detail', admin_c.get(reverse('adminpanel:application_detail', args=[auction.pk])))
    check(
        'admin application_approve',
        admin_c.post(reverse('adminpanel:application_approve', args=[auction.pk]), {
            'max_interest_rate': '20', 'duration_days': '20',
        }),
    )
    auction.refresh_from_db()
    print(f"   after approve: status={auction.status}")

    check('my_applications after approval', c.get(reverse('users:my_applications')))
    check('my_contracts after approval', c.get(reverse('users:my_contracts')))
    check('my_offers after approval', c.get(reverse('users:my_offers')))
    check('account_settings after approval', c.get(reverse('users:account_settings')))
    check('referral after approval', c.get(reverse('users:referral')))
    check('notifications', c.get(reverse('core:notifications')))

print("\n--- full repayment cycle test (fund -> sign -> pay -> admin confirm) ---")
if borrower and auction and auction.status == Auction.Status.ACTIVE:
    funder = User.objects.create_user(
        username='fundertest1', email='funder@example.com', password='Zlozite-Heslo123',
        role=User.Role.LENDER, wallet_balance=Decimal('10000'), kyc_completed=True,
        email_verified=True,
    )
    fc = Client()
    fc.force_login(funder)
    check('fund auction (place_bid)', fc.post(reverse('auctions:place_bid', args=[auction.pk])))
    auction.refresh_from_db()
    print(f"   auction status after funding: {auction.status}")

    if auction.status == Auction.Status.SIGNING:
        check('sign_loan_contract GET (email not verified -> redirect)', c.get(
            reverse('users:sign_loan_contract', args=[auction.pk])))
        borrower.email_verified = True
        borrower.save(update_fields=['email_verified'])
        check('sign_loan_contract POST', c.post(reverse('users:sign_loan_contract', args=[auction.pk])))
        auction.refresh_from_db()
        print(f"   auction status after signing: {auction.status}")

    if auction.status == Auction.Status.FUNDED:
        check('my_loans', c.get(reverse('users:my_loans')))
        check('request_postponement POST', c.post(reverse('users:request_postponement', args=[auction.pk])))
        check('report_payment POST', c.post(reverse('users:report_payment', args=[auction.pk])))
        check('contract_loan_agreement PDF (borrower)', c.get(
            reverse('users:contract_loan_agreement', args=[auction.pk])), expect=(200,))
        check('contract_payment_notice PDF (borrower)', c.get(
            reverse('users:contract_payment_notice', args=[auction.pk])), expect=(200,))

        bid = auction.bids.first()
        if bid:
            check('investor contract_loan_agreement PDF', fc.get(
                reverse('auctions:contract_loan_agreement', args=[bid.pk])), expect=(200,))
            check('investor contract_assignment_agreement PDF', fc.get(
                reverse('auctions:contract_assignment_agreement', args=[bid.pk])), expect=(200,))
            check('investor contract_assignment_notice PDF', fc.get(
                reverse('auctions:contract_assignment_notice', args=[bid.pk])), expect=(200,))
            check('bid_toggle_sale (list on secondary market)', fc.post(
                reverse('auctions:bid_toggle_sale', args=[bid.pk])))

print("\n--- repeat application as existing borrower ---")
if borrower:
    repeat_data = {'amount_requested': '150', 'duration_days': '15', 'purpose': 'Druha ziadost testovacie.'}
    check('loan_application POST (repeat borrower)', c.post(reverse('users:loan_application'), repeat_data))

print("\n--- borrower logout ---")
check('logout (POST)', c.post(reverse('users:logout')))
check('login_borrower GET', c.get(reverse('users:login_borrower')))

# ---------------------------------------------------------------------------
print("\n=== INVESTOR JOURNEY ===")
ic = Client()
check('landing investor', ic.get(reverse('core:investor')))
check('signup GET', ic.get(reverse('users:signup')))

signup_data = {
    'username': 'testinvestor1', 'email': 'investor.test@example.com',
    'password1': 'Zlozite-Heslo123', 'password2': 'Zlozite-Heslo123',
    'first_name': 'Eva', 'last_name': 'Investorová', 'phone_number': '+421900555666',
    'date_of_birth': '1985-05-05', 'id_card_number': 'CD654321', 'birth_number': '8505051234',
    'street_address': 'Vedlajsia 2', 'city': 'Kosice', 'postal_code': '04001',
    'bank_account_iban': 'SK8909000000000000000001',
    'gdpr_consent': 'on',
}
resp = check('signup POST', ic.post(reverse('users:signup'), signup_data))
if resp.status_code == 200:
    form = resp.context['form'] if resp.context and 'form' in resp.context else None
    if form:
        print("   SIGNUP FORM ERRORS:", form.errors)

investor = User.objects.filter(username='testinvestor1').first()
if not investor:
    errors.append("[investor signup] user testinvestor1 was NOT created")
else:
    print(f"   investor created: {investor.username}, role={investor.role}")
    investor.email_verified = True
    investor.save(update_fields=['email_verified'])
    check('investor_dashboard', ic.get(reverse('auctions:investor_dashboard')))
    check('investor_history', ic.get(reverse('auctions:investor_history')))
    check('investor_contracts', ic.get(reverse('auctions:investor_contracts')))
    check('tax_statement', ic.get(reverse('auctions:tax_statement')))
    check('open_auctions', ic.get(reverse('auctions:open_auctions')))
    check('marketplace', ic.get(reverse('auctions:marketplace')))
    check('my_profile', ic.get(reverse('users:my_profile')))
    check('account_settings (investor)', ic.get(reverse('users:account_settings')))
    check('referral (investor)', ic.get(reverse('users:referral')))
    check('notifications (investor)', ic.get(reverse('core:notifications')))
    check('auctions:list', ic.get(reverse('auctions:list')))

    check('wallet_deposit POST', ic.post(reverse('auctions:wallet_deposit'), {'amount': '1000'}))
    investor.refresh_from_db()
    print(f"   wallet_balance after deposit request: {investor.wallet_balance}")

    from auctions.models import WalletTransaction
    pending_tx = WalletTransaction.objects.filter(
        user=investor, kind=WalletTransaction.Kind.DEPOSIT, status=WalletTransaction.Status.PENDING,
    ).first()
    if pending_tx:
        admin_c3 = Client()
        admin_c3.force_login(User.objects.filter(is_superuser=True).first())
        check('admin wallet_confirm POST', admin_c3.post(
            reverse('adminpanel:wallet_confirm', args=[pending_tx.pk])))
        investor.refresh_from_db()
        print(f"   wallet_balance after admin confirm: {investor.wallet_balance}")
    else:
        errors.append("[wallet_deposit] no PENDING WalletTransaction was created for investor")

    # vytvor dalsieho testovacieho dlznika + ACTIVE aukciu, aby sme otestovali
    # realny bidding flow investora (nie len kontrolu na prazdny zoznam)
    borrower2 = User.objects.create_user(
        username='9002022222', email='borrower2@example.com', password='x',
        role=User.Role.BORROWER, kyc_completed=True,
    )
    from django.utils import timezone as _tz
    open_auction = Auction.objects.create(
        borrower=borrower2, title='Testovacia aktivna aukcia', description='Test',
        amount_requested=Decimal('100'), max_interest_rate=Decimal('20'),
        duration_days=15, status=Auction.Status.ACTIVE,
        ends_at=_tz.now() + _tz.timedelta(days=15),
    )
    check('auction detail', ic.get(reverse('auctions:detail', args=[open_auction.pk])))
    check('open_auctions shows it', ic.get(reverse('auctions:open_auctions')))
    check('place_bid POST', ic.post(reverse('auctions:place_bid', args=[open_auction.pk])))
    open_auction.refresh_from_db()
    print(f"   auction status after investor bid: {open_auction.status}")
    if open_auction.status != Auction.Status.SIGNING:
        errors.append(f"[place_bid] auction did not move to SIGNING after bid, got {open_auction.status}")

    check('wallet_withdraw POST', ic.post(reverse('auctions:wallet_withdraw'), {'amount': '50'}))

print("\n=== ADMIN PANEL PAGES ===")
admin_c2 = Client()
admin_user2 = User.objects.filter(is_superuser=True).first()
admin_c2.force_login(admin_user2)
for name in ['dashboard', 'applications_list', 'wallet_list', 'loans_list', 'users_list',
             'marketplace_list', 'audit_log', 'contracts_list', 'settings']:
    check(f'admin:{name}', admin_c2.get(reverse(f'adminpanel:{name}')))

print("\n=== STATIC / PUBLIC PAGES ===")
for url_name in ['core:landing', 'core:investor', 'core:borrower', 'core:contact', 'core:faq',
                  'core:terms', 'core:privacy', 'core:public_stats']:
    check(url_name, Client().get(reverse(url_name)))

print("\n\n===================== SUMMARY =====================")
if errors:
    print(f"{len(errors)} PROBLEM(S) FOUND:")
    for e in errors:
        print(" -", e)
else:
    print("No hard errors (non-200/302 status codes) found.")
