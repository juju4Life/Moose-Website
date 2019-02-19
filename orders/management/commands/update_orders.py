from django.core.management.base import BaseCommand
from engine.tcgplayer_api import TcgPlayerApi
from django.core.mail import send_mail
from orders.models import Orders, GroupName
from my_customs.decorators import report_error
from engine.tcg_manifest import Manifest
from orders.models import NewOrders
from datetime import date

api = TcgPlayerApi()
M = Manifest()


class Command(BaseCommand):
    @report_error
    def handle(self, **options):

        # Check for new group ids

        order_count = 0
        errors = []

        group = GroupName.objects
        offset = 0
        while offset < 2000:
            print(offset)
            # orders = Orders.objects.values_list('order_number', flat=True)
            recent_orders = api.get_recent_orders(offset=offset)['results']
            if recent_orders:
                to_upload = []
                for recent in recent_orders:
                    if Orders.objects.filter(order_number=recent).exists() is False:
                        to_upload.append(recent)

                print(f"Number of orders to upload {len(to_upload)}")
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
                        if first_name is None:
                            first_name = ''
                        last_name = o['customer']['lastName']
                        if last_name is None:
                            last_name = ''
                        email = o['customer']['email']
                        shipping_first_name = o['customer']['shippingAddress']['firstName']
                        shipping_last_name = o['customer']['shippingAddress']['lastName']
                        address_1 = o['customer']['shippingAddress']['address1']
                        address_2 = o['customer']['shippingAddress']['address2']
                        if address_2 is None:
                            address_2 = ''
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
                                    conc = f"{category}<>{q}<>{name}<>{expansion}<>{language}<>{condition}<>{printing}<>{price}<>{sku}"
                                    ordered_items.append(conc)

                                    # Create reference for each ordered card
                                    items = NewOrders(
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
                                    items.save()
                            total -= 100
                        db = Orders(
                            category=category,
                            order_number=order_number,
                            order_channel_type=order_channel,
                            order_status_type=order_status,
                            order_delivery_type=order_delivery,
                            is_direct=is_direct,
                            international=international,
                            presale_status_type=presale,
                            order_date=order_date,
                            modified_on_date=modified,
                            customer_token=token,
                            first_name=first_name,
                            last_name=last_name,
                            email=email,
                            shipping_first_name=shipping_first_name,
                            shipping_last_name=shipping_last_name,
                            address_1=address_1,
                            address_2=address_2,
                            city=city,
                            state=state,
                            postal_code=postal_code,
                            country=country,
                            product_value=product_value,
                            shipping=shipping,
                            tax=tax,
                            gross=gross,
                            fees=fees,
                            net=net,
                            ordered_items='\n'.join(ordered_items),

                        )
                        try:
                            db.save()
                        except Exception as e:
                            print(e)
                            errors.append(order_number)
                        order_count += 1

            else:
                subject = "Api for orders returned empty list"
                errors = api.get_recent_orders(offset=offset)['errors']
                message = f"Api returned empty list. May be a problem with Credentials. API call for errors: {errors}"
                to = ('jermol.jupiter@gmail.com',)
                email_from = 'tcgfirst.com'
                send_mail(subject, message, email_from, to)
            print(f"{offset}-{offset+100} of recent orders")
            print(f"Total orders added: {order_count}")
            offset += 100

        print(errors)





