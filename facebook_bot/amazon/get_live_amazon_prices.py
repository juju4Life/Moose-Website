from datetime import datetime
from amazon.models import AmazonLiveInventory
from amazon.amazon_mws import MWS

api = MWS()

live = AmazonLiveInventory.objects
report_id = api.request_and_get_inventory_report('inventory')

headers, data = api.parse_inventory_report(report_id)
print(headers)


def no():
    for d in data:
        new_item = live.create(
            sku=d[0],
            old_price=d[1],
            new_price=0,
            time_check_delta=datetime.now(),

        )

        new_item.save()









