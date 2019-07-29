from django.core.management.base import BaseCommand
from my_customs.decorators import report_error
from my_customs.functions import check_direct_status, check_if_foil
from engine.models import TcgGroupPrice
from engine.tcgplayer_api import TcgPlayerApi
from engine.models import MTG
from orders.models import GroupName

api = TcgPlayerApi()


class Command(BaseCommand):
    @report_error
    def handle(self, **options):
        groups = GroupName.objects.filter(category='Magic the Gathering').filter(added=False)

        for group in groups:
            price_data = api.price_by_group_id(group.group_id)
            if price_data['success'] is True:
                for card in price_data['results']:
                    if card['subTypeName'] == 'Normal':
                        product_id = card['productId']
                        market_price = card['marketPrice']
                        low_price = card['lowPrice']
                        direct_low_price = card['directLowPrice']
                        mid_price = card['midPrice']
                        high_price = card['highPrice']
                        is_direct = check_direct_status(direct_low_price)
                        is_foil = check_if_foil(card['subTypeName'])











