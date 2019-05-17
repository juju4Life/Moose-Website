from django.core.management.base import BaseCommand
from engine.models import MTG
from engine.tcgplayer_api import TcgPlayerApi
from scryfall_api import get_image

tcg = TcgPlayerApi()


class Command(BaseCommand):
    def handle(self, **options):

        db = MTG.objects.exclude(condition='Unopened').filter(product_id='')

        for each in db:
            sku = each.sku
            try:
                product_id = tcg.card_info_by_sku(sku)['results'][0]['productId']
            except Exception as e:
                print(f'{e, each.product_name, each.set_name}')
                product_id = ''

            if product_id != '':
                try:
                    image = get_image(product_id)
                    each.product_id = product_id
                    each.image_url = image
                    each.save()

                    print(f"uploaded {each.product_name, each.set_name} {each.product_id}")
                except Exception as e:
                    print(e, each.product_name, each.set_name)



