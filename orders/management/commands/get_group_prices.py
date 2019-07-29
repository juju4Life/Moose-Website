from django.core.management.base import BaseCommand
from my_customs.decorators import report_error
from my_customs.functions import check_direct_status, check_if_foil
from engine.models import TcgGroupPrice, MTG
from engine.tcgplayer_api import TcgPlayerApi
from engine.models import MTG
from orders.models import GroupName

api = TcgPlayerApi()


class Command(BaseCommand):
    @report_error
    def handle(self, **options):
        groups = GroupName.objects.filter(category='Magic the Gathering').filter(added=True)

        for group in groups:
            cards_over_five = 0
            print(group)
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

                        card_info = MTG.objects.filter(product_id=product_id).first()

                        if card_info is not None and market_price > 5 or low_price > 5:
                            name = card_info.product_name
                            expansion = card_info.set_name

                            obj, created = TcgGroupPrice.objects.get_or_create(
                                product_id=product_id,
                                name=name,
                                expansion=expansion,
                                foil=is_foil,
                                is_direct=is_direct,
                                low_price=low_price,
                                market_price=market_price,
                                mid_price=mid_price,
                                high_price=high_price,
                                direct_low_price=direct_low_price
                            )

                            obj.save()
                            cards_over_five += 1
                        else:
                            pass
            print(cards_over_five)














