from django.core.management.base import BaseCommand
from buylist.ck_buylist import ck_buylist, get_page_count
from buylist.scg_buylist import get_scg_buylist


class Command(BaseCommand):
    def handle(self, *args, **options):
        ck_buylist(get_page_count())
        get_scg_buylist()
























