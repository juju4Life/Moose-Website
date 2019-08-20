from datetime import datetime
from django.core.management.base import BaseCommand
from amazon.models import AmazonLiveInventory
from amazon.amazon_mws import MWS
import json

api = MWS()


class Command(BaseCommand):
    def handle(self, *args, **options):
        # print(api.parse_active_listings_report('16237027463018127'))
        print(api.check_feed_submission('151729018128'))

        # api.request_and_get_inventory_report('active_listings')
        # d = api.get_sku_lowest_offer(['WT-I22S-J83M', 'WR-1M67-09LV'], 'new')

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




