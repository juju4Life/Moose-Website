from django.core.management.base import BaseCommand
from amazon.amazon_mws import MWS
from engine.models import CardPriceData
from engine.tcgplayer_api import TcgPlayerApi
from orders.models import GroupName
from my_customs.functions import check_direct_status, check_if_foil, null_to_zero


mws_api = MWS()
tcg = TcgPlayerApi('moose')


class Command(BaseCommand):
    def handle(self, *args, **options):
        cards = CardPriceData.objects

        groups = GroupName.objects.filter(category='Magic the Gathering')
        num_cards = 0
        for group in groups:
            price_data = tcg.price_by_group_id(group.group_id)
            if price_data['success'] is True:
                for card in price_data['results']:
                    if card['subTypeName'] == 'Normal':
                        if market_price > 3.99:
                            product_id = card['productId']
                            market_price = null_to_zero(card['marketPrice'])
                            low_price = null_to_zero(card['lowPrice'])
                            direct_low_price = null_to_zero(card['directLowPrice'])
                            is_foil = check_if_foil(card['subTypeName'])

        # report_id = mws_api.request_and_get_inventory_report('active_listings')
        report_id = '1681571789301816'
        amazon_cards = mws_api.parse_active_listings_report(report_id)[2]

        amazon_fee_list = [{'name': i['name'], 'sku': i['sku', 'price': i['price']], 'net': float(i['price']) * .85} for i in amazon_cards]
        for card in amazon_fee_list:
            sku = card['sku']
            net = card['net']
            price = card['price']
            item_name = card['name']

            obj, created = CardPriceData.objects.get_or_create(sku=sku)
            if created:
                obj.name = item_name
                obj.amazon_price = price
                obj.amazon_net = net


















