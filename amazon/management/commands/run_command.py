from django.core.management.base import BaseCommand
from amazon.models import AmazonLiveInventory
from amazon.amazon_mws import MWS

api = MWS()


class Command(BaseCommand):
    def handle(self, *args, **options):
        live = AmazonLiveInventory.objects
        report_id = api.request_and_get_inventory_report('inventory')

        headers, data = api.parse_inventory_report(report_id)

        for d in data:
            new_item = live.create(
                sku=d[0],
                price=d[2],

            )



