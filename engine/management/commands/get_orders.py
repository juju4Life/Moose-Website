from django.core.management.base import BaseCommand
from engine.tcgplayer import full_order
from engine.tracker import Database


class Command(BaseCommand):
    def handle(self, **options):
        full_order()
        Database().update_foreign()



