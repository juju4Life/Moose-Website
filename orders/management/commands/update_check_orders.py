from django.core.management.base import BaseCommand
from engine.tcgplayer_api import TcgPlayerApi
from orders.models import NewOrders


api = TcgPlayerApi()


class Command(BaseCommand):
    def handle(self, **options):
        orders = NewOrders.objects.all()
        for index, order in enumerate(orders):
            order_details = api.get_order_details([order.order_number])['results'][0]
            is_direct = order_details['isDirect']
            order.is_direct = is_direct
            order.save()
            print(index)








