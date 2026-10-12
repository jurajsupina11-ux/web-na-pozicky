"""Test generovania zmluvnej dokumentacie (PDF) - zmluva o pozicke, predpis,
potvrdenie o zaniku dlhu, oznamenie o postupeni, zmluva o postupeni pohladavky."""
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
from auctions.models import Auction
from bids.models import Bid

User = get_user_model()
results = []

def check(name, condition, extra=""):
    status = "PASS" if condition else "FAIL"
    results.append((status, name, extra))
    print(f"[{status}] {name}" + (f" -- {extra}" if extra and status == 'FAIL' else ""))

User.objects.filter(username__in=['ct_borrower', 'ct_investor', 'ct_investor2']).delete()
c = Client(raise_request_exception=False)

borrower = User.objects.create_user(username='ct_borrower', password='x', role=User.Role.BORROWER, kyc_completed=True)
investor = User.objects.create_user(username='ct_investor', password='x', role=User.Role.LENDER)
investor2 = User.objects.create_user(username='ct_investor2', password='x', role=User.Role.LENDER)
investor2.wallet_balance = Decimal('100')
investor2.save()

loan = Auction.objects.create(
    borrower=borrower, title='t', description='t', amount_requested=Decimal('200'),
    max_interest_rate=Decimal('24'), duration_days=14, status=Auction.Status.FUNDED,
    ends_at=timezone.now() + timedelta(days=14),
)
bid = Bid.objects.create(auction=loan, lender=investor, amount=Decimal('200'), interest_rate=Decimal('24'))

# ===== borrower: zmluva o pozicke, predpis k uhrade =====
c.force_login(borrower)
r = c.get(f'/accounts/moje-zmluvy/{loan.pk}/zmluva.pdf')
check('Borrower loan agreement PDF returns 200', r.status_code == 200, f'status={r.status_code}')
check('Borrower loan agreement PDF is valid PDF', r.content[:5] == b'%PDF-')
check('Borrower loan agreement PDF non-trivial size', len(r.content) > 1000)

r = c.get(f'/accounts/moje-zmluvy/{loan.pk}/predpis.pdf')
check('Payment notice PDF returns 200', r.status_code == 200, f'status={r.status_code}')
check('Payment notice PDF is valid PDF', r.content[:5] == b'%PDF-')

r = c.get(f'/accounts/moje-zmluvy/{loan.pk}/potvrdenie-o-zaniku-dlhu.pdf')
check('Debt discharge PDF blocked for non-closed loan (redirect)', r.status_code in (302, 404), f'status={r.status_code}')
c.logout()

# close the loan and re-check discharge certificate
loan.status = Auction.Status.CLOSED
loan.save(update_fields=['status'])
c.force_login(borrower)
r = c.get(f'/accounts/moje-zmluvy/{loan.pk}/potvrdenie-o-zaniku-dlhu.pdf')
check('Debt discharge PDF returns 200 for closed loan', r.status_code == 200, f'status={r.status_code}')
check('Debt discharge PDF is valid PDF', r.content[:5] == b'%PDF-')
c.logout()

# ===== investor: zmluva o pozicke =====
c.force_login(investor)
r = c.get(f'/aukcie/investicia/{bid.pk}/zmluva.pdf')
check('Investor loan agreement PDF returns 200', r.status_code == 200, f'status={r.status_code}')
check('Investor loan agreement PDF is valid PDF', r.content[:5] == b'%PDF-')

r = c.get(f'/aukcie/investicia/{bid.pk}/zmluva-o-postupeni.pdf')
check('Assignment agreement blocked before any transfer (redirect)', r.status_code == 302, f'status={r.status_code}')
c.logout()

# ===== simulate secondary market transfer =====
bid.previous_lender = investor
bid.transferred_at = timezone.now()
bid.lender = investor2
bid.save(update_fields=['previous_lender', 'transferred_at', 'lender'])

c.force_login(investor2)
r = c.get(f'/aukcie/investicia/{bid.pk}/zmluva-o-postupeni.pdf')
check('Assignment agreement PDF returns 200 for buyer after transfer', r.status_code == 200, f'status={r.status_code}')
check('Assignment agreement PDF is valid PDF', r.content[:5] == b'%PDF-')

r = c.get(f'/aukcie/investicia/{bid.pk}/oznamenie-o-postupeni.pdf')
check('Assignment notice PDF returns 200 for buyer', r.status_code == 200, f'status={r.status_code}')
check('Assignment notice PDF is valid PDF', r.content[:5] == b'%PDF-')
c.logout()

c.force_login(investor)
r = c.get(f'/aukcie/investicia/{bid.pk}/zmluva-o-postupeni.pdf')
check('Assignment agreement PDF returns 200 for original seller too', r.status_code == 200, f'status={r.status_code}')
c.logout()

c.force_login(borrower)
r = c.get(f'/aukcie/investicia/{bid.pk}/oznamenie-o-postupeni.pdf')
check('Assignment notice PDF accessible by borrower too', r.status_code == 200, f'status={r.status_code}')
c.logout()

# random third party should not access
User.objects.filter(username='ct_outsider').delete()
outsider = User.objects.create_user(username='ct_outsider', password='x', role=User.Role.LENDER)
c.force_login(outsider)
r = c.get(f'/aukcie/investicia/{bid.pk}/zmluva-o-postupeni.pdf')
check('Outsider blocked from assignment agreement', r.status_code == 302, f'status={r.status_code}')
c.logout()

User.objects.filter(username__in=['ct_borrower', 'ct_investor', 'ct_investor2', 'ct_outsider']).delete()

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
