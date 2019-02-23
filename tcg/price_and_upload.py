from .price_alogrithm import *
from engine.tcgplayer_api import TcgPlayerApi
from my_customs.decorators import report_error
from django.core.mail import send_mail
from orders.models import Inventory
from datetime import date
from django.core.exceptions import ObjectDoesNotExist

api = TcgPlayerApi()


def task_management(obj):
    data = obj.objects.filter(upload_status=False)
    if len(data) <= 100:
        sku_list = [i.sku for i in data]
        upload_sku(sku_list, data)

    else:
        start = 0
        stop = 100
        while True:
            sku_list = [i.sku for i in data[start:stop]]
            upload_sku(sku_list, data)

            if stop == len(data):
                break
            else:
                start = stop
                stop += 100
                if stop > len(data):
                    stop = len(data)


@report_error
def upload_sku(sku_list, data):
    print(sku_list)
    errors_list = []
    inventory = Inventory.objects
    api_market_data = api.market_prices_by_sku(sku_list)

    if api_market_data['success']:
        price_data = api_market_data['results']

        for each in price_data:
            sku = str(each['skuId'])
            market_price = each['marketPrice']
            low_price = each['lowPrice']
            direct_low_price = each['directLowPrice']
            # lowest_listing = each['lowestListingPrice']

            # Get current quantity of sku on TCGplayer Inventory
            api_inventory_quantity = api.get_sku_quantity(sku)
            if api_inventory_quantity['errors']:
                print(api_inventory_quantity['errors'])

            if api_inventory_quantity['success'] or api_inventory_quantity['errors'] == ['No Sku(s) were found for SkuId (315800).']:
                try:
                    current_quantity = api.get_sku_quantity(sku)['results'][0]['quantity']
                except IndexError:
                    current_quantity = 0
                # Query for all matching sku (Instances of Multiple cards with a upload_status of False)
                all_skus = data.filter(sku=sku)

                # Sum of all sku upload quantities to be uploaded to inventory
                quantity = sum([i.upload_quantity for i in all_skus])

                # quantity must be added to current inventory total, and new quantity for sku is set wrather than incremented
                upload_quantity = quantity + current_quantity

                # Use pricing tool to adjust upload price
                upload_price = sku_price_algorithm(market_price, direct=direct_low_price, low=low_price)

                # Attempt to upload sku
                uploaded_card = api.upload(sku, price='a', quantity=upload_quantity)

                # Report any errors in uploading
                if uploaded_card['errors']:
                    errors_list.append(uploaded_card['errors'][0] + f' for sku: {sku}' + '\n')
                    print(uploaded_card['errors'])

                if True:
                    # Update item in Upload model to reflect a successful upload
                    for upload in all_skus:
                        upload.upload_status = True
                        upload.upload_date = date.today()
                        upload.upload_price = upload_price
                        upload.save()

                    # All changes made are reflected in the online inventory
                    # If sku is not in inventory, create it
                    try:
                        online_stock = inventory.get(sku=sku)
                        online_stock.quantity = upload_quantity
                        online_stock.last_upload_date = date.today()
                        online_stock.last_upload_quantity = quantity
                        online_stock.save()

                    except ObjectDoesNotExist:
                        new = Inventory(
                            sku=sku,
                            quantity=upload_quantity,
                            expansion=all_skus[0].group_name,
                            name=all_skus[0].name,
                            condition=all_skus[0].condition,
                            printing=all_skus[0].printing,
                            language=all_skus[0].language,
                            category=all_skus[0].category,
                            rarity='unknown',
                            price=upload_price,
                            last_upload_date=date.today(),
                            last_upload_quantity=quantity,
                            last_sold_date=date(1800, 1, 1),
                            last_sold_quantity=0,
                            last_sold_price=0,
                            total_quantity_sold=0,
                        )
                        new.save()

                    print('Yass')

    else:
        print(api_market_data['errors'])

    if errors_list:
        subject = "Errors uploading card(S)"
        message = f"There were error uploading the following list of cards\n{','.join(errors_list)}"
        mail_from = 'tcgfirst'
        mail_to = ['jermol.jupiter@gmai.com', ]
        send_mail(subject, message, mail_from, mail_to)



