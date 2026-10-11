from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from auctions.models import Auction
from bids.models import Bid
from users.models import User

#: Testovacie demo účty - slúžia len na manuálne overenie oboch prostredí
#: (investor aj dlžník) cez Admin náhľad, bez nutnosti prejsť celým flow
#: registrácie/žiadosti. Nie sú nijako overené, nepoužívajú sa produkčne.
TEST_BORROWER_USERNAME = 'demo_dlznik'
TEST_BORROWER_PASSWORD = 'DemoTest2026!'

TEST_LENDER_USERNAME = 'demo_investor'
TEST_LENDER_PASSWORD = 'DemoTest2026!'


class Command(BaseCommand):
    help = 'Vytvorí (ak ešte neexistujú) demo dlžníka s aktívnou pôžičkou a demo investora, aby bolo možné oba typy prostredia hneď vyskúšať cez Admin náhľad.'

    def handle(self, *args, **options):
        borrower, b_created = User.objects.get_or_create(
            username=TEST_BORROWER_USERNAME,
            defaults={
                'email': 'demo.dlznik@pozickypredlznikov.sk',
                'role': User.Role.BORROWER,
                'first_name': 'Demo',
                'last_name': 'Dlžník',
                'phone_number': '0900000001',
                'date_of_birth': '1990-01-01',
                'id_card_number': 'AB111111',
                'birth_number': '9001011111',
                'street_address': 'Demo ulica 1',
                'city': 'Bratislava',
                'postal_code': '81101',
                'bank_account_iban': 'SK0000000000000000000001',
                'kyc_completed': True,
            },
        )
        borrower.set_password(TEST_BORROWER_PASSWORD)
        borrower.role = User.Role.BORROWER
        borrower.kyc_completed = True
        borrower.save()

        lender, l_created = User.objects.get_or_create(
            username=TEST_LENDER_USERNAME,
            defaults={
                'email': 'demo.investor@pozickypredlznikov.sk',
                'role': User.Role.LENDER,
                'phone_number': '0900000002',
            },
        )
        lender.set_password(TEST_LENDER_PASSWORD)
        lender.role = User.Role.LENDER
        if lender.wallet_balance < Decimal('100'):
            lender.wallet_balance = Decimal('1000')
        lender.save()

        # Zabezpečí demo dlžníkovi jednu aktívnu (vyfinancovanú) pôžičku,
        # aby bolo prostredie "Moje pôžičky" / Dashboard hneď vidieť naplnené.
        auction, a_created = Auction.objects.get_or_create(
            borrower=borrower,
            title='Demo žiadosť o pôžičku 200 € na 14 dní',
            defaults={
                'description': 'Demo žiadosť vytvorená automaticky pre testovanie prostredia dlžníka.',
                'amount_requested': Decimal('200'),
                'max_interest_rate': Decimal('24'),
                'duration_days': 14,
                'status': Auction.Status.FUNDED,
                'ends_at': timezone.now() + timezone.timedelta(days=14),
            },
        )
        if auction.status != Auction.Status.FUNDED:
            auction.status = Auction.Status.FUNDED
            auction.save(update_fields=['status'])

        Bid.objects.get_or_create(
            auction=auction,
            lender=lender,
            defaults={'amount': Decimal('200'), 'interest_rate': Decimal('24')},
        )

        self.stdout.write(self.style.SUCCESS(
            f'Demo účty pripravené: dlžník "{TEST_BORROWER_USERNAME}" (s aktívnou pôžičkou) '
            f'a investor "{TEST_LENDER_USERNAME}" (heslo pre oba: {TEST_BORROWER_PASSWORD}).',
        ))
