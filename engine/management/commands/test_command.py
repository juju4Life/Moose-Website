from django.core.management.base import BaseCommand
from buylist.ck_buylist import ck_buylist, get_page_count
from buylist.scg_buylist import get_scg_buylist
import requests
from bs4 import BeautifulSoup as b


class Command(BaseCommand):
    def handle(self, *args, **options):
        # ck_buylist(get_page_count())
        # get_scg_buylist()
        url = 'https://shop.tcgplayer.com/productcatalog/product/getpricetable?captureFeaturedSellerData=True&pageSize=10&productId=122604&gameName=magic' \
              '&useV2Listings=false&_=5933406623101'

        r = requests.get(url).content
        soup = b(r, 'html.parser')
        print(soup.prettify())
























