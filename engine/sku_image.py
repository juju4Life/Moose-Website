from django.core.management.base import BaseCommand
from .models import MTG
from .tcgplayer_api import TcgPlayerApi

tcg = TcgPlayerApi()


class Command(BaseCommand):
    def handle(self, **options):
        db = MTG.objects.filter(language='English')

        for each in db:
            pass


