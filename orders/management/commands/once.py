from django.core.management.base import BaseCommand
from engine.tcgplayer_api import TcgPlayerApi
from django.core.mail import send_mail
from orders.models import Inventory
from my_customs.decorators import report_error
from datetime import date, timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError


api = TcgPlayerApi()


class Command(BaseCommand):
    def handle(self, **options):

        # message list for alert purposes
        message = []

        # Various categoies to request information from the TCGplayer API
        category_ids = [2, 3, 31, 56, 16, 32, 27, 17, 29, 35, 14, 22]

        # check if there are orders recorded for yesterday. If not, something may be wrong. send notification.
        for cat in category_ids:
            api_check = api.get_inventory(str(cat))
            if not api_check['errors']:
                cards = api_check['results']
                for i, card in enumerate(cards):
                    sku = card['skuId']
                    if Inventory.objects.filter(sku=sku).exists() is False:
                        api_check_2 = api.get_sku_quantity(str(sku))
                        if not api_check_2['errors']:
                            quantity = api.get_sku_quantity(str(sku))['results'][0]['quantity']
                            rarity = card['rarityName']
                            if rarity is None:
                                rarity = ''
                            new_item = Inventory(
                                sku=sku,
                                quantity=quantity,
                                name=card['productName'],
                                category=card['categoryName'],
                                expansion=card['groupName'],
                                condition=card['conditionName'],
                                rarity=rarity,
                                language=card['languageName'],
                                price=card['currentPrice'],
                                printing=card['printingName'],
                                last_upload_date=date.today(),
                                last_sold_date=date.today(),
                            )
                            new_item.save()
                            print(i)















