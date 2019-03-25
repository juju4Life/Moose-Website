from django.core.management.base import BaseCommand
from engine.tcgplayer_api import TcgPlayerApi
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from orders.models import Orders, GroupName
from my_customs.decorators import report_error
from engine.tcg_manifest import Manifest
from orders.models import NewOrders, Inventory
from datetime import date
from decouple import config
from scryfall_api import get_image

api = TcgPlayerApi()
M = Manifest()


class Command(BaseCommand):
    @report_error
    def handle(self, **options):

        # convert group ID to groupname
        group = GroupName.objects

        # Inventory of currecntly listed items
        inventory = Inventory.objects

        # Check for new group ids
        errors = []
        to_upload = []

        # Search the last 50 orders for any that have not been recorded to the database
        recent_orders = api.get_recent_orders(offset=0)['results']
        if recent_orders:
            for recent in recent_orders:
                if NewOrders.objects.filter(order_number=recent).exists() is False:
                    to_upload.append(recent)
        else:
            subject = "List with 0 results returned for api.get_recent_orders"
            message = "List with 0 results returned for api.get_recent_orders"
            to = [config('my_email')]
            from_ = 'tcgfirst'
            send_mail(subject, message, from_, to)
        if to_upload:
            print(len(to_upload))
            # Get order details from order_numbers
            api_order_details = api.get_order_details(to_upload)
            if api_order_details['errors']:
                errors.append(api_order_details['errors'][0] + ' api.get_order_details')

            else:
                # Create al order_details variables
                order_details = api_order_details['results']
                for o in order_details:
                    order_number = o['orderNumber']
                    order_date = o['orderedOn'][0:10]
                    is_direct = o['isDirect']
                    shipping_first_name = o['customer']['shippingAddress']['firstName']
                    shipping_last_name = o['customer']['shippingAddress']['lastName']
                    customer_name = f"{shipping_first_name} {shipping_last_name}"
                    order_delivery = M.order_delivery_types(o['orderDeliveryTypeId'])

                    cards = api.get_order_items(order_number)['results']

                    # Create dictionary of sku, qty, and price. This information is needed to query for product-specific information later
                    card_data = {}
                    for card in cards:
                        sku = card['skuId']
                        quantity = card['quantity']
                        card_data[sku] = {
                            'skuId': sku,
                            'quantity': quantity,
                            'price': card['price'],
                        }

                    # Create list of skus to api call for product_info. Dict comes from last step
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

                        # Use sku from product info to api call for me related information in each sku
                        item_details = api.get_card_info(str(product_id))['results']
                        for item in item_details:
                            name = item['name']
                            category = M.game(item['categoryId'])
                            expansion = group.get(group_id=str(item['groupId']))

                            # Update Inventory db with recently sold information
                            try:
                                card = inventory.get(sku=sku)
                                card.quantity -= q
                                card.last_sold_date = order_date
                                card.last_sold_quantity = q
                                card.last_sold_price = price
                                card.total_quantity_sold += q
                                card.save()

                            # If product doesn't exisit in inventory for some reason, create and populate fields
                            except ObjectDoesNotExist:
                                image_url = get_image(product_id)
                                new_item = Inventory(
                                    sku=sku,
                                    quantity=0,
                                    expansion=expansion,
                                    name=name,
                                    condition=condition,
                                    printing=printing,
                                    language=language,
                                    category=category,
                                    rarity='Unknown',
                                    price=price,
                                    last_upload_date=date(1111, 1, 1),
                                    last_upload_quantity=0,
                                    last_sold_date=order_date,
                                    last_sold_quantity=q,
                                    last_sold_price=price,
                                    total_quantity_sold=q,
                                    ebay=False,
                                    amazon=False,
                                    product_id=product_id,
                                    image_url=image_url,

                                )
                                new_item.save()

                            # Create reference for each ordered card
                            items = NewOrders(
                                is_direct=is_direct,
                                customer_name=customer_name,
                                order_delivery_type=order_delivery,
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

                    if is_direct is False:
                        pass

        if errors:
            subject = "List of errors for function, check_orders"
            message = f"List of errors during execution of function, check_orders\n{errors}"
            to = [config('my_email')]
            from_ = 'tcgfirst'
            send_mail(subject, message, from_, to)




