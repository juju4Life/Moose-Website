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
        end = time()
        elapsed = (end - start) / 3600

        two_start = time()
        get_scg_buylist()
        two_stop = time()
        two_elapsed = (two_stop - two_start) / 3600

        three_start = time()
        get_tcg_prices()
        three_stop = time()
        three_elapsed = (three_stop - three_start) / 3600

        four_start = time()
        add_buylist_data()
        four_stop = time()
        four_elapsed = (four_stop - four_start) / 3600

        send_mail(
            subject=f'Buylist Hub Time\nCK: {elapsed} Hours\nSCG: {two_elapsed}\nTCG Prices: {three_elapsed}\ncreate_hub: {four_elapsed}',
            message=f'Buylist hub finished in {elapsed} hours',
            from_email='TCGFirst',
            recipient_list=[config('my_email'), ]
        )























