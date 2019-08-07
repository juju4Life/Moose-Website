from django.core.management.base import BaseCommand
from engine.tcgplayer_api import TcgPlayerApi
from bs4 import BeautifulSoup as B
from my_customs.functions import float_from_string, null_to_zero, check_if_foil, integers_from_string
from tcg.tcg_functions import moose_price_algorithm
import requests
import random

api = TcgPlayerApi()
# filterName=Condition&filterValue=LightlyPlayed


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


class Command(BaseCommand):
    def handle(self, *args, **options):
        listed_cards = api.get_category_skus('magic')
        if listed_cards['success'] is True:
            for card in listed_cards['results']:
                sku = card['skuId']
                product_id = card['productId']
                name = card['productName']
                expansion = card['groupName']
                printing = card['printingName']
                market = card['marketPrice']
                condition = card['conditionName']
                next_page = True
                page = 1
                seller_data_list = []
                while next_page is True:
                    request_path = url(product_id=product_id, condition=condition, foil=printing, page=page)
                    r = requests.get(request_path).content
                    print(page, request_path)
                    soup = B(r, 'html.parser')
                    data = soup.find_all('div', {'class': 'product-listing '})
                    for d in data:
                        seller_total_sales = integers_from_string(d.find('span', {'class': 'seller__sales'}).text)
                        seller_name = d.find('a', {'class': 'seller__name'}).text.strip()
                        seller_condition = d.find('div', {'class': 'product-listing__condition'}).text.strip()
                        if seller_total_sales >= 10000 and seller_name != 'MTGFirst' and condition == seller_condition:
                            # seller_feedback = d.find('span', {'class': 'seller__feedback-rating'}).text
                            price = float_from_string(d.find('span', {'class': 'product-listing__price'}).text)
                            if price is not None:
                                shipping = float_from_string(d.find('span', {'class': 'product-listing__shipping'}).text.strip())
                                if shipping == 25.:
                                    shipping = .99
                                total_price = price + shipping

                                price_and_default = {
                                    'price': total_price,
                                    'default_shipping': True if shipping == 0 else False
                                }
                                print(name, expansion, printing)
                                print(condition, seller_condition)
                                print(seller_name, seller_total_sales)
                                print(price, shipping)
                                print('_______________')

                                seller_data_list.append(price_and_default)
                                if len(seller_data_list) == 2:
                                    next_page = False
                                    break
                    page += 1

                updated_price = moose_price_algorithm(seller_data_list=seller_data_list, market_price=market, condition=condition)
                print(seller_data_list, updated_price)
                # api.update_sku_price(sku_id=sku, price=updated_price, _json=True)

        else:
            pass




