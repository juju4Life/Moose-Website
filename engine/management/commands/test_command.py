from django.core.management.base import BaseCommand
from buylist.ck_buylist import ck_buylist, get_page_count
from buylist.scg_buylist import get_scg_buylist
from buylist.gather_buylist_info import add_buylist_data
from engine.get_group_prices import get_tcg_prices


class Command(BaseCommand):
    def handle(self, *args, **options):
        ck_buylist(get_page_count())
        get_scg_buylist()
        # get_tcg_prices()
        # add_buylist_data()
























