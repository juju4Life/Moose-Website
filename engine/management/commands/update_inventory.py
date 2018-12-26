from django.core.management.base import BaseCommand
from engine.tcgplayer import update_inventory

class Command(BaseCommand):
    def handle(self, **options):
       update_inventory()



