from django.core.management.base import BaseCommand
from engine.update_direct import update


class Command(BaseCommand):
    def handle(self, **options):
        update()






