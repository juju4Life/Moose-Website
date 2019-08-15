from __future__ import absolute_import, unicode_literals
from celery import shared_task
import traceback
from tcg.price_alogrithm import *
from engine.tcgplayer_api import TcgPlayerApi
from engine.models import MTG, Yugioh, Pokemon, Upload
from my_customs.decorators import report_error
from django.core.mail import send_mail
from orders.models import Inventory
from datetime import date
from django.core.exceptions import ObjectDoesNotExist
from scryfall_api import get_image
import random
from my_customs.functions import request_pages_data
from tcg.tcg_functions import moose_price_algorithm, get_product_seller_info
from time import time

api = TcgPlayerApi('moose')

'''
Url function generates dynamic url based on differences in card attributes. Random number is generated to provide the 13-digit request number that Tcgplayer 
expects with each request. Different urls are required for Foil and Normal versions of cards.
'''


def url(product_id, foil, condition, page=1):
    random_string = str(random.randint(1000000000000, 9999999999999))
    condition = condition.replace(" ", "")
    url_path = {
        'Normal': f'https://shop.tcgplayer.com/productcatalog/product/changepricetablepage?filterName=Condition&filterValue={condition}&productId={product_id}&'
        f'gameName=magic&page={page}&X-Requested-With=XMLHttpRequest&_={random_string}',


        'Foil': f'https://shop.tcgplayer.com/productcatalog/product/changepricetablepage?filterName=Printing&filterValue=Foil&productId={product_id}&'
        f'gameName=magic&page={page}&X-Requested-With=XMLHttpRequest&_={random_string}',

        }

    return url_path[foil]


@shared_task(name='orders.tasks.update_moose_tcg')
def update_moose_tcg():
    start_time = time()
    # Entire Moose Loot Listed inventory
    listed_cards = api.get_category_skus('magic')
    if listed_cards['success'] is True:
        print(f"Updating {listed_cards['totalItems']} for Moose Inventory")
        for index, card in enumerate(listed_cards['results']):
            try:
                condition = card['conditionName']
                printing = card['printingName']
                print(index)
                if condition != 'Unopened':
                    current_price = card['currentPrice']
                    low = card['lowPrice']
                    if current_price != low:
                        sku = card['skuId']
                        product_id = card['productId']
                        name = card['productName']
                        expansion = card['groupName']
                        market = card['marketPrice']
                        language = card['languageName']

                        '''    
                        If the card is not English it will be priced at the low price minus one cent.

                        For each card in the MooseLoot inventory we will make a request to the tcgplayer page containing all seller data for a given 
                        product. 
                        We request and scan pages (10 results per page) until we find 2 listings with sellers that have 10,000 sales or more. We break the while loop 
                        once we have found those two listings and move on to the next card. In the case where only one or zero listings are found, 
                        we break the loop and use one price to match against or default to the market price.      
                        '''

                        if language != 'English' and printing != 'Foil':
                            # catch instances where there is no low price
                            try:
                                updated_price = low - .01
                            except TypeError:
                                updated_price = None

                            if updated_price is not None:
                                print('Foreign')
                                api.update_sku_price(sku_id=sku, price=updated_price, _json=True)

                        elif language == 'English':

                            next_page = True
                            page = 1
                            seller_data_list = []

                            while next_page is True:

                                request_path = url(product_id=product_id, condition=condition, foil=printing, page=page)

                                data, page_source = request_pages_data(
                                    url=request_path,
                                    tag='div',
                                    attribute='class',
                                    attribute_value='product-listing ',
                                )

                                # Check if there are products in the request. If not that indicates no more listings and thus we break the loop
                                if not data:
                                    break

                                # loop over each item on the page and get Seller Info
                                for d in data:
                                    seller_condition = d.find('div', {'class': 'product-listing__condition'}).text.strip()
                                    seller_name = d.find('a', {'class': 'seller__name'}).text.strip()

                                    if seller_name != 'MTGFirst' and seller_name != 'Moose Loot' and condition == seller_condition:

                                        price, total_price, seller_total_sales = get_product_seller_info(d)

                                        price_dict = {
                                            'price': total_price,
                                            'gold': True if seller_total_sales >= 10000 else False
                                        }
                                        seller_data_list.append(price_dict)
                                        if len(seller_data_list) == 5:
                                            next_page = False
                                            break

                                page += 1

                            '''
                            We will check the number of other seller listings.
                            If there were zero listings found we simply make the updated price the market price.

                            If just one listing is found, we run the price algorithm which will just add shipping if default and price .01c less.

                            If there are 2 10,000+ listings, algorithm will compare and take the best/cheapest listings price
                            '''

                            updated_price = moose_price_algorithm(seller_data=seller_data_list, )

                            '''
                             new = moose_inventory.create(
                                name=card_data['card_name'],
                                expansion=card_data['card_set'],
                                condition=card_data['card_condition'],
                                printing=printing,
                                seller_1_name=card_data['seller_1_name'],
                                seller_1_total_sales=card_data['seller_1_total_sales'],
                                seller_1_total_price=card_data['seller_1_total_price'],
                                seller_2_name=card_data['seller_2_name'],
                                seller_2_total_sales=card_data['seller_2_total_sales'],
                                seller_2_total_price=card_data['seller_2_total_price'],
                                updated_price=card_data['updated_price'],

                            )

                            new.save()
                            '''

                            if updated_price is not None and round(updated_price, 2) != current_price:
                                print(index)
                                api.update_sku_price(sku_id=sku, price=updated_price, _json=True)

                                if index < 100:
                                    print(name, expansion, condition, printing)
                                    print(f"Current: {current_price}, Market: {market}, Low: {low}, Updated: {updated_price}")

            except Exception as e:
                print(e)
                traceback_str = ''.join(traceback.format_tb(e.__traceback__))
                subject = "Error on function to update MooseLoot tcg"
                message = f"Error on function to update MooseLoot tcg:\n {card}\n\nFull Traceback:\n\n{traceback_str}"
                mail_from = 'tcgfirst'
                mail_to = ['jermol.jupiter@gmail.com', ]
                send_mail(subject, message, mail_from, mail_to)

    end_time = time()
    elapsed = (end_time - start_time) / 3600
    subject = "Time elapsed for Moose Tcg Auto Price - 1 cycle"
    message = f"Time auto price completed: {elapsed} hours"
    mail_from = 'tcgfirst'
    mail_to = ['jermol.jupiter@gmail.com', ]
    send_mail(subject, message, mail_from, mail_to)


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
                    print(f'Whatever it is cat: {sku}, {cat}')
                    sku_card_info = cat.get(sku=sku)
                except ObjectDoesNotExist:
                    try:
                        if 2 not in cat_ids_list:
                            cat = category_map[2]
                            print(f'Pokemon Cat: {sku}')
                            sku_card_info = cat.get(sku=sku)
                    except ObjectDoesNotExist:
                        cat_ids_list.append(2)
                        try:
                            if 3 not in cat_ids_list:
                                cat = category_map[3]
                                print(f'Yugioh cat: {sku}')
                                sku_card_info = cat.get(sku=sku)
                        except ObjectDoesNotExist:
                            cat_ids_list.append(3)
                            try:
                                if 1 not in cat_ids_list:
                                    cat = category_map[1]
                                    print(f'mtg cat: {sku}')
                                    sku_card_info = cat.get(sku=sku)
                            except ObjectDoesNotExist:
                                print(f'Really dont exist {sku}, {cat}')

                print(f'Final Cat: {cat}, {sku}')
                cat_ids_list = []
                if sku_card_info:
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

                    # Use pricing tool to adjust upload price
                    upload_price = sku_price_algorithm(
                        category=category, printing=printing, condition=condition, sku=sku, market=market_price, direct=direct_low_price, low=low_price,
                        language=language, expansion=expansion,
                    )

                    # Attempt to upload sku
                    uploaded_card = api.upload(sku, price=upload_price, quantity=upload_quantity)

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


