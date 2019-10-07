from django.core.management.base import BaseCommand
from buylist.ck_buylist import ck_buylist, get_page_count


class Command(BaseCommand):
    def handle(self, *args, **options):
        ck_buylist(get_page_count())






















