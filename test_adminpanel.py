"""Test vlastneho admin prostredia (/sprava/) - dashboard, schvalenie/zamietnutie/
protiponuka ziadosti, potvrdenie/zamietnutie penazenkovej transakcie, blokovanie
uzivatela, pristup len pre superusera."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
os.environ.setdefault('ALLOWED_HOSTS', 'testserver,localhost,127.0.0.1')
django.setup()

from decimal import Decimal
from datetime import timedelta
from django.test import Client
from django.contrib.auth import get_user_model
from django.utils import timezone
from auctions.models import Auction, WalletTransaction
from bids.models import Bid
from adminpanel.models import AuditLog

User = get_user_model()
results = []


def check(name, condition, extra=""):
    status = "PASS" if condition else "FAIL"
    results.append((status, name, extra))
    print(f"[{status}] {name}" + (f" -- {extra}" if extra and status == 'FAIL' else ""))


User.objects.filter(username__in=['ap_borrower', 'ap_investor', 'ap_admin']).delete()

admin_user = User.objects.create_superuser(username='ap_admin', password='x', email='admin@example.com')
borrower = User.objects.create_user(
    username='ap_borrower', password='x', role=User.Role.BORROWER, kyc_completed=True,
    email='ap_borrower@example.com', first_name='Jana', last_name='Testovacia', birth_number='9001019999',
)
investor = User.objects.create_user(
    username='ap_investor', password='x', role=User.Role.LENDER, email='ap_investor@example.com',
)
investor.wallet_balance = Decimal('100')
investor.save()

c = Client(raise_request_exception=False)

# ===== access control =====
r = c.get('/sprava/', follow=True)
check('Anonymous redirected away from admin panel', r.status_code == 200 and 'sprava' not in (r.redirect_chain[-1][0] if r.redirect_chain else ''))

c.force_login(borrower)
r = c.get('/sprava/')
check('Non-superuser blocked from admin panel', r.status_code != 200 or 'login' in r.content.decode(errors='ignore').lower() or r.status_code in (302, 403))
c.logout()

c.force_login(admin_user)
r = c.get('/sprava/')
check('Superuser can access admin dashboard', r.status_code == 200)

# ===== application review =====
auction = Auction.objects.create(
    borrower=borrower, title='t', description='t', amount_requested=Decimal('200'),
    max_interest_rate=Decimal('24'), duration_days=14, status=Auction.Status.PENDING_REVIEW,
    ends_at=timezone.now() + timedelta(days=14),
)
r = c.get('/sprava/ziadosti/')
check('Applications list page loads', r.status_code == 200)
check('Pending application visible in default filter', str(auction.pk).encode() in r.content)

r = c.get(f'/sprava/ziadosti/{auction.pk}/')
check('Application detail page loads', r.status_code == 200)
check('Application detail shows borrower KYC data', b'9001019999' in r.content)

r = c.post(f'/sprava/ziadosti/{auction.pk}/schvalit/', follow=True)
auction.refresh_from_db()
check('Application approved via admin panel', auction.status == Auction.Status.ACTIVE, f'status={auction.status}')
check('AuditLog entry created for approval', AuditLog.objects.filter(target_model='Auction', target_id=str(auction.pk)).exists())

# reject another application
auction2 = Auction.objects.create(
    borrower=borrower, title='t2', description='t2', amount_requested=Decimal('150'),
    max_interest_rate=Decimal('24'), duration_days=14, status=Auction.Status.PENDING_REVIEW,
    ends_at=timezone.now() + timedelta(days=14),
)
r = c.post(f'/sprava/ziadosti/{auction2.pk}/zamietnut/', {'reason': 'test dovod'}, follow=True)
auction2.refresh_from_db()
check('Application rejected via admin panel', auction2.status == Auction.Status.REJECTED)
check('Rejection reason saved', auction2.rejection_reason == 'test dovod')

# counter offer on a third application
auction3 = Auction.objects.create(
    borrower=borrower, title='t3', description='t3', amount_requested=Decimal('300'),
    max_interest_rate=Decimal('24'), duration_days=14, status=Auction.Status.PENDING_REVIEW,
    ends_at=timezone.now() + timedelta(days=14),
)
r = c.post(f'/sprava/ziadosti/{auction3.pk}/protiponuka/', {'amount': '150'}, follow=True)
auction3.refresh_from_db()
check('Counter offer sets status', auction3.status == Auction.Status.COUNTER_OFFER)
check('Counter offer amount saved', auction3.counter_offer_amount == Decimal('150'))

# ===== wallet transactions =====
deposit_tx = WalletTransaction.objects.create(user=investor, kind=WalletTransaction.Kind.DEPOSIT, amount=Decimal('500'))
r = c.get('/sprava/penazenka/')
check('Wallet list page loads', r.status_code == 200)

r = c.post(f'/sprava/penazenka/{deposit_tx.pk}/potvrdit/', follow=True)
deposit_tx.refresh_from_db()
investor.refresh_from_db()
check('Deposit confirmed via admin panel', deposit_tx.status == WalletTransaction.Status.COMPLETED)
check('Wallet balance credited after confirmation', investor.wallet_balance == Decimal('600'), f'balance={investor.wallet_balance}')

withdraw_tx = WalletTransaction.objects.create(user=investor, kind=WalletTransaction.Kind.WITHDRAWAL, amount=Decimal('100'))
investor.wallet_balance -= Decimal('100')
investor.save(update_fields=['wallet_balance'])
r = c.post(f'/sprava/penazenka/{withdraw_tx.pk}/zamietnut/', follow=True)
withdraw_tx.refresh_from_db()
investor.refresh_from_db()
check('Withdrawal rejected via admin panel', withdraw_tx.status == WalletTransaction.Status.REJECTED)
check('Wallet balance refunded after withdrawal rejection', investor.wallet_balance == Decimal('600'), f'balance={investor.wallet_balance}')

# ===== loans list =====
r = c.get('/sprava/pozicky/')
check('Loans list page loads', r.status_code == 200)

# ===== users list / detail / block =====
r = c.get('/sprava/pouzivatelia/?q=ap_borrower')
check('Users search page loads and finds borrower', r.status_code == 200 and b'ap_borrower' in r.content)

r = c.get(f'/sprava/pouzivatelia/{borrower.pk}/')
check('User detail page loads', r.status_code == 200)

r = c.post(f'/sprava/pouzivatelia/{borrower.pk}/blokovat/', follow=True)
borrower.refresh_from_db()
check('User blocked via admin panel', borrower.is_blocked is True)

login_ok = c.login(username='ap_borrower', password='x')
check('Blocked user cannot log in', login_ok is False)

c.force_login(admin_user)
r = c.post(f'/sprava/pouzivatelia/{borrower.pk}/blokovat/', follow=True)
borrower.refresh_from_db()
check('User unblocked via admin panel (toggle)', borrower.is_blocked is False)

login_ok = c.login(username='ap_borrower', password='x')
check('Unblocked user can log in again', login_ok is True)
c.force_login(admin_user)

# ===== marketplace + audit log pages =====
r = c.get('/sprava/trh/')
check('Marketplace page loads', r.status_code == 200)

r = c.get('/sprava/audit/')
check('Audit log page loads', r.status_code == 200)
check('Audit log shows recorded actions', AuditLog.objects.count() >= 3)

User.objects.filter(username__in=['ap_borrower', 'ap_investor', 'ap_admin']).delete()

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
