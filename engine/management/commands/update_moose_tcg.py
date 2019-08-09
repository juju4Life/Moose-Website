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


        'Foil': f'https://shop.tcgplayer.com/productcatalog/product/getpricetable?filterName=Printing&filterValue=Foil&captureFeaturedSellerData=True&'
        f'pageSize=10&productId={product_id}&gameName=magic&_={random_string}',

        }

    return url_path[foil]


class Command(BaseCommand):
    @report_error
    def handle(self, *args, **options):
        update_moose_tcg.apply_async(que='low_priority')





