from django.core.management.base import BaseCommand
from amazon.amazon_mws import MWS
from engine.models import CardPriceData

api = MWS()


class Command(BaseCommand):
    def handle(self, *args, **options):
        report_id = api.request_and_get_inventory_report('inventory')

        headers, data = api.parse_inventory_report(report_id)

        dic = {}

        for d in data:
            dic[d['sku']] = d['price']

        obj_data = CardPriceData.objects.exclude(sku='')

        for obj in obj_data:
            price = dic.get(obj.sku, None)
            if price is not None:
                obj.amazon_price = price
                obj.save()








