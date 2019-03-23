from django.core.management.base import BaseCommand
from .models import MTG
from .tcgplayer_api import TcgPlayerApi
import requests

tcg = TcgPlayerApi()


class Command(BaseCommand):
    def handle(self, **options):

        def get_image(product_id):
            url = f'https://api.scryfall.com/cards/tcgplayer/{product_id}'
            r = requests.get(url)
            return r.json()['image_uris']['normal']

        db = MTG.objects.all()

        for each in db:
            sku = each.sku
            product_id = tcg.card_info_by_sku(sku)['results'][0]['productId']
            image = get_image(product_id)
            each.product_id = product_id
            each.image_url = image
            each.save()



