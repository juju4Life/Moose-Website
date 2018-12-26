from django.core.management.base import BaseCommand
from engine.tcgplayer import update_case_price

class Command(BaseCommand):
    def handle(self, **options):
       update_case_price()



