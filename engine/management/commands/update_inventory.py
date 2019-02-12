from django.core.management.base import BaseCommand
from engine.tcgplayer import update_inventory
from my_customs.decorators import report_error


class Command(BaseCommand):
    @report_error
    def handle(self, **options):
       update_inventory()



