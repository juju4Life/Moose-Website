from django.core.management.base import BaseCommand
from engine.tcgplayer_api import TcgPlayerApi


api = TcgPlayerApi()


class Command(BaseCommand):
    def handle(self, **options):
        pass



