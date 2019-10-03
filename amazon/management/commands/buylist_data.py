from django.core.management.base import BaseCommand
from itertools import combinations
from amazon.amazon_mws import MWS
from engine.models import CardPriceData, MTG
from engine.tcgplayer_api import TcgPlayerApi
from orders.models import GroupName
from my_customs.functions import check_direct_status, check_if_foil, null_to_zero

mws_api = MWS()
tcg = TcgPlayerApi('moose')


class Command(BaseCommand):
    def handle(self, *args, **options):
        card_data = CardPriceData.objects

        # report_id = mws_api.request_and_get_inventory_report('active_listings')

        report_id = '16857831116018170'
        amazon_cards = mws_api.parse_active_listings_report(report_id)[2]
        amazon_fee = 15
        shipping_fee = 2.85
        amazon_fee_list = [{'name': i['name'], 'sku': i['sku'], 'price': i['price'], 'net': float(i['price']) * .85} for i in amazon_cards]
        print(len(amazon_fee_list))
        for index, card in enumerate(amazon_fee_list):
            item_name = card['name']
            if 'foil' not in item_name.lower():
                sku = card['sku']
                # net = card['net']
                price = float(card['price'])
                net = price * ((100 - amazon_fee) / 100) - shipping_fee

                substrings = [item_name[x:y] for x, y in combinations(range(len(item_name) + 1), r=2)]
                c = card_data.filter(expansion__in=substrings).filter(name__in=substrings).first()

                try:
                    if c:
                        c.sku = sku
                        c.amazon_net = net
                        c.amazon_price = price
                        c.save()
                        print(index)
                    else:
                        print('Not On TcgPlayer')
                        print(item_name)
                except Exception as e:
                    print(e)
                    print(card)

'''
        cards = CardPriceData.objects
        groups = GroupName.objects.filter(category='Magic the Gathering')
        num_cards = 0
        for group in groups:
            print(group.group_name)
            price_data = tcg.price_by_group_id(group.group_id)
            if price_data['success'] is True:
                for card in price_data['results']:
                    if card['subTypeName'] == 'Normal':
                        market_price = null_to_zero(card['marketPrice'])
                        if market_price > 2.99:
                            product_id = card['productId']
                            card_info = MTG.objects.filter(product_id=product_id).first()
                            if card_info is not None:
                                name = card_info.product_name
                                expansion = card_info.set_name

                                low_price = null_to_zero(card['lowPrice'])
                                direct_low_price = null_to_zero(card['directLowPrice'])
                                is_foil = check_if_foil(card['subTypeName'])

                                cards.get_or_create(
                                    name=name,
                                    expansion=expansion,
                                    product_id=product_id,
                                )

                                num_cards += 1
                                print(num_cards)

'''
























