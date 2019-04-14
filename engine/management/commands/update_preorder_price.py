from django.core.management import BaseCommand
from engine.tcgplayer_api import TcgPlayerApi
from customer.models import ItemizedPreorder
from tcg.rarity_algorithm import rarity_round
api = TcgPlayerApi()


class Command(BaseCommand):
    def handle(self, *args, **options):
        preorders = ItemizedPreorder.objects.all()

        for preorder in preorders:
            product_id = preorder.product_id
            price_data = api.get_market_price(product_id)['results']
            price = price_data[0]
            if price['subTypeName'] == 'Foil':
                price = price_data[1]

            market = price['marketPrice']
            low = price['lowPrice']
            new_price = market

            if low is not None:
                if market is not None:
                    if low > market:
                        new_price = low
                else:
                    new_price = low
            else:
                preorder.available = False

            if preorder.available is True:
                new_price = rarity_round(preorder.rarity, new_price)
                preorder.price = new_price

            preorder.save()
            print(preorder.name, preorder.price)


