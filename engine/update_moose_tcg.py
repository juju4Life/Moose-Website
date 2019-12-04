import random
import traceback
from time import time
from django.core.mail import send_mail
from engine.tcgplayer_api import TcgPlayerApi
from engine.models import MooseAutopriceMetrics
from my_customs.functions import request_pages_data
from my_customs.decorators import report_error
from tcg.tcg_functions import moose_price_algorithm, get_product_seller_info, metrics_update


api = TcgPlayerApi('moose')


@report_error
def moose_price():
    start_time = time()
    # Entire Moose Loot Listed inventory
    listed_cards = api.get_category_skus('magic')
    if listed_cards['success'] is True:
        print(f"Updating {listed_cards['totalItems']} for Moose Inventory")
        for index, card in enumerate(listed_cards['results']):
            try:
                condition = card['conditionName']
                printing = card['printingName']
                current_price = card['currentPrice']
                low = card['lowPrice']
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

                if condition == 'Unopened':
                    if current_price != low:
                        try:
                            updated_price = low - .01
                        except TypeError:
                            updated_price = None

                        if updated_price is not None:
                            if updated_price < .25:
                                updated_price = .25
                            api.update_sku_price(sku_id=sku, price=updated_price, _json=True)

                            updated_price = updated_price * .95
                            if updated_price < .25:
                                updated_price = .25
                            api.update_sku_price(sku_id=sku, price=updated_price, _json=True, channel='1')

                if language != 'English' and printing != 'Foil' and condition != 'Unopened':
                    # catch instances where there is no low price

                    good_languages = ['Japanese', 'Korean', 'Russian', 'German']

                    compare_price = api.get_market_price(product_id)
                    if compare_price['success']is True:
                        english_data = compare_price['results'][0]
                        if english_data['subTypeName'] == 'Foil':
                            english_data = compare_price['results'][1]

                        english_low = english_data['lowPrice']

                        if current_price != english_low:

                            if language in good_languages:
                                try:
                                    updated_price = english_low - .01
                                except TypeError:
                                    updated_price = None
                            else:
                                try:
                                    updated_price = english_low * .90
                                except TypeError:
                                    updated_price = None

                            if updated_price is not None:
                                if updated_price < .25:
                                    updated_price = .25
                                api.update_sku_price(sku_id=sku, price=updated_price, _json=True)
                                metrics, created = MooseAutopriceMetrics.objects.get_or_create(sku=sku)
                                metrics_update(
                                    metrics=metrics,
                                    expansion=expansion,
                                    name=name,
                                    condition=condition,
                                    printing=printing,
                                    language=language,
                                    current_price=current_price,
                                    updated_price=updated_price,
                                    low=low,
                                )
                                updated_price = updated_price * .95
                                if updated_price < .25:
                                    updated_price = .25
                                api.update_sku_price(sku_id=sku, price=updated_price, _json=True, channel='1')

                elif language == 'English' and condition != 'Unopened':

                    next_page = True
                    page = 1
                    seller_data_list = []
                    random_string = str(random.randint(1000000000000, 9999999999999))

                    while next_page is True:

                        path = f'https://shop.tcgplayer.com/productcatalog/product/getpricetable?captureFeaturedSellerData=True&pageSize=10&productId={product_id}' \
                            f'&gameName=magic&useV2Listings=false&_={random_string}&page={page}'

                        data, page_source = request_pages_data(
                            url=path,
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
                                    'gold': True if seller_total_sales >= 10000 else False,
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
                    # print(f'Updated Price for {name}, {expansion}, {current_price}, {updated_price}')
                    if updated_price is not None and round(updated_price, 2) != current_price:
                        # print(index)

                        if updated_price < .25:
                            updated_price = .25

                        api.update_sku_price(sku_id=sku, price=updated_price, _json=True)

                        metrics, created = MooseAutopriceMetrics.objects.get_or_create(sku=sku)
                        metrics_update(
                            metrics=metrics,
                            seller_data_list=seller_data_list,
                            expansion=expansion,
                            name=name,
                            condition=condition,
                            printing=printing,
                            language=language,
                            current_price=current_price,
                            updated_price=updated_price,
                        )

                        updated_price = updated_price * .95
                        if updated_price < .25:
                            updated_price = .25
                        api.update_sku_price(sku_id=sku, price=updated_price, _json=True, channel='1')

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
            print(f"Moose Card #{index}")
    end_time = time()
    elapsed = (end_time - start_time) / 3600
    subject = "Time elapsed for Moose Tcg Auto Price - 1 cycle"
    message = f"Time auto price completed: {elapsed} hours"
    mail_from = 'tcgfirst'
    mail_to = ['jermol.jupiter@gmail.com', ]
    send_mail(subject, message, mail_from, mail_to)





