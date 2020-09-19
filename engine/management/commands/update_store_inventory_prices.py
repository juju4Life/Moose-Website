from django.core.management.base import BaseCommand
from engine.store_inventory import Inventory


class Command(BaseCommand):
    def handle(self, *args, **options):
        Inventory().update_store_inventory()


