from django.core.management.base import BaseCommand
from engine.tcgplayer_api import TcgPlayerApi

api = TcgPlayerApi("moose")


class Command(BaseCommand):
    def handle(self, *args, **options):
        pass

