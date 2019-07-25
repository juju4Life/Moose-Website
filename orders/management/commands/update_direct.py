from django.core.management.base import BaseCommand
from engine.tcgplayer_api import TcgPlayerApi

api = TcgPlayerApi()


class Command(BaseCommand):
    def handle(self, **options):
        listed_cards = api.get_category_skus('magic')

        success = listed_cards['success']
        if success is True:
            non_direct = 0
            # total_listed = listed_cards['totalItems']
            cards = listed_cards['results']

            for card in cards:
                direct_low_price = card['directLowPrice']

                if direct_low_price is not None:
                    sku = card['skuId']
                    current_price = card['currentPrice']
                    market_price = card['marketPrice']
                    new_price = ''

                    if current_price > direct_low_price:
                        new_price = direct_low_price - .01

                        api.update_sku_price(sku_id=sku, price=new_price, _json=True)
                else:
                    non_direct += 1
        else:
            errors = listed_cards['errors']













