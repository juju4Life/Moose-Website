from django.core.management.base import BaseCommand
from engine.tcgplayer_api import TcgPlayerApi


class Command(BaseCommand):
    def handle(self, *args, **options):
        api = TcgPlayerApi("moose")

        listed_cards = api.get_category_skus('magic')
        print(listed_cards)
        if listed_cards['success'] is True:
            print(listed_cards["totalItems"])


