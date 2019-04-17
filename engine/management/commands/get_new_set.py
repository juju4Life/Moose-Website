from django.core.management.base import BaseCommand
from engine.tcgplayer import new_set
from engine.tcgplayer_api import TcgPlayerApi
from engine.tcg_manifest import Manifest
from customer.models import ItemizedPreorder
from engine.models import MTG
from scryfall_api import get_image, get_card_data
from orders.models import GroupName
from math import ceil
from tcg.rarity_algorithm import rarity_round

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
                    rarity = ''
                    card_type = ''
                    card_text = ''
                    image = get_image(str(product_id))
                    if image == '':
                        image = each['imageUrl']


                    for ext in each['extendedData']:
                        try:
                            if ext['name'] == 'Rarity':
                                rarity = ext['value']
                        except Exception:
                            rarity = 'Unknown'

                        try:
                            if ext['name'] == 'SubType':
                                card_type = ext['value']
                        except Exception:
                            card_type = 'Unknown'

                        try:
                            if ext['name'] == 'OracleText':
                                card_text = ext['value']
                        except Exception:
                            card_text = 'Unknown'


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

                    try:
                        price_data = tcg.get_market_price(str(product_id))['results']
                        if price_data[0]['subTypeName'] == 'Foil':
                            price_data = price_data[1]
                        elif price_data[0]['subTypeName'] == 'Normal':
                            price_data = price_data[0]

                        price = price_data['marketPrice']
                        low = price_data['lowPrice']
                        if low is not None:
                            if price is not None:
                                if low > price:
                                    price = low
                            else:
                                price = low

                        price = rarity_round(rarity, price)
                    except Exception as e:
                        print(e)
                        price = 0

                    set_name = GroupName.objects.get(group_id=int(group_id))
                    if ItemizedPreorder.objects.filter(product_id=product_id).exists() is False:
                        print(product_name, color, card_type, rarity)
                        new_card = ItemizedPreorder(
                            name=product_name,
                            quantity=8,
                            expansion=set_name,
                            item_type='Single',
                            price=price,
                            custom_price=False,
                            available=True,
                            image_url=image,
                            product_id=product_id,
                            total_sold=0,
                            rarity=rarity,
                            card_text=card_text,
                            card_type=card_type,
                        )
                        new_card.save()

            total -= 100
            offset += 100





