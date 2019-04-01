from django.core.management.base import BaseCommand
from engine.tcgplayer import new_set
from engine.tcgplayer_api import TcgPlayerApi
from engine.tcg_manifest import Manifest
from customer.models import ItemizedPreorder
from engine.models import MTG
from scryfall_api import get_image, get_card_data
from orders.models import GroupName

manifest = Manifest()
tcg = TcgPlayerApi()


class Command(BaseCommand):
    def handle(self, **options):
        convert_to_color = {
            'B': 'Black',
            'U': 'Blue',
            'R': 'Red',
            'G': 'Green',
            'W': 'White',
        }
        user_input = input('Input Group ID: ')
        group_id = str(user_input)
        total = tcg.get_set_data(group_id)['totalItems']
        print(total)
        offset = 0
        while total > 0:
            data = tcg.get_set_data(group_id, offset=offset)['results']
            for each in data:
                product_id = each['productId']
                try:
                    product_name = each['name']
                except KeyError:
                    product_name = None

                if product_name is not None:
                    image = get_image(str(product_id))
                    if image == '':
                        image = each['imageUrl']

                    rarity = each['extendedData'][0]['value']
                    try:
                        color = get_card_data(str(product_id))['colors']
                    except KeyError:
                        color = None

                    if color is not None:
                        if len(color) < 1:
                            color = 'Colorless'
                        elif len(color) == 1:
                            color = convert_to_color[color[0]]
                        else:
                            color = 'Multi-color'

                    set_name = GroupName.objects.get(group_id=int(group_id))

                    if ItemizedPreorder.objects.filter(product_id=product_id) is False:
                        new_preorder = ItemizedPreorder(

                        )
            total -= 100
            offset += 100





