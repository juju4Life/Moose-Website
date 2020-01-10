from django.core.management.base import BaseCommand
from engine.tcgplayer_api import TcgPlayerApi
from orders.models import Inventory
from tcg.price_alogrithm import sku_price_algorithm

api = TcgPlayerApi('first')


class Command(BaseCommand):
    def handle(self, **options):
        database = Inventory.objects.filter(category='Star Wars Destiny')

        for index, item in enumerate(database):
            if item.quantity > 0 and item.price == 0:
                if item.condition != 'Unopened':
                    sku_price = api.market_prices_by_sku([item.sku])['results'][0]
                    market_price = sku_price['marketPrice']
                    low_price = sku_price['lowPrice']
                    direct_low_price = sku_price['directLowPrice']

                    upload_price = sku_price_algorithm(
                            category=item.category, printing=item.printing, condition=item.condition, sku=item.sku, market=market_price, direct=direct_low_price,
                        low=low_price
                        )

                    if upload_price is not None:
                        item.price = upload_price
                        api.update_sku_price(item.sku, upload_price, _json=True)
                        item.save()
                        print(index)









