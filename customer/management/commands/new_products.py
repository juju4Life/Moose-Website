from django.core.management.base import BaseCommand
from customer.products_release_date import mtg


class Command(BaseCommand):
    def handle(self, **options):
        mtg()


