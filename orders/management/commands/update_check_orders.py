from django.core.management.base import BaseCommand
from engine.tcgplayer_api import TcgPlayerApi
from orders.models import NewOrders


api = TcgPlayerApi()


class Command(BaseCommand):
    def handle(self, **options):
        orders = NewOrders.objects.all()
        for order in orders:
            order_details = api.get_order_details(order.order_number)
            is_direct = order_details








