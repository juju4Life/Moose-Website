from datetime import datetime
from pytz import timezone

from django.core.management.base import BaseCommand
from my_customs.decorators import report_error
from my_customs.functions import set_offset
from scryfall_api import get_image
from orders.models import GroupName
from engine.add_card_info import add_info
from engine.tcgplayer_api import TcgPlayerApi
from engine.tcg_manifest import Manifest
from engine.models import MTG

api = TcgPlayerApi('moose')
manifest = Manifest()


class Command(BaseCommand):
    # @report_error
    def handle(self, *args, **options):
        '''
        cats = ["Dragon Shield Card Sleeves", 'KMC Card Sleeves', 'Monster Protectors Card Sleeves', 'BCW Card Sleeves', 'Pirate Lab Card Sleeves',
                "Player's Choice Card Sleeves", "Ultimate Guard Card Sleeves", "Ultra Pro Card Sleeves", "Dex Protection Card Sleeves", "Legion Premium "
                                                                                                                                        "Supplies Card "
                                                                                                                                        "Sleeves",
                ] 
                '''

        groups = GroupName.objects.filter(category="Magic the Gathering", added=False)
        for group in groups:
            category = group.category
            upload_list = list()
            expansion = group.group_name
            count = 0
            cards = set_offset(func=api.get_set_data, group_id=group.group_id)
            if cards is not None:

                for card in cards:
                    product_id = card['productId']
                    name = card['name']

                    image = get_image(product_id)

                    if image == '':
                        image = card['imageUrl']
                    else:
                        pass

                    if MTG.objects.filter(product_id=product_id).exists() is False:

                        preorder = True if group.release_date > datetime.now(timezone('EST')) else False

                        if category == "Magic the Gathering":

                            upload_list.append(
                                MTG(
                                    name=name,
                                    expansion=expansion,
                                    language='English',
                                    image_url=image,
                                    product_id=product_id,
                                    preorder=preorder,
                                )
                            )

                        elif category == "Card Sleeves":
                            upload_list.append(
                                MTG(
                                    name=name,
                                    expansion=expansion,
                                    language='English',
                                    image_url=image,
                                    product_id=product_id,
                                    layout="supplies",
                                    card_type="Card Sleeves",
                                )
                            )

                        count += 1

            # group_add_input = input('Changed Group Added to True?\n')
            # if group_add_input.lower() == 'yes':

            if len(upload_list) > 0:
                MTG.objects.bulk_create(upload_list)
                if group.release_date <= datetime.now(timezone('EST')):
                    group.added = True
                    group.save()

        # Add detailed card attributes
        add_info()


