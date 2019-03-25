from django.core.management.base import BaseCommand
from engine.models import MTG
from engine.tcgplayer_api import TcgPlayerApi
from scryfall_api import get_image

tcg = TcgPlayerApi()


class Command(BaseCommand):
    def handle(self, **options):

        db = MTG.objects.exclude(condition='Unopened')

        for each in db:
            sku = each.sku
            product_id = tcg.card_info_by_sku(sku)['results'][0]['productId']
            if each.product_id != '':
                try:

                    image = get_image(product_id)
                    each.product_id = product_id
                    each.image_url = image
                    each.save()
                except Exception as e:
                    print(e, each.name, each.expansion)



