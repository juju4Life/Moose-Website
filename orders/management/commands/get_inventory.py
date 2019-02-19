from django.core.management.base import BaseCommand
from engine.tcgplayer_api import TcgPlayerApi
from django.core.mail import send_mail
from orders.models import Inventory, NewOrders
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

        # get database query for current inventory copy
        inventory = Inventory.objects.all()

        # get database query for all orders with yesterday's date
        yesterday = date.today()  # - timedelta(1)
        new_orders = NewOrders.objects.filter(order_date=yesterday)

        # Contains difference in quantities for Inventory vs api call for
        # updated inventory for each sku
        diff_dict = {}

        # check if there are orders recorded for yesterday. If not, something may be wrong. send notification.
        if new_orders:
            # Loop through categories and request full inventory listings for each category
            for cat in category_ids:
                api_check = api.get_inventory(str(cat))
                if not api_check['errors']:
                    cards = api_check['results']

                    for card in cards:
                        sku = card['skuId']
                        api_check_2 = api.get_sku_quantity(str(sku))

                        if not api_check_2['errors']:
                            quantity = api.get_sku_quantity(str(sku))['results'][0]['quantity']

                            # Create dictionary containing all inventory data
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
                        else:
                            send_mail('error for get_inventory api call ', f"{api_check_2['errors']}", 'TCGfirst', 'jermol.jupiter@gmail.com')
                else:
                    send_mail('error for get_sku_quantity api call ', f"{api_check['errors']}", 'TCGfirst', 'jermol.jupiter@gmail.com')

            if diff_dict:
                for key, value in diff_dict.items():
                    quantity = value['quantity']
                    sku = key

                    # Search current database for exact sku. If it doesn't exist, create object with acquired info
                    try:
                        db_data = inventory.get(sku=sku)

                    except ObjectDoesNotExist:
                        '''new_item = Inventory(
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
                        new_item.save()'''
                        db_data = inventory.get(sku=sku)

                    # Compare dict's record of sku quantity with current db's matching sku quantity value. Store the result
                    compare_qty = abs(db_data.quantity - quantity)

                    # Change current db quantity value to the new one and add total quantity to the total items sold field
                    db_data.quantity = quantity
                    db_data.total_quantity_sold += quantity

                    # Get quantity sum of all orders with give sku from yesterday's orders
                    order_items = new_orders.filter(sku=sku)
                    sum_orders = sum(order_items.values_list('quantity', flat=True))

                    if sum_orders:
                        # Update db object with recently sold information
                        db_data.last_sold_date = yesterday
                        db_data.last_sold_quantity = sum_orders
                        db_data.last_sold_price = sum(order_items.values_list('price', flat=True)) / sum_orders

                    # Subtract the sum of ordered items from the new quantity value
                    # If that number is negative. That many cards have been uploaded. Update current db's last upload date for field
                    # If that number is positive. That many items have been removed from the inventory
                    # zero indicates no change in inventory. No uploads or removals
                    result = compare_qty - sum_orders

                    if result < 0:
                        # Update objects last upload date and quantity if result is negative (that many cards uploaded)
                        db_data.last_upload_date = yesterday
                        db_data.last_upload_quantity = abs(result)

                    elif result > 0:
                        # If result is greater than 0, these items should have been removed from the inventory. send info to message box to check for accuracy
                        message.append(f"{sku} - {result} {value['printing']} {value['condition']} - {value['language']} - {value['name']} - {value['expansion']}\n ")

                    # db_data.save()
            else:
                send_mail('diff dict is empty for get_inventory.py function', "Unknown error. Possibly get_inventory api call returned empy list", 'TCGfirst',
                          'jermol.jupiter@gmail.com')
        else:
            # Send notification about missing no present orders
            send_mail(f'No orders for {yesterday}', f'No orders for {yesterday}. Please investigate', 'TCGfirst', 'jermol.jupiter@gmail.com')

        if message:
            message = ','.join(message)
            send_mail('Items should have been removed from the inventory', f'The following list of items should have been removed from the inventory\n{message}',
                      'TCGfirst', 'jermol.jupiter@gmail.com')















