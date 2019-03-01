from django.core.management.base import BaseCommand
from engine.tcgplayer_api import TcgPlayerApi
from orders.models import NewOrders


api = TcgPlayerApi()


class Command(BaseCommand):
    def handle(self, **options):

        pass






