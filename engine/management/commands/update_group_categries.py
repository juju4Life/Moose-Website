from django.core.management.base import BaseCommand
from engine.tcgplayer import buylist_hub

class Command(BaseCommand):
    def handle(self, **options):
       buylist_hub()



