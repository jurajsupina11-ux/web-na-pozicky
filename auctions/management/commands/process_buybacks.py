"""Garancia odkúpenia - ak dlžník nesplatí pôžičku do BUYBACK_DAYS_AFTER_DUE dní
po splatnosti, platforma automaticky odkúpi pohľadávku od investora: investor
dostane istinu + dohodnutý úrok (za pôvodnú dobu splatnosti) vyplatené na
peňaženku, pôžička prechádza do stavu CLOSED (bought_back=True) a ďalšie
vymáhanie dlhu preberá platforma. Určené na pravidelné spúšťanie (napr. raz
denne cez Render Cron Job): `python manage.py process_buybacks`."""
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from auctions.models import Auction
from core.emails import send_buyback_notice_borrower, send_buyback_notice_lender
from core.models import Notification, notify

#: Počet dní po splatnosti, po ktorých platforma automaticky odkúpi pôžičku.
BUYBACK_DAYS_AFTER_DUE = 90


class Command(BaseCommand):
    help = 'Automaticky odkúpi pôžičky nesplatené viac ako 90 dní po splatnosti (garancia odkúpenia).'

    def handle(self, *args, **options):
        now = timezone.now()
        candidates = Auction.objects.filter(
            status=Auction.Status.FUNDED,
            bought_back=False,
        ).select_related('borrower')

        count = 0
        for loan in candidates:
            days_overdue = (now - loan.computed_due_date).days
            if days_overdue < BUYBACK_DAYS_AFTER_DUE:
                continue

            bid = loan.bids.select_related('lender').first()
            if not bid:
                continue

            interest = bid.amount * (bid.interest_rate / Decimal('100')) * (
                Decimal(loan.duration_days) / Decimal('365')
            )
            payout = round(bid.amount + interest, 2)

            lender = bid.lender
            lender.wallet_balance += payout
            lender.save(update_fields=['wallet_balance'])

            loan.status = Auction.Status.CLOSED
            loan.bought_back = True
            loan.bought_back_at = now
            loan.save(update_fields=['status', 'bought_back', 'bought_back_at'])

            send_buyback_notice_lender(lender, loan)
            send_buyback_notice_borrower(loan.borrower, loan)
            notify(
                lender,
                'Pôžička bola odkúpená - vyplatených ' + f'{payout} €',
                f'Pôžička #{loan.pk} nebola splatená do {BUYBACK_DAYS_AFTER_DUE} dní po splatnosti, '
                f'garancia odkúpenia vám vyplatila {payout} € na peňaženku.',
                kind=Notification.Kind.SUCCESS,
                url='/aukcie/historia/',
            )
            notify(
                loan.borrower,
                'Vaša pôžička bola odkúpená platformou',
                f'Pôžička #{loan.pk} bola odkúpená platformou, dlh evidujeme priamo voči nám.',
                kind=Notification.Kind.WARNING,
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f'Automaticky odkúpených pôžičiek: {count}.'))
