from django.core.management.base import BaseCommand
from engine.tcgplayer_api import TcgPlayerApi
from django.core.mail import send_mail
from orders.models import Orders, GroupName
from my_customs.decorators import report_error
from engine.tcg_manifest import Manifest

api = TcgPlayerApi()
M = Manifest()


class Command(BaseCommand):
    @report_error
    def handle(self, **options):
        orders = Orders.objects.all()
        group = GroupName.objects
        count = 0
        for order in orders:
            if order.ordered_items == '':
                category = ''
                order_number = order.order_number
                ordered_items = []
                total = api.get_order_items(order_number)['totalItems']
                while total > 0:
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
                    print(product_info)
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
                            expansion = group.get(group_id=item['groupId']).group_name
                            conc = f"{category}<>{q}<>{name}<>{expansion}<>{language}<>{condition}<>{printing}<>{price}<>{sku}"
                            ordered_items.append(conc)
                    total -= 100
                order.category = category
                order.ordered_items = '\n'.join(ordered_items)
                order.save()
                count += 1
                print(count)



