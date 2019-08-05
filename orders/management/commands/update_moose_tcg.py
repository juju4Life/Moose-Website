from django.core.management.base import BaseCommand
from engine.tcgplayer_api import TcgPlayerApi
from bs4 import BeautifulSoup as B
from my_customs.functions import float_from_string, null_to_zero, check_if_foil
import requests
import random

api = TcgPlayerApi()
# filterName=Condition&filterValue=LightlyPlayed


def url(product_id, foil, condition, page=1):
    random_string = str(random.randint(1000000000000, 9999999999999))
    condition = condition.replace(" ", "")
    is_foil = check_if_foil(foil)

    url_path = {
        False: f'https://shop.tcgplayer.com/productcatalog/product/changedetailsfilter?captureFeaturedSellerData=True&pageSize=10&'
        f'filterName=Condition&filterValue={condition}&productId={product_id}&gameName=magic&_={random_string}&page={page}',


        True: f'https://shop.tcgplayer.com/productcatalog/product/changedetailsfilter?'
        f'filterName=Printing&filterValue=Foil&pageSize=10&productId={product_id}&gameName=magic&_={random_string}&page={page}',
        }

    return url_path[is_foil]


class Command(BaseCommand):
    def handle(self, *args, **options):
        listed_cards = api.get_category_skus('magic')
        if listed_cards['success'] is True:
            for card in listed_cards['results']:
                product_id = card['productId']
                name = card['productName']
                expansion = card['groupName']
                printing = card['printingName']
                low = card['lowPrice']
                condition = card['conditionName']
                next_page = True
                page = 1
                while next_page is True:
                    request_path = url(product_id=product_id, condition='Near Mint', foil=printing, page=page)
                    r = requests.get(request_path).content
                    print(page, request_path)
                    soup = B(r, 'html.parser')
                    data = soup.find_all('div', {'class': 'product-listing '})
                    for d in data:
                        seller_total_sales = float_from_string(d.find('span', {'class': 'seller__sales'}).text)
                        print(d.find('a', {'class': 'seller__name'}).text.strip(), seller_total_sales)
                        if seller_total_sales >= 10000:
                            name = d.find('a', {'class': 'seller__name'}).text.strip()
                            # seller_feedback = d.find('span', {'class': 'seller__feedback-rating'}).text
                            price = float_from_string(d.find('span', {'class': 'product-listing__price'}).text)
                            seller_condition = d.find('div', {'class': 'product-listing__condition'}).text.strip()
                            if price is not None:
                                shipping = float_from_string(d.find('span', {'class': 'product-listing__shipping'}).text.strip())
                                total_price = price + shipping
                    page += 1

        else:
            pass




