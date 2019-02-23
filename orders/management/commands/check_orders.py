from django.core.management.base import BaseCommand
from engine.tcgplayer_api import TcgPlayerApi
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from orders.models import Orders, GroupName
from my_customs.decorators import report_error
from engine.tcg_manifest import Manifest
from orders.models import NewOrders, Inventory
from datetime import date
from collections import Counter

api = TcgPlayerApi()
M = Manifest()


class Command(BaseCommand):
    def handle(self, **options):
        group = GroupName.objects
        inventory = Inventory.objects
        # Check for new group ids
        checks = Counter()
        errors = []
        to_upload = []
        recent_orders = api.get_recent_orders(offset=0)['results'][0:10]
        if recent_orders:
            for recent in recent_orders:
                if NewOrders.objects.filter(order_number=recent).exists() is False:
                    to_upload.append(recent)

        order_details = api.get_order_details(to_upload)['results']
        for o in order_details:
            order_number = o['orderNumber']
            print(order_number)
            order_date = o['orderedOn']
            cards = api.get_order_items(order_number)['results']
            card_data = {}
            for card in cards:
                sku = card['skuId']
                quantity = card['quantity']
                card_data[sku] = {
                    'skuId': sku,
                    'quantity': quantity,
                    'price': card['price'],
                }

            sku_list = [str(i) for i in card_data]
            product_info = api.card_info_by_sku(','.join(sku_list))['results']
            for p in product_info:
                q = card_data[p['skuId']]['quantity']
                price = card_data[p['skuId']]['price']
                sku = p['skuId']
                product_id = p['productId']
                language = M.language(p['languageId'])
                condition = M.condition(p['conditionId'])
                printing = M.printing(p['printingId'])
                item_details = api.get_card_info(str(product_id))['results']
                for item in item_details:
                    name = item['name']
                    category = M.game(item['categoryId'])
                    expansion = group.get(group_id=str(item['groupId']))
                    # print(f'{category}, {expansion}, {name}, {condition}, {language}, {printing}, {q}, {price}')
                    print(f'{category}, {name}, {q}, {sku}')
                    checks[sku] += q
                    try:
                        card = inventory.get(sku=sku)

                    except ObjectDoesNotExist:
                        pass
                    # Create reference for each ordered card
                    '''items = NewOrders(
                        check_order_date=date.today(),
                        order_number=order_number,
                        order_date=order_date,
                        sku=sku,
                        name=name,
                        expansion=expansion,
                        category=category,
                        condition=condition,
                        printing=printing,
                        language=language,
                        price=price,
                        quantity=q,
                    )
                    items.save()'''
        print(checks)





