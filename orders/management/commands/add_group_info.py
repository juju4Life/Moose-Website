from django.core.management.base import BaseCommand
from my_customs.decorators import report_error
from my_customs.functions import set_offset
from scryfall_api import get_image, get_card_data
from orders.models import GroupName
from engine.tcgplayer_api import TcgPlayerApi
from engine.tcg_manifest import Manifest
from engine.models import MTG

api = TcgPlayerApi()
manifest = Manifest()


class Command(BaseCommand):
    @report_error
    def handle(self, *args, **options):
        groups = GroupName.objects.filter(category='Magic the Gathering').filter(added=False)
        foil_map = {
            1: False,
            2: True,

        }

        for group in groups:
            expansion = group.group_name
            print(f"Adding {expansion}")
            count = 0
            cards = set_offset(func=api.get_set_data, group_id=group.group_id)

            for card in cards:
                product_id = card['productId']
                name = card['name']
                image = get_image(product_id)
                if image == '':
                    image = card['imageUrl']

                scryfall_info = get_card_data(product_id)
                rarity = ''
                collector_number = ''
                if scryfall_info.get('object') != 'error':
                    rarity = scryfall_info['rarity']
                    collector_number = scryfall_info['collector_number']
                else:
                    pass

                sku_list = api.get_product_sku_list(product_id)

                for sku in sku_list['results']:
                    language = manifest.language(sku['languageId'])
                    if language == 'English':
                        is_foil = foil_map[sku['printingId']]
                        condition = manifest.condition(sku['conditionId'])

                        if MTG.objects.filter(sku=sku).exists() is False:

                            new_entry = MTG(
                                product_name=name,
                                product_line='Magic',
                                title='',
                                rarity=rarity,
                                number=collector_number,
                                set_name=expansion,
                                sku=sku,
                                condition=condition,
                                language=language,
                                foil=is_foil,
                                product_id=product_id,
                                image_url=image,
                            )

                            new_entry.save()
                            count += 1
                            print(count)
            print(expansion)
            group_add_input = input('Changed Group Added to True?\n')
            if group_add_input.lower() == 'yes':
                group.added = True
                group.save()











