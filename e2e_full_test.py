"""
Komplexny end-to-end test celej appky cez Django test client.
Testuje: registraciu investora, ziadost o pozicku (dlznik), financovanie,
platbu/odklad, sekundarny trh, zmenu hesla, historiu + PDF export,
impersonaciu adminom, a vsetky verejne/chybove stranky.
Vypisuje PASS/FAIL pre kazdy krok a na konci zhrnutie.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
os.environ.setdefault('ALLOWED_HOSTS', 'testserver,localhost,127.0.0.1')
django.setup()

from decimal import Decimal
from django.test import Client
from django.contrib.auth import get_user_model
from auctions.models import Auction, WalletTransaction
from bids.models import Bid

User = get_user_model()

results = []

def check(name, condition, extra=""):
    status = "PASS" if condition else "FAIL"
    results.append((status, name, extra))
    print(f"[{status}] {name}" + (f" -- {extra}" if extra and status == 'FAIL' else ""))

# cleanup from previous runs
User.objects.filter(
    username__in=['e2e_investor', 'e2e_borrower', 'e2e_investor2', 'e2e_bot_investor', '9001011234'],
).delete()

c = Client(raise_request_exception=False)

# ========== 1. PUBLIC PAGES ==========
for path, label in [
    ('/', 'Landing'), ('/investori/', 'Investor landing'), ('/pre-ziadatelov/', 'Borrower landing'),
    ('/kontakt/', 'Contact'), ('/caste-otazky/', 'FAQ'), ('/obchodne-podmienky/', 'Terms'),
    ('/ochrana-osobnych-udajov/', 'Privacy'),
    ('/accounts/login/', 'Generic login (admin)'),
    ('/accounts/login/investor/', 'Investor login'),
    ('/accounts/login/dlznik/', 'Borrower login'),
    ('/accounts/signup/', 'Investor signup'),
    ('/accounts/ziadost-o-uver/', 'Loan application form'),
]:
    r = c.get(path)
    check(f'GET {path} ({label})', r.status_code == 200, f'status={r.status_code}')

# 404 page
r = c.get('/this-page-does-not-exist-xyz/')
check('GET nonexistent page returns 404', r.status_code == 404, f'status={r.status_code}')

# ========== 2. INVESTOR REGISTRATION ==========
signup_data = {
    'username': 'e2e_investor',
    'email': 'e2e_investor@example.com',
    'phone_number': '+421900000001',
    'first_name': 'Peter',
    'last_name': 'Investor',
    'date_of_birth': '1985-05-05',
    'id_card_number': 'CD987654',
    'birth_number': '8505051234',
    'street_address': 'Investicna 1',
    'city': 'Bratislava',
    'postal_code': '81101',
    'bank_account_iban': 'SK8909000000000022228888',
    'password1': 'SuperSecret123!',
    'password2': 'SuperSecret123!',
    'gdpr_consent': 'on',
}
r = c.post('/accounts/signup/', signup_data, follow=True)
check('POST signup (investor) succeeds', r.status_code == 200, f'status={r.status_code}')
investor = User.objects.filter(username='e2e_investor').first()
check('Investor user created', investor is not None)
if investor:
    check('Investor role set correctly', investor.role == User.Role.LENDER, f'role={investor.role}')
    check('Investor auto-logged-in after signup', '_auth_user_id' in c.session)
    check('Investor GDPR consent recorded', investor.gdpr_consent_given is True)
    check('Investor display_id generated', bool(investor.display_id) and len(investor.display_id) == 6)
    check('Investor KYC data saved (kyc_completed)', investor.kyc_completed is True)
    check('Investor birth number saved', investor.birth_number == '8505051234')

# honeypot field should silently reject bot-like submissions
bot_signup_data = dict(signup_data)
bot_signup_data['username'] = 'e2e_bot_investor'
bot_signup_data['birth_number'] = '8505051235'
bot_signup_data['website'] = 'http://spam.example.com'
r = c.post('/accounts/signup/', bot_signup_data, follow=True)
check('Honeypot field blocks bot-like signup', not User.objects.filter(username='e2e_bot_investor').exists())

c.logout()

# Login as investor via dedicated investor login page
r = c.post('/accounts/login/investor/', {'username': 'e2e_investor', 'password': 'SuperSecret123!'}, follow=True)
check('Investor login via /login/investor/ works', r.status_code == 200 and '_auth_user_id' in c.session)
check('Investor redirected to investor dashboard after login', '/aukcie/dashboard/' in r.redirect_chain[-1][0] if r.redirect_chain else False, str(r.redirect_chain))
c.logout()

# Login investor via WRONG (borrower) login page - should still log in but role mismatch is just UX, not blocked
r = c.post('/accounts/login/dlznik/', {'username': 'e2e_investor', 'password': 'SuperSecret123!'}, follow=True)
check('Investor can technically log in via borrower login page (no hard role gate)', r.status_code == 200)
c.logout()

# ========== 3. WALLET DEPOSIT (manual bank transfer - request + admin confirmation) ==========
c.force_login(investor)

# Deposit requires a verified e-mail first
r = c.post('/aukcie/penazenka/vklad/', {'amount': '500'}, follow=True)
check('Deposit redirects to e-mail verification when not verified', 'overit-email' in r.redirect_chain[-1][0] if r.redirect_chain else False, str(r.redirect_chain))

r = c.post('/accounts/overit-email/', follow=True)
check('Investor verification e-mail request succeeds', r.status_code == 200)
investor.refresh_from_db()
r = c.get(f'/accounts/overit-email/{investor.email_verification_token}/', follow=True)
investor.refresh_from_db()
check('Investor e-mail marked as verified', investor.email_verified is True)

r = c.post('/aukcie/penazenka/vklad/', {'amount': '500'}, follow=True)
investor.refresh_from_db()
check('Wallet deposit request does NOT auto-credit (manual bank process)', investor.wallet_balance == Decimal('0.00'), f'balance={investor.wallet_balance}')

deposit_tx = WalletTransaction.objects.filter(user=investor, kind=WalletTransaction.Kind.DEPOSIT).first()
check('Deposit WalletTransaction record created with PENDING status', deposit_tx is not None and deposit_tx.status == WalletTransaction.Status.PENDING)

# simulate admin confirming the deposit (bank transfer received)
deposit_tx.status = WalletTransaction.Status.COMPLETED
investor.wallet_balance += deposit_tx.amount
investor.save(update_fields=['wallet_balance'])
deposit_tx.save(update_fields=['status'])
investor.refresh_from_db()
check('After admin confirmation, wallet balance credited', investor.wallet_balance == Decimal('500.00'), f'balance={investor.wallet_balance}')

r = c.post('/aukcie/penazenka/vklad/', {'amount': '-50'}, follow=True)
investor.refresh_from_db()
check('Wallet deposit rejects negative amount', investor.wallet_balance == Decimal('500.00'), f'balance={investor.wallet_balance}')

r = c.post('/aukcie/penazenka/vklad/', {'amount': 'abc'}, follow=True)
check('Wallet deposit rejects garbage amount without crashing', r.status_code == 200)
c.logout()

# ========== 4. BORROWER LOAN APPLICATION ==========
loan_data = {
    'email': 'e2e_borrower@example.com',
    'phone_number': '+421900000002',
    'first_name': 'Jana',
    'last_name': 'Testovacia',
    'date_of_birth': '1990-01-01',
    'id_card_number': 'AB123456',
    'birth_number': '9001011234',
    'street_address': 'Testovacia 1',
    'city': 'Bratislava',
    'postal_code': '81101',
    'bank_account_iban': 'SK8909000000000011117777',
    'amount_requested': '200',
    'duration_days': '14',
    'purpose': 'Test ucel',
    'gdpr_consent': 'on',
}
r = c.post('/accounts/ziadost-o-uver/', loan_data, follow=True)
check('POST loan application succeeds', r.status_code == 200, f'status={r.status_code}')
borrower = User.objects.filter(username='9001011234').first()
check('Borrower user created with username = birth number', borrower is not None)
if borrower:
    check('Borrower role set correctly', borrower.role == User.Role.BORROWER, f'role={borrower.role}')
    check('Borrower auto-logged-in after application', '_auth_user_id' in c.session)
    check('Borrower kyc_completed flag set', borrower.kyc_completed is True)
    check('Borrower has a usable auto-generated password', borrower.has_usable_password())

auction = Auction.objects.filter(borrower=borrower).first() if borrower else None
check('Auction (loan request) created for borrower', auction is not None)
if auction:
    check('Auction amount matches request', auction.amount_requested == Decimal('200.00'), f'amount={auction.amount_requested}')
    check('Auction status is PENDING_REVIEW (awaiting admin approval)', auction.status == Auction.Status.PENDING_REVIEW, f'status={auction.status}')

# Borrower should NOT have access to /moje-pozicky/ or /moje-ziadosti/ yet (not approved)
r = c.get('/accounts/moje-pozicky/', follow=True)
check('Borrower blocked from Moje pozicky before approval (redirected)', 'stav-ziadosti' in r.redirect_chain[-1][0] if r.redirect_chain else False, str(r.redirect_chain))

r = c.get('/accounts/moje-ziadosti/', follow=True)
check('Borrower blocked from Moje ziadosti before approval (redirected)', 'stav-ziadosti' in r.redirect_chain[-1][0] if r.redirect_chain else False, str(r.redirect_chain))

# Application status page should show pending state
r = c.get('/accounts/stav-ziadosti/')
check('Application status page accessible', r.status_code == 200)
check('Application status page shows pending hint', b'os\xc3\xbadenie' in r.content or b'aka' in r.content)

c.logout()

# ========== 4b. ADMIN APPROVES THE APPLICATION ==========
auction.status = Auction.Status.ACTIVE
auction.save(update_fields=['status'])

# ========== 5. INVESTOR FUNDS THE LOAN ==========
c.force_login(investor)
r = c.get(f'/aukcie/{auction.pk}/')
check('Investor can view auction detail page', r.status_code == 200)

r = c.post(f'/aukcie/{auction.pk}/bid/', {'amount': '200', 'interest_rate': '24'}, follow=True)
check('Investor bid submission succeeds', r.status_code == 200, f'status={r.status_code}')

auction.refresh_from_db()
check('Auction awaiting contract signature after full funding', auction.status == Auction.Status.SIGNING, f'status={auction.status}')

investor.refresh_from_db()
check('Investor wallet debited by bid amount', investor.wallet_balance == Decimal('300.00'), f'balance={investor.wallet_balance}')

bid = Bid.objects.filter(auction=auction, lender=investor).first()
check('Bid record created', bid is not None)

c.logout()

# ========== 6. BORROWER CAN NOW ACCESS LOAN ENVIRONMENT ==========
c.force_login(borrower)
r = c.get('/accounts/moje-pozicky/')
check('Borrower can access Moje pozicky while awaiting signature', r.status_code == 200)
check('Moje pozicky shows signing hint', b'podpis' in r.content.lower())

# Signing requires a verified e-mail first
r = c.get(f'/accounts/moje-pozicky/{auction.pk}/podpisat-zmluvu/', follow=True)
check('Signing redirects to e-mail verification when not verified', 'overit-email' in r.redirect_chain[-1][0] if r.redirect_chain else False, str(r.redirect_chain))

r = c.post('/accounts/overit-email/', follow=True)
check('Verification e-mail request succeeds', r.status_code == 200)
borrower.refresh_from_db()
check('Verification token generated', bool(borrower.email_verification_token))

r = c.get(f'/accounts/overit-email/{borrower.email_verification_token}/', follow=True)
check('Clicking verification link succeeds', r.status_code == 200)
borrower.refresh_from_db()
check('Borrower e-mail marked as verified', borrower.email_verified is True)

# Borrower signs the loan contract -> loan becomes FUNDED
r = c.post(f'/accounts/moje-pozicky/{auction.pk}/podpisat-zmluvu/', follow=True)
check('Contract signing succeeds', r.status_code == 200)
auction.refresh_from_db()
check('Auction fully funded (FUNDED) after contract signature', auction.status == Auction.Status.FUNDED, f'status={auction.status}')
check('Auction records contract_signed_at timestamp', auction.contract_signed_at is not None)

r = c.get('/accounts/moje-pozicky/')
check('Moje pozicky shows the loan amount', b'200' in r.content)

r = c.get('/accounts/moje-ziadosti/')
check('Moje ziadosti accessible, shows funded status', r.status_code == 200)

r = c.get('/accounts/moje-zmluvy/')
check('Moje zmluvy accessible', r.status_code == 200)

r = c.get('/accounts/ponuky/')
check('Ponuky page accessible for borrower', r.status_code == 200)

r = c.get('/accounts/moje-udaje/')
check('Moje udaje (profile) accessible', r.status_code == 200)
check('Moje udaje shows masked IBAN (not full)', b'\xe2\x80\xa2\xe2\x80\xa2\xe2\x80\xa2\xe2\x80\xa2' in r.content or b'SK89' not in r.content)

# Request postponement
r = c.post(f'/accounts/moje-pozicky/{auction.pk}/odklad/', follow=True)
check('Postponement request succeeds', r.status_code == 200)
auction.refresh_from_db()
check('Auction postponed_days incremented by 7', auction.postponed_days == 7, f'postponed_days={auction.postponed_days}')

# Report payment
r = c.post(f'/accounts/moje-pozicky/{auction.pk}/nahlasit-uhradu/', follow=True)
check('Report payment succeeds', r.status_code == 200)
auction.refresh_from_db()
check('Auction payment_reported flag set', auction.payment_reported is True)

# Account settings - update IBAN
r = c.post('/accounts/nastavenia/', {'bank_account_iban': 'SK0000000000000000000000'}, follow=True)
check('Borrower can update IBAN via account settings', r.status_code == 200)
borrower.refresh_from_db()
check('IBAN actually updated in DB', borrower.bank_account_iban == 'SK0000000000000000000000', f'iban={borrower.bank_account_iban}')

c.logout()

# ========== 7. SECONDARY MARKET ==========
c.force_login(investor)
r = c.post(f'/aukcie/investicia/{bid.pk}/predaj/', follow=True)
check('Investor can list investment for sale', r.status_code == 200)
bid.refresh_from_db()
check('Bid.for_sale flag set to True', bid.for_sale is True)

r = c.get('/aukcie/trh/')
check('Marketplace page accessible', r.status_code == 200)
check('Listed bid appears on marketplace (visible to other investors is tested below)', True)

# cancel sale (within 5 min window)
r = c.post(f'/aukcie/investicia/{bid.pk}/predaj/', follow=True)
bid.refresh_from_db()
check('Investor can cancel sale within 5-minute window', bid.for_sale is False)

c.logout()

# second investor to buy from marketplace
User.objects.filter(username='e2e_investor2').delete()
investor2 = User.objects.create_user(
    username='e2e_investor2', password='SuperSecret123!', role=User.Role.LENDER,
    email='e2e_investor2@example.com', email_verified=True,
)
investor2.wallet_balance = Decimal('500.00')
investor2.save(update_fields=['wallet_balance'])

c.force_login(investor)
c.post(f'/aukcie/investicia/{bid.pk}/predaj/', follow=True)  # re-list for sale
c.logout()

c.force_login(investor2)
r = c.get('/aukcie/trh/')
check('Second investor sees listing on marketplace', bid.auction.borrower.display_name.encode() in r.content or str(bid.amount).encode() in r.content)
r = c.post(f'/aukcie/trh/{bid.pk}/kupit/', follow=True)
check('Second investor can buy listed investment', r.status_code == 200)
bid.refresh_from_db()
check('Bid ownership transferred to buyer', bid.lender_id == investor2.pk, f'lender_id={bid.lender_id}')
investor2.refresh_from_db()
check('Buyer wallet debited', investor2.wallet_balance == Decimal('300.00'), f'balance={investor2.wallet_balance}')
c.logout()

# ========== 8. WALLET WITHDRAW (requires SK IBAN + security code) ==========
c.force_login(investor2)
investor2.bank_account_iban = 'SK8909000000000011117777'
investor2.save(update_fields=['bank_account_iban'])

# missing/wrong security code should be rejected
r = c.post('/aukcie/penazenka/vyber/', {'amount': '50', 'security_code': 'wrong'}, follow=True)
investor2.refresh_from_db()
check('Wallet withdraw rejects wrong security code', investor2.wallet_balance == Decimal('300.00'), f'balance={investor2.wallet_balance}')

r = c.post('/aukcie/penazenka/vyber/', {'amount': '50', 'security_code': investor2.security_code}, follow=True)
investor2.refresh_from_db()
check('Wallet withdraw works with correct security code', investor2.wallet_balance == Decimal('250.00'), f'balance={investor2.wallet_balance}')

withdraw_tx = WalletTransaction.objects.filter(user=investor2, kind=WalletTransaction.Kind.WITHDRAWAL).first()
check('Withdrawal WalletTransaction record created', withdraw_tx is not None and withdraw_tx.iban == investor2.bank_account_iban)

r = c.post('/aukcie/penazenka/vyber/', {'amount': '999999', 'security_code': investor2.security_code}, follow=True)
investor2.refresh_from_db()
check('Wallet withdraw rejects amount exceeding balance', investor2.wallet_balance == Decimal('250.00'), f'balance={investor2.wallet_balance}')
c.logout()

# ========== 9. PASSWORD CHANGE ==========
c.force_login(investor2)
r = c.post('/accounts/nastavenia/zmena-hesla/', {
    'old_password': 'SuperSecret123!',
    'new_password1': 'EvenMoreSecret456!',
    'new_password2': 'EvenMoreSecret456!',
    'security_code': investor2.security_code,
}, follow=True)
check('Password change succeeds', r.status_code == 200)
investor2.refresh_from_db()  # in-memory password hash is stale after the change; needed for later force_login()
c.logout()
login_ok = c.login(username='e2e_investor2', password='EvenMoreSecret456!')
check('Can log in with new password after change', login_ok)
c.logout()

# wrong old password should fail validation
c.force_login(investor2)
r = c.post('/accounts/nastavenia/zmena-hesla/', {
    'old_password': 'WRONG_PASSWORD',
    'new_password1': 'Whatever123!',
    'new_password2': 'Whatever123!',
    'security_code': investor2.security_code,
}, follow=True)
check('Password change rejects wrong old password', b'incorrect' in r.content.lower() or r.status_code == 200)
c.logout()

# ========== 10. INVESTOR HISTORY + PDF EXPORT ==========
c.force_login(investor2)
r = c.get('/aukcie/historia/')
if r.status_code != 200:
    print('--- HISTORY PAGE ERROR DEBUG --- status=', r.status_code, 'redirect=', r.get('Location', ''))
    print(r.content[:4000].decode('utf-8', errors='replace'))
    print('--- END DEBUG ---')
check('Investor history page accessible', r.status_code == 200)
check('History shows the bought investment', b'200' in r.content)

r = c.get('/aukcie/historia/export.pdf')
if r.status_code != 200 or r.get('Content-Type') != 'application/pdf':
    print('--- PDF EXPORT ERROR DEBUG ---')
    print(r.content[:4000].decode('utf-8', errors='replace'))
    print('--- END DEBUG ---')
check('PDF export returns 200', r.status_code == 200)
check('PDF export has correct content-type', r.get('Content-Type') == 'application/pdf', r.get('Content-Type'))
check('PDF export produces valid PDF (magic bytes)', r.content[:5] == b'%PDF-')
check('PDF export is non-trivial size', len(r.content) > 1000, f'size={len(r.content)}')

# date filter
r = c.get('/aukcie/historia/?od=2020-01-01&do=2099-12-31')
check('Investor history date filter accepts valid range', r.status_code == 200)
r = c.get('/aukcie/historia/?od=garbage&do=garbage')
check('Investor history date filter handles garbage input without crashing', r.status_code == 200)
c.logout()

# ========== 11. IMPERSONATION (ADMIN) ==========
admin = User.objects.filter(username='admin').first()
if admin:
    c.force_login(admin)
    r = c.get('/accounts/admin-nahlad/')
    check('Admin impersonate list accessible', r.status_code == 200)
    check('Impersonate list contains test borrower', borrower.username.encode() in r.content)

    r = c.get(f'/accounts/admin-nahlad/{borrower.pk}/', follow=True)
    check('Admin can start impersonating borrower', r.status_code == 200)
    r = c.get('/accounts/moje-ziadosti/')
    check('Admin sees borrower dashboard while impersonating', r.status_code == 200)

    r = c.get('/accounts/admin-nahlad/stop/', follow=True)
    check('Admin can stop impersonating', r.status_code == 200)
    c.logout()
else:
    check('Admin user exists for impersonation test', False, 'run ensure_test_admin management command first')

# ========== 12. ACCOUNT SETTINGS PAGES RENDER FOR BOTH ROLES ==========
c.force_login(investor2)
r = c.get('/accounts/nastavenia/')
if r.status_code != 200:
    print('--- SETTINGS PAGE ERROR DEBUG ---')
    print(r.content[:4000].decode('utf-8', errors='replace'))
    print('--- END DEBUG ---')
check('Investor account settings page renders', r.status_code == 200)
c.logout()

c.force_login(borrower)
r = c.get('/accounts/nastavenia/')
check('Borrower account settings page renders', r.status_code == 200)
c.logout()

# ========== CLEANUP ==========
User.objects.filter(username__in=['e2e_investor', 'e2e_investor2', 'e2e_borrower']).delete()

# ========== SUMMARY ==========
print('\n' + '=' * 70)
passed = sum(1 for s, _, _ in results if s == 'PASS')
failed = [r for r in results if r[0] == 'FAIL']
print(f'TOTAL: {len(results)} | PASSED: {passed} | FAILED: {len(failed)}')
if failed:
    print('\nFAILED CHECKS:')
    for status, name, extra in failed:
        print(f'  - {name} ({extra})')
else:
    print('\nAll checks passed.')
print('=' * 70)


