from django.core.management.base import BaseCommand
from amazon.models import AmazonLiveInventory
from amazon.amazon_mws import MWS
from my_customs.exml import CreateXML
import json

api = MWS()
x = CreateXML()


class Command(BaseCommand):
    def handle(self, *args, **options):
        update_feeds = []
        inventory = AmazonLiveInventory.objects.all()
        num_items = 20  # inventory.count()
        start = 17
        stop = 19
        while num_items > 0:
            if stop > inventory.count():
                stop = inventory.count()
            items = inventory[start:stop]

            skus = [i.sku for i in items]
            prices = api.get_sku_prices(skus)

            for i in prices:
                sku = i['SellerSKU']['value']
                new_price = i['Product']['CompetitivePricing']['CompetitivePrices']['CompetitivePrice']['Price']['LandedPrice']['Amount'][
                                       'value']

                old_price = items.filter(sku=sku).old_price

                if old_price != new_price:
                    pass

            for s in items:
                update_feeds.append({
                    'sku': s.sku,
                    'price': round(float(s.old_price) - .01, 2),
                })

            start += 20
            stop += 20
            num_items -= 20

        # feed = x.generate_mws_price_xml(update_feeds)
        # print(api.update_sku_price(feed))

















