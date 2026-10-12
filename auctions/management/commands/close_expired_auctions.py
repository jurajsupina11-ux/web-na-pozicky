"""Automaticky zruší žiadosti o pôžičku (aukcie), ktoré neboli vyfinancované
do konca lehoty (ends_at). Určené na pravidelné spúšťanie (napr. každú hodinu
cez Render Cron Job): `python manage.py close_expired_auctions`."""
from django.core.management.base import BaseCommand
from django.utils import timezone

from auctions.models import Auction
from core.emails import send_auction_expired
from core.models import Notification, notify


class Command(BaseCommand):
    help = 'Zruší aktívne žiadosti o pôžičku, ktorým uplynula lehota (ends_at) bez financovania.'

    def handle(self, *args, **options):
        now = timezone.now()
        expired = Auction.objects.filter(status=Auction.Status.ACTIVE, ends_at__lt=now).select_related('borrower')

        count = 0
        for auction in expired:
            auction.status = Auction.Status.CANCELLED
            auction.save(update_fields=['status'])
            send_auction_expired(auction.borrower, auction)
            notify(
                auction.borrower,
                'Žiadosť o pôžičku bola zrušená',
                f'Žiadosť o pôžičku {auction.amount_requested} € nebola vyfinancovaná v lehote a bola zrušená.',
                kind=Notification.Kind.WARNING,
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f'Zrušených žiadostí po uplynutí lehoty: {count}.'))
