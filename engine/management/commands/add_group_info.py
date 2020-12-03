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
from tcg.tcg_functions import categorize_product_layout

api = TcgPlayerApi('moose')
manifest = Manifest()


class Command(BaseCommand):
    # @report_error
    def handle(self, *args, **options):

        groups = GroupName.objects.filter(category="Magic the Gathering", added=False)

        for group in groups:
            release_date = group.release_date
            category = group.category
            upload_list = list()
            expansion = group.group_name
            count = 0

            # API call is required paged requests. We call this function that makes all of the separate requests and combines the data.
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

                        # determine if item is a pre-release product on creation
                        preorder = True if group.release_date > datetime.now(timezone('EST')) else False

                        if category == "Magic the Gathering":

                            # Determine category of product (Sealed, Supplies, Singles etc.)
                            layout = categorize_product_layout(name)

                            upload_list.append(
                                MTG(
                                    name=name,
                                    expansion=expansion,
                                    language='English',
                                    image_url=image,
                                    product_id=product_id,
                                    preorder=preorder,
                                    release_date=release_date,
                                    layout=layout,
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

            if len(upload_list) > 0:
                MTG.objects.bulk_create(upload_list)
                if group.release_date <= datetime.now(timezone('EST')):
                    group.added = True
                    group.save()

        # Add detailed card attributes
        add_info()

