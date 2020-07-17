from amazon.amazon_mws import MWS
from django.core.management.base import BaseCommand
from engine.models import CardPriceData
from tcg.tcg_functions import amazon_fee_calc


class Command(BaseCommand):
    def handle(self, *args, **options):
        mws = MWS()

        start = 0
        stop = 20
        count = CardPriceData.objects.exclude(sku="").count()
        print(count)

        while stop < count:
            cards = CardPriceData.objects.exclude(sku="")[start:stop]
            skus = [card.sku for card in cards]
            objs = {card.sku: card for card in cards}
            amazon_prices = mws.get_sku_prices(skus)
            for ap in amazon_prices:
                sku = ap["SellerSKU"]["value"]
                try:
                    price = ap["Product"]["CompetitivePricing"]["CompetitivePrices"]["CompetitivePrice"]["Price"]["LandedPrice"]["Amount"]["value"]
                except KeyError:
                    try:
                        price = ap["Product"]["CompetitivePricing"]["CompetitivePrices"]
                        if not price:
                            pass
                    except KeyError as e:
                        print(e)
                        price = None
                except TypeError:
                    price = ap["Product"]["CompetitivePricing"]["CompetitivePrices"]["CompetitivePrice"][0]["Price"]["LandedPrice"]["Amount"]["value"]

                if price:
                    amazon_net, other = amazon_fee_calc(float(price))
                    obj = objs[sku]
                    obj.amazon_price = price
                    obj.amazon_net = amazon_net
                    obj.save()

            start += 20
            stop += 20
            print(stop)

