"""Test novych funkcii: all-or-nothing bidding, buyback po 90 dnoch,
notifikacie, danovy vykaz, verejne statistiky, referral, vernostny program."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
os.environ.setdefault('ALLOWED_HOSTS', 'testserver,localhost,127.0.0.1')
django.setup()

from decimal import Decimal
from django.test import Client
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.utils import timezone
from datetime import timedelta
from auctions.models import Auction
from bids.models import Bid
from core.models import Notification

User = get_user_model()
results = []

def check(name, condition, extra=""):
    status = "PASS" if condition else "FAIL"
    results.append((status, name, extra))
    print(f"[{status}] {name}" + (f" -- {extra}" if extra and status == 'FAIL' else ""))

User.objects.filter(username__in=['nf_investor', 'nf_investor2', 'nf_borrower', 'nf_ref_investor']).delete()

c = Client(raise_request_exception=False)

# ===== all-or-nothing bidding =====
investor = User.objects.create_user(username='nf_investor', password='x', role=User.Role.LENDER)
investor.wallet_balance = Decimal('100')
investor.save()
borrower = User.objects.create_user(
    username='nf_borrower', password='x', role=User.Role.BORROWER, kyc_completed=True,
    email='nf_borrower@example.com', email_verified=True,
)
auction = Auction.objects.create(
    borrower=borrower, title='t', description='t', amount_requested=Decimal('200'),
    max_interest_rate=Decimal('24'), duration_days=14, status=Auction.Status.ACTIVE,
    ends_at=timezone.now() + timedelta(days=14),
)
c.force_login(investor)
r = c.post(f'/aukcie/{auction.pk}/bid/', {}, follow=True)
auction.refresh_from_db()
check('Insufficient wallet blocks funding (all-or-nothing)', auction.status == Auction.Status.ACTIVE, f'status={auction.status}')

investor.wallet_balance = Decimal('200')
investor.save()
r = c.post(f'/aukcie/{auction.pk}/bid/', {}, follow=True)
auction.refresh_from_db()
check('Full funding moves auction to SIGNING (awaiting contract)', auction.status == Auction.Status.SIGNING, f'status={auction.status}')
bid = Bid.objects.filter(auction=auction).first()
check('Bid amount equals full requested amount', bid.amount == Decimal('200'), f'amount={bid.amount}')
check('Bid interest rate equals auction max_interest_rate', bid.interest_rate == Decimal('24'), f'rate={bid.interest_rate}')
c.logout()

# Borrower signs the contract -> auction becomes FUNDED and money is released
c.force_login(borrower)
r = c.post(f'/accounts/moje-pozicky/{auction.pk}/podpisat-zmluvu/', follow=True)
auction.refresh_from_db()
check('Auction becomes FUNDED after borrower signs contract', auction.status == Auction.Status.FUNDED, f'status={auction.status}')
c.logout()

# ===== buyback after 90 days =====
auction.starts_at = timezone.now() - timedelta(days=200)
auction.save(update_fields=['starts_at'])
investor.refresh_from_db()
balance_before = investor.wallet_balance
call_command('process_buybacks')
auction.refresh_from_db()
check('Auction bought back after 90+ days overdue', auction.bought_back is True)
check('Auction status set to CLOSED after buyback', auction.status == Auction.Status.CLOSED)
investor.refresh_from_db()
check('Lender wallet credited with principal+interest on buyback', investor.wallet_balance > balance_before, f'balance={investor.wallet_balance}')
check('Buyback notification created for lender', Notification.objects.filter(user=investor, kind=Notification.Kind.SUCCESS).exists())
check('Buyback notification created for borrower', Notification.objects.filter(user=borrower, kind=Notification.Kind.WARNING).exists())

# ===== notifications UI =====
c.force_login(investor)
r = c.get('/notifikacie/')
check('Notifications list page loads for investor', r.status_code == 200)
notif = Notification.objects.filter(user=investor).first()
r = c.get(f'/notifikacie/precitat/{notif.pk}/', follow=True)
notif.refresh_from_db()
check('Marking single notification as read works', notif.is_read is True)
r = c.get('/notifikacie/precitat-vsetky/', follow=True)
check('Mark-all-read endpoint works', r.status_code == 200)
check('All notifications marked read', not Notification.objects.filter(user=investor, is_read=False).exists())
c.logout()

c.force_login(borrower)
r = c.get('/notifikacie/')
check('Notifications list page loads for borrower (different template)', r.status_code == 200)
c.logout()

# ===== public stats =====
r = c.get('/statistiky/')
check('Public stats page loads (anonymous)', r.status_code == 200)

# ===== tax statement =====
closed_bid_year = auction.computed_due_date.year
c.force_login(investor)
r = c.get('/aukcie/danovy-vykaz/')
check('Tax statement page loads', r.status_code == 200)
r = c.get(f'/aukcie/danovy-vykaz/{closed_bid_year}/export.pdf')
check('Tax statement PDF export returns 200', r.status_code == 200)
check('Tax statement PDF has correct content-type', r.get('Content-Type') == 'application/pdf', r.get('Content-Type'))
check('Tax statement PDF valid magic bytes', r.content[:5] == b'%PDF-')
c.logout()

# ===== referral program =====
c.force_login(investor)
r = c.get('/accounts/pozvi-priatela/')
check('Referral page loads for investor', r.status_code == 200)
check(
    'Referral page shows loyalty tier',
    b'Bronz' in r.content or b'Striebro' in r.content or b'Zlato' in r.content or b'Platina' in r.content,
)
c.logout()

investor.refresh_from_db()
ref_code = investor.referral_code
check('Referral code generated for existing user', bool(ref_code) and len(ref_code) == 8, f'code={ref_code}')

r = c.get(f'/accounts/signup/?ref={ref_code}')
check('Signup page with ref param loads', r.status_code == 200)

signup_data = {
    'username': 'nf_ref_investor', 'email': 'nf_ref@example.com', 'phone_number': '+421900000099',
    'password1': 'SuperSecret123!', 'password2': 'SuperSecret123!', 'gdpr_consent': 'on', 'ref_code': ref_code,
}
r = c.post(f'/accounts/signup/?ref={ref_code}', signup_data, follow=True)
ref_investor = User.objects.filter(username='nf_ref_investor').first()
check('Referred user created', ref_investor is not None)
if ref_investor:
    check('Referred user has referred_by set correctly', ref_investor.referred_by_id == investor.pk)

    ref_investor.wallet_balance = Decimal('50')
    ref_investor.save()
    auction2 = Auction.objects.create(
        borrower=borrower, title='t2', description='t2', amount_requested=Decimal('50'),
        max_interest_rate=Decimal('24'), duration_days=14, status=Auction.Status.ACTIVE,
        ends_at=timezone.now() + timedelta(days=14),
    )
    investor_balance_before = investor.wallet_balance
    c.force_login(ref_investor)
    r = c.post(f'/aukcie/{auction2.pk}/bid/', {}, follow=True)
    ref_investor.refresh_from_db()
    investor.refresh_from_db()
    check('Referred user got referral bonus after first investment', ref_investor.referral_reward_granted is True)
    check('Referrer got referral bonus too', investor.wallet_balance > investor_balance_before, f'balance={investor.wallet_balance}')
    c.logout()

User.objects.filter(username__in=['nf_investor', 'nf_investor2', 'nf_borrower', 'nf_ref_investor']).delete()

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
