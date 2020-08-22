
from django.core.management.base import BaseCommand
from engine.update_mtg_skus import update_skus


class Command(BaseCommand):
    def handle(self, *args, **options):
        update_skus()


