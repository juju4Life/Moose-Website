from django.core.management.base import BaseCommand
from amazon.amazon_mws import MWS
from engine.models import CardPriceData

mws_api = MWS()


class Command(BaseCommand):
    def handle(self, *args, **options):
        # report_id = mws_api.request_and_get_inventory_report('active_listings')
        report_id = '16815717893018166'
        amazon_cards = mws_api.parse_active_listings_report(report_id)[2]

        amazon_fee_list = [{'sku': i['sku', 'price': i['price']], 'net': float(i['price']) * .85} for i in amazon_cards]
        for card in amazon_fee_list:
            sku = card['sku']
            net = card['net']
            price = card['price']
            item_name = card['name']

            obj, created = CardPriceData.objects.get_or_create(sku=sku)
            if created:
               pass














