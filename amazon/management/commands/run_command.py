from datetime import datetime
from django.core.management.base import BaseCommand
from amazon.models import AmazonLiveInventory
from amazon.amazon_mws import MWS
import json

api = MWS()


class Command(BaseCommand):
    def handle(self, *args, **options):
        # a, b = api.parse_active_listings_report('16381982011018137')
        # a = api.get_sku_lowest_priced_offer('1U-PLK0-3Q09')
        a = api.get_asin_lowest_offer(asin='B019CZA9KO', condition='new')
        print(json.dumps(a, indent=4))
        # print(api.check_feed_submission('151729018128'))

        # api.request_and_get_inventory_report('active_listings')
        # d = api.get_sku_lowest_offer('1U-PLK0-3Q09', 'new')

        '''
         live = AmazonLiveInventory.objects
        report_id = api.request_and_get_inventory_report('inventory')

        headers, data = api.parse_inventory_report(report_id)

        for d in data:
            new_item = live.create(
                sku=d[0],
                old_price=d[1],
                new_price=0,
                time_check_delta=datetime.now(),

            )

            new_item.save()
        '''




