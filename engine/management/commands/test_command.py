from time import time
from decouple import config
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from buylist.ck_buylist import ck_buylist, get_page_count
from buylist.scg_buylist import get_scg_buylist
from buylist.gather_buylist_info import add_buylist_data
from engine.get_group_prices import get_tcg_prices


class Command(BaseCommand):
    def handle(self, *args, **options):
        start = time()

        ck_buylist(get_page_count())
        get_scg_buylist()
        print('Getting Tcg group prices')
        get_tcg_prices()
        print('gathering buylist data')
        add_buylist_data()

        end = time()
        elapsed = (end - start) / 3600
        send_mail(
            subject=f'Buylist Hub Time: {elapsed} Hours',
            message=f'Buylist hub finished in {elapsed} hours',
            from_email='TCGFirst',
            recipient_list=[config('my_email'), ]
        )























