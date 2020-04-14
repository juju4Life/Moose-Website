from django.core.management.base import BaseCommand
from my_customs.decorators import report_error
from my_customs.functions import set_offset
from scryfall_api import get_image
from orders.models import GroupName
from engine.tcgplayer_api import TcgPlayerApi
from engine.tcg_manifest import Manifest
from engine.models import MTG

api = TcgPlayerApi('moose')
manifest = Manifest()


class Command(BaseCommand):
    @report_error
    def handle(self, *args, **options):
        groups = GroupName.objects.filter(category='Magic the Gathering').filter(added=False)
        upload_list = list()

        for group in groups:
            expansion = group.group_name
            print(f"Adding {expansion}")
            count = 0
            cards = set_offset(func=api.get_set_data, group_id=group.group_id)

            for card in cards:
                print(card)
                product_id = card['productId']
                name = card['name']

                image = get_image(product_id)
                if image == '':
                    image = card['imageUrl']
                else:
                    pass

                if MTG.objects.filter(product_id=product_id).exists() is False:

                    upload_list.append(
                        MTG(
                            name=name,
                            expansion=expansion,
                            language='English',
                            image_url=image,
                        )
                    )
                    count += 1
                    print(count)
                break
            group_add_input = input('Changed Group Added to True?\n')
            if group_add_input.lower() == 'yes':
                group.added = True
                group.save()











