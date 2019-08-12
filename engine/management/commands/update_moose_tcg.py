from django.core.management.base import BaseCommand
from orders.tasks import update_moose_tcg
from my_customs.decorators import report_error
import random
from bs4 import BeautifulSoup as B
from my_customs.functions import float_from_string, null_to_zero, check_if_foil, integers_from_string
from tcg.tcg_functions import moose_price_algorithm
import requests
from time import time
from engine.tcgplayer_api import TcgPlayerApi
from django.core.mail import send_mail
import csv

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


        'Foil': f'https://shop.tcgplayer.com/productcatalog/product/changepricetablepage?filterName=Foil&filterValue=Foil&productId={product_id}&'
        f'gameName=magic&page={page}&X-Requested-With=XMLHttpRequest&_={random_string}',

        }

    return url_path[foil]


class Command(BaseCommand):
    @report_error
    def handle(self, *args, **options):
        # update_moose_tcg.apply_async(que='low_priority')
        item_data = []
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
                    if condition != 'Unopened' and printing == 'Foil':
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
                                    api.update_sku_price(sku_id=sku, price=updated_price, _json=True)
                            else:

                                card_data = {
                                    'card_name': '',
                                    'card_set': '',
                                    'card_condition': '',
                                    'seller_1_name': '',
                                    'seller_1_total_sales': '',
                                    'seller_2_name': '',
                                    'seller_2_total_sales': '',
                                    'seller_1_total_price': '',
                                    'seller_2_total_price': '',
                                    'Updated_price': '',
                                }

                                next_page = True
                                page = 1
                                seller_data_list = []

                                while next_page is True:
                                    request_path = url(product_id=product_id, condition=condition, foil=printing, page=page)
                                    r = requests.get(request_path).content
                                    soup = B(r, 'html.parser')
                                    data = soup.find_all('div', {'class': 'product-listing '})

                                    # Check if there are products in the request. If not that indicates no more listings and thus we break the loop
                                    if not data:
                                        break
                                    # loop over each item on the page and get Seller Info

                                    for d in data:
                                        check = d.find('span', {'class': 'seller__sales'})
                                        if check is not None:
                                            seller_total_sales = integers_from_string(d.find('span', {'class': 'seller__sales'}).text)
                                            seller_name = d.find('a', {'class': 'seller__name'}).text.strip()
                                            seller_condition = d.find('div', {'class': 'product-listing__condition'}).text.strip()
                                            if seller_total_sales >= 10000 and seller_name != 'MTGFirst' and seller_name != 'Moose Loot' and condition == seller_condition:

                                                # seller_feedback = d.find('span', {'class': 'seller__feedback-rating'}).text
                                                # function extracts all floating points from string.
                                                price = float_from_string(d.find('span', {'class': 'product-listing__price'}).text)

                                                # Fail Safe in the case where html is changed and no real value is extracted
                                                if price is not None and price is not 0:
                                                    shipping = float_from_string(d.find('span', {'class': 'product-listing__shipping'}).text.strip())

                                                    # 25 would be extracted from shipping text that state "Free shipping over 25". We make this result 0 and
                                                    # handle additional shipping costs using defaults
                                                    if shipping == 25.:
                                                        shipping = 0

                                                    # Default shipping added to cards under five.
                                                    if price >= 5:
                                                        total_price = price + shipping
                                                    else:
                                                        total_price = price

                                                    # We are appending the two cheapest listings with 10,000 minimum sales and that meets other if requirements.
                                                    # Break once we get 2
                                                    seller_data_list.append(total_price)
                                                    if len(seller_data_list) == 1:
                                                        card_data['seller_1_name'] = seller_name
                                                        card_data['seller_1_total_sales'] = seller_total_sales
                                                        card_data['seller_1_total_price'] = total_price
                                                        card_data['card_name'] = name
                                                        card_data['card_set'] = expansion
                                                        card_data['card_condition'] = condition

                                                    if len(seller_data_list) == 2:
                                                        card_data['seller_2_name'] = seller_name
                                                        card_data['seller_2_total_sales'] = seller_total_sales
                                                        card_data['seller_2_total_price'] = total_price
                                                        next_page = False
                                                        break
                                    page += 1

                                '''
                                We will check the number of other seller listings.
                                If there were zero listings found we simply make the updated price the market price.
    
                                If just one listing is found, we run the price algorithm which will just add shipping if default and price .01c less.
    
                                If there are 2 10,000+ listings, algorithm will compare and take the best/cheapest listings price
                                '''

                                if len(seller_data_list) == 1:
                                    seller_data_list.append(0)

                                updated_price = moose_price_algorithm(seller_data_list=seller_data_list, market_price=market, low_price=low,
                                                                      condition=condition)
                                card_data['updated_price'] = updated_price
                                item_data.append(card_data)

                                if updated_price is not None:
                                    api.update_sku_price(sku_id=sku, price=updated_price, _json=True)
                                    if index < 100:
                                        print(index, name, expansion, condition, printing)
                                        print(f"Current: {current_price}, Market: {market}, low: {low}, Updated: {updated_price}")

                except Exception as e:
                    print(e)
                    subject = "Error on function to update MooseLoot tcg"
                    message = f"Error on function to update MooseLoot tcg:\n {card}\n\nSeller Info: {seller_name, seller_total_sales}"
                    mail_from = 'tcgfirst'
                    mail_to = ['jermol.jupiter@gmail.com', ]
                    send_mail(subject, message, mail_from, mail_to)

        end_time = time()
        elapsed = end_time - start_time
        subject = "Time elapsed for Moose Tcg Auto Price - 1 cycle"
        message = f"Time auto price completed: {elapsed} seconds"
        mail_from = 'tcgfirst'
        mail_to = ['jermol.jupiter@gmail.com', ]
        send_mail(subject, message, mail_from, mail_to)

        with open('moose_foils.csv', 'w', newline='') as f:
            fieldnames = ['card_name', 'card_set', 'card_condition', 'seller_1_name', 'seller_1_total_sales', 'seller_1_total_price',
                          'seller_2_name', 'seller_2_total_sales', 'seller_2_total_price', 'updated_price', ]

            writer = csv.DictWriter(f=f, fieldnames=fieldnames)

            for d in item_data:
                writer.writerow(d)







