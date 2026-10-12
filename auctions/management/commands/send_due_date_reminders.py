"""Odošle e-mailové pripomienky dlžníkom - blížiaca sa alebo prekročená
splatnosť pôžičky. Určené na pravidelné spúšťanie (napr. raz denne cez
Render Cron Job): `python manage.py send_due_date_reminders`."""
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from auctions.models import Auction
from core.emails import send_payment_due_soon_reminder, send_payment_overdue_reminder

#: Koľko dní pred splatnosťou sa má poslať pripomienka.
REMINDER_DAYS_BEFORE = 3


class Command(BaseCommand):
    help = 'Pošle e-mailové pripomienky dlžníkom s blížiacou sa alebo prekročenou splatnosťou.'

    def handle(self, *args, **options):
        now = timezone.now()
        active_loans = Auction.objects.filter(
            status=Auction.Status.FUNDED,
            payment_reported=False,
        )

        sent_due_soon = sent_overdue = 0
        for loan in active_loans:
            due_date = loan.starts_at + timedelta(days=loan.duration_days + loan.postponed_days)
            days_left = (due_date - now).days

            if due_date < now:
                send_payment_overdue_reminder(loan.borrower, loan)
                sent_overdue += 1
            elif 0 <= days_left <= REMINDER_DAYS_BEFORE:
                send_payment_due_soon_reminder(loan.borrower, loan, max(days_left, 1))
                sent_due_soon += 1

        self.stdout.write(self.style.SUCCESS(
            f'Odoslané pripomienky: {sent_due_soon} blížiaca sa splatnosť, '
            f'{sent_overdue} po splatnosti.',
        ))
