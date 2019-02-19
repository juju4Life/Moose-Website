from django.core.management.base import BaseCommand
from engine.tcgplayer_api import TcgPlayerApi
from django.core.mail import send_mail
from orders.models import Orders, Inventory
from my_customs.decorators import report_error
from engine.tcg_manifest import Manifest
from datetime import date
from django.core.exceptions import ObjectDoesNotExist


api = TcgPlayerApi()
M = Manifest()


class Command(BaseCommand):
    @report_error
    def handle(self, **options):
        category_ids = [1, 2, 3, 31, 56, 16, 32, 27, 17, 29, 35, 14, 22]
        inventory = Inventory.objects.all()

        # Contains difference in quantities for Inventory vs api call for
        # updated inventory for each sku
        diff_dict = {}

        for cat in category_ids:
            cards = api.get_inventory(str(cat))['results']

            for card in cards:
                sku = card['skuId']
                quantity = api.get_sku_quantity(str(sku))['results'][0]['quantity']
                diff_dict[sku] = {
                    'quantity': quantity,
                    'name': card['productName'],
                    'category': card['categoryName'],
                    'expansion': card['groupName'],
                    'condition': card['conditionName'],
                    'rarity': card['rarityName'],
                    'language': card['languageName'],
                    'price': card['currentPrice'],
                    'printing': card['printingName'],
                    'upload_date': date.today(),
                    'last_upload_quantity': quantity,
                }

        for key, value in diff_dict.items():
            quantity = value['quantity']
            sku = key

            try:
                db_quantity = inventory.get(sku=sku).quantity
            except ObjectDoesNotExist:
                db_quantity = []
                new_item = Inventory(
                    sku=key,
                    quantity=quantity,
                    name=value['name'],
                    category=value['category'],
                    expansion=value['expansion'],
                    condition=value['condition'],
                    rarity=value['rarity'],
                    language=value['language'],
                    price=value['price'],
                    printing=value['printing'],
                    last_upload_date=value['upload_date'],
                    last_upload_quantity=value['last_upload_quantity'],
                )

                new_item.save()

            if db_quantity:
                pass








