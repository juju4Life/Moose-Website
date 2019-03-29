from __future__ import absolute_import, unicode_literals
from celery import shared_task
from tcg.price_alogrithm import *
from engine.tcgplayer_api import TcgPlayerApi
from engine.models import MTG, Yugioh, Pokemon, Upload
from my_customs.decorators import report_error
from django.core.mail import send_mail
from orders.models import Inventory
from datetime import date
from django.core.exceptions import ObjectDoesNotExist
from scryfall_api import get_image

api = TcgPlayerApi()


@shared_task(name='orders.tasks.task_upload')
def task_management():
    data = Upload.objects.filter(upload_status=False)

    # All cards should be from one category
    # APi for sku productId, which gets us the category ID for the category
    sku = data[0].sku
    product_id = api.card_info_by_sku(sku)['results'][0]['productId']
    cat_id = api.get_card_info(str(product_id))['results'][0]['categoryId']

    # Max of 100 skus for prices in a single api call. Request Info for entire list if <= 100
    if len(data) <= 100:

        sku_list = list({i.sku for i in data})
        upload_sku(sku_list, data, cat_id)

    # if list > 100, While loop run function for up to 100 skus for each iteration
    else:
        start = 0
        stop = 100
        while True:
            sku_list = [i.sku for i in data[start:stop]]
            upload_sku(sku_list, data, cat_id)

            if stop == len(data):
                break
            else:
                start = stop
                stop += 100
                if stop > len(data):
                    stop = len(data)


@report_error
def upload_sku(sku_list, data, cat_id):
    errors_list = []
    inventory = Inventory.objects
    mtg = MTG.objects
    ygo = Yugioh.objects
    pokemon = Pokemon.objects

    # map category_id of sku to correct database.
    category_map = {
        1: mtg,
        2: ygo,
        3: pokemon,
    }

    cat = category_map[cat_id]

    # List of Category ids. Used to keep track of check databses when trying to find correct db for sku
    cat_ids_list = [cat_id]

    # Get market data for list of sku
    api_market_data = api.market_prices_by_sku(sku_list)

    if api_market_data['success']:
        print('is success')
        price_data = api_market_data['results']

        for each in price_data:
            sku = str(each['skuId'])
            market_price = each['marketPrice']
            low_price = each['lowPrice']
            direct_low_price = each['directLowPrice']

            # Get current quantity of sku from TCGplayer Inventory
            api_inventory_quantity = api.get_sku_quantity(sku)
            if api_inventory_quantity['errors']:
                print('Inventory errors')

            if api_inventory_quantity['success'] or api_inventory_quantity['errors'] == [f'No Sku(s) were found for SkuId ({sku}).']:

                try:
                    current_quantity = api.get_sku_quantity(sku)['results'][0]['quantity']
                except IndexError:
                    current_quantity = 0

                # Query for all matching sku (Instances of Multiple cards with a upload_status of False)
                all_skus = data.filter(sku=sku)

                # Card details for give category
                # If get sku fails, iterate though each category until the correct db is found
                # Empty list if sku is not found in any database
                sku_card_info = []
                try:
                    print('getting info')
                    sku_card_info = cat.get(sku=sku)

                except ObjectDoesNotExist:
                    try:
                        if 2 not in cat_ids_list:
                            cat = category_map[2]
                            sku_card_info = cat.get(sku=sku)
                    except ObjectDoesNotExist:
                        cat_ids_list.append(2)
                        try:
                            if 3 not in cat_ids_list:
                                cat = category_map[3]
                                sku_card_info = cat.get(sku=sku)
                        except ObjectDoesNotExist:
                            cat_ids_list.append(3)
                            try:
                                if 1 not in cat_ids_list:
                                    cat = category_map[1]
                                    sku_card_info = cat.get(sku=sku)
                            except ObjectDoesNotExist:
                                pass

                if sku_card_info:
                    'There is sku info for this card'
                    condition = sku_card_info.condition

                    # Sum of all sku upload quantities to be uploaded to inventory
                    quantity = sum([i.upload_quantity for i in all_skus])
                    printing = sku_card_info.foil
                    category = sku_card_info.product_line
                    name = sku_card_info.product_name
                    expansion = sku_card_info.set_name
                    language = sku_card_info.language

                    # quantity must be added to current inventory total, and new quantity for sku is set wrather than incremented
                    upload_quantity = quantity + current_quantity
                    print('About to price algo')
                    # Use pricing tool to adjust upload price
                    upload_price = sku_price_algorithm(
                        category=category, printing=printing, condition=condition, sku=sku, market=market_price, direct=direct_low_price, low=low_price,
                        language=language, expansion=expansion,
                    )
                    print('Now uploding after pricecheck')
                    # Attempt to upload sku
                    uploaded_card = api.upload(sku, price=upload_price, quantity=upload_quantity)
                    print('Card should be uploaded')
                    # Report any errors in uploading
                    if uploaded_card['errors']:
                        errors_list.append(uploaded_card['errors'][0] + f' for sku: {sku}' + '\n')
                        print(uploaded_card['errors'])

                    elif uploaded_card['success']:
                        # Update item in Upload model to reflect a successful upload
                        # Query relevant database for details on sku

                        for upload in all_skus:
                            upload.upload_status = True
                            upload.upload_date = date.today()
                            upload.upload_price = upload_price
                            upload.category = category
                            upload.name = name
                            upload.group_name = expansion
                            upload.condition = condition
                            upload.printing = printing
                            upload.language = language
                            upload.save()

                        # All changes made are reflected in the online inventory
                        # If sku is not in inventory, create it
                        try:
                            online_stock = inventory.get(sku=sku)
                            online_stock.quantity = upload_quantity
                            online_stock.price = upload_price
                            online_stock.last_upload_date = date.today()
                            online_stock.last_upload_quantity = quantity
                            online_stock.save()

                        except ObjectDoesNotExist:
                            product_id = api.card_info_by_sku(sku)['results'][0]['productId']
                            print(product_id)
                            image_url = get_image(product_id)
                            print(image_url)
                            new = Inventory(
                                sku=sku,
                                quantity=upload_quantity,
                                expansion=expansion,
                                name=name,
                                condition=condition,
                                printing=printing,
                                language=language,
                                category=category,
                                rarity='unknown',
                                price=upload_price,
                                last_upload_date=date.today(),
                                last_upload_quantity=quantity,
                                last_sold_date=date(1111, 1, 1),
                                last_sold_quantity=0,
                                last_sold_price=0,
                                total_quantity_sold=0,
                                ebay=False,
                                amazon=False,
                                product_id=product_id,
                                image_url=image_url,
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


