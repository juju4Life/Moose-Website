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
        orders = Orders.objects.values_list('order_number', flat=True)
        group = GroupName.Objects
        offset = 0
        while offset < 300:
            recent_orders = api.get_recent_orders(offset=offset)['results']
            if recent_orders:
                to_upload = []
                for recent in recent_orders:
                    if recent not in orders:
                        to_upload.append(recent)

                if to_upload:
                    order_details = api.get_order_details(to_upload)['results']
                    for o in order_details:
                        order_number = o['orderNumber']
                        order_channel = M.order_channel_type(o['orderChannelTypeId'])
                        order_status = M.order_status_type(o['orderStatusTypeId'])
                        order_delivery = M.order_delivery_types(o['orderDeliveryTypeId'])
                        is_direct = o['isDirect']
                        international = o['isInternational']
                        presale = M.order_presale_status_type(o['presaleStatusTypeId'])
                        order_date = o['orderedOn'][0:10]
                        modified = o['modifiedOn'][0:10]
                        token = o['customer']['token']
                        first_name = o['customer']['firstName']
                        last_name = o['customer']['lastName']
                        email = o['customer']['email']
                        shipping_first_name = o['customer']['shippingAddress']['firstName']
                        shipping_last_name = o['customer']['shippingAddress']['lastName']
                        address_1 = o['customer']['shippingAddress']['address1']
                        address_2 = o['customer']['shippingAddress']['address2']
                        city = o['customer']['shippingAddress']['city']
                        state = o['customer']['shippingAddress']['state']
                        postal_code = o['customer']['shippingAddress']['postalCode']
                        country = o['customer']['shippingAddress']['country']
                        product_value = o['orderValue']['product']
                        shipping = o['orderValue']['shipping']
                        tax = o['orderValue']['tax']
                        gross = o['orderValue']['gross']
                        fees = o['orderValue']['fees']
                        net = o['orderValue']['net']
                        category = 'Unknown'
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

                            for p in product_info:
                                print(p)
                                q = card_data[p['skuId']]['quantity']
                                price = card_data[p['skuId']]['price']
                                sku = p['skuId']
                                product_id = p['productId']
                                language = M.language(p['languageId'])
                                condition = M.condition(p['conditionId'])
                                # printing = M.printing(p['printingId'])
                                item_details = api.get_card_info(str(product_id))['results']
                                for item in item_details:
                                    name = item['name']
                                    category = M.game(item['categoryId'])
                                    expansion = M.group(item['groupId'])
                                    conc = f"{category}<>{q}<>{name}<>{expansion}<>{language}<>{condition}<>{printing}<>{price}<>{sku}"
                                    ordered_items.append(conc)
                            total -= 100

                        db = Orders.objects
                        db.create(
                            order_number=order_number,
                            order_channel_type=order_channel,
                            order_status_type=order_status,
                            order_delivery_type=order_delivery,
                            is_direct=is_direct,
                            international=international,


                        )
            else:
                subject = "Api for orders returned empty list"

            offset += 100




