from django.core.management.base import BaseCommand
from engine.tcgplayer_api import TcgPlayerApi
from django.core.mail import send_mail
from orders.models import Inventory
from my_customs.decorators import report_error
from datetime import date, timedelta
from django.core.exceptions import ObjectDoesNotExist


api = TcgPlayerApi()


class Command(BaseCommand):
    @report_error
    def handle(self, **options):

        # message list for alert purposes
        message = []

        # Various categoies to request information from the TCGplayer API
        category_ids = [1, 2, 3, 31, 56, 16, 32, 27, 17, 29, 35, 14, 22]

        # check if there are orders recorded for yesterday. If not, something may be wrong. send notification.
        for i, cat in enumerate(category_ids):
            api_check = api.get_inventory(str(cat))
            if not api_check['errors']:
                cards = api_check['results']
                for card in cards:
                    sku = card['skuId']
                    api_check_2 = api.get_sku_quantity(str(sku))

                    if not api_check_2['errors']:
                        quantity = api.get_sku_quantity(str(sku))['results'][0]['quantity']
                        new_item = Inventory(
                            sku=sku,
                            quantity=quantity,
                            name=card['name'],
                            category=card['category'],
                            expansion=card['expansion'],
                            condition=card['condition'],
                            rarity=card['rarity'],
                            language=card['language'],
                            price=card['price'],
                            printing=card['printing'],
                            last_upload_date='',
                        )
                        new_item.save()
                        print(i)















