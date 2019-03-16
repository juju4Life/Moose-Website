from django.core.management.base import BaseCommand
from engine.tcgplayer_api import TcgPlayerApi
from my_customs.decorators import report_error
from django.core.mail import send_mail
from engine.tcg_manifest import Manifest
from orders.models import GroupName, Inventory
from tcg.price_alogrithm import *
from time import time
from datetime import date
from decimal import Decimal


api = TcgPlayerApi()
M = Manifest()


class Command(BaseCommand):
    @report_error
    def handle(self, **options):
        start = time()
        # Cards in database as True or False for printing type
        foil_map = {
            'True': 'Foil',
            'False': 'Normal',
        }

        # Maps condition for cards that have other information attached to the condition field
        def condition_map(cond):
            cond = cond.lower()
            lp = 'lightly played'
            nm = 'near mint'
            mp = 'moderately played'
            hp = 'heavily played'
            dmg = 'damaged'
            if lp in cond:
                cond = lp
            elif nm in cond:
                cond = nm
            elif mp in cond:
                cond = mp
            elif hp in cond:
                cond = hp
            elif dmg in cond:
                cond = dmg
            return cond

        # Query all groups labeled Magic the Gathering
        groups = GroupName.objects.filter(category='Magic the Gathering')

        # Query through all groups. For each, if a filtered result in the Inventory exists, prepare var to loop over Inventory filtered list
        for index, group in enumerate(groups):
            if index >= 0:
                inventory = Inventory.objects.filter(expansion=group.group_name)

                # Get pricing data for entire group
                if inventory:
                    pricing_data = api.price_by_group_id(str(group.group_id))
                    print(group.group_name, index)

                    # Create dictionary with all pricing results mapped to product Id
                    if pricing_data['success']:
                        pricing_data = pricing_data['results']

                        d = {
                            i['productId']: {
                                'Foil': {
                                    'low': None,
                                    'mid': None,
                                    'market': None,
                                    'direct': None,
                                },
                                'Normal': {
                                    'low': None,
                                    'mid': None,
                                    'market': None,
                                    'direct': None,
                                },
                            } for i in pricing_data
                        }

                        for price in pricing_data:
                            sub_type = price['subTypeName']
                            product_id = price['productId']
                            low = price['lowPrice']
                            market = price['marketPrice']
                            mid = price['midPrice']
                            direct = price['directLowPrice']

                            d[product_id][sub_type]['low'] = low
                            d[product_id][sub_type]['market'] = market
                            d[product_id][sub_type]['mid'] = mid
                            d[product_id][sub_type]['direct'] = direct

                        # Loop through each item in Inventory, if quantity > 0  and ignore Sealed product
                        for item in inventory:
                            if item.quantity > 0 and item.custom_price is False:
                                if item.condition != 'Unopened':
                                    continue_with_price = True

                                    if item.price > 5. and item.price < 50. and item.printing == 'False':
                                        last_sold = item.last_sold_date
                                        today = date.today()
                                        delta = today - last_sold

                                        if delta.days > 10:
                                            item.price = item.price * Decimal(.95)
                                            item.save()
                                            continue_with_price = False

                                    if continue_with_price is True:
                                        # API call using each sku for product_id
                                        sku = item.sku
                                        product_id = api.card_info_by_sku(sku)['results'][0]['productId']

                                        try:
                                            is_foil = foil_map[item.printing]
                                        except KeyError as e:
                                            send_mail(subject='Not Properly configured identifier for Foil or Normal', message=f'{item.name} {item.expansion} {item.printing} error: {e}', from_email='tcgfirst', recipient_list=['jermol.jupiter@gmail.com', ])
                                            is_foil = 'Unknown'
                                        # Grab pricing data from dictionary using product id
                                        try:
                                            price_lib = d[product_id]
                                        except KeyError:
                                            get_price = api.get_market_price(str(product_id))['results']
                                            price_lib = get_price[0]
                                            if price_lib['subTypeName'] != is_foil:
                                                price_lib = get_price[1]

                                        # Run pricing algorithm base on foiling an language

                                        if is_foil == 'Normal':
                                            price_lib = price_lib['Normal']

                                            if item.language == 'English':
                                                condition = item.condition
                                                updated_price = price_algorithm(
                                                    condition=condition,
                                                    market=price_lib['market'],
                                                    direct=price_lib['direct'],
                                                    mid=price_lib['mid'],
                                                    low=price_lib['low'],
                                                )
                                                if updated_price is not None:
                                                    item.price = updated_price
                                                    api.update_sku_price(sku, updated_price, _json=True)
                                                    # print(f"{item.name} {item.expansion} {item.condition} {item.price} {item.language}")
                                                    item.save()

                                            elif item.language != 'English':
                                                condition = condition_map(item.condition)
                                                updated_price = price_foreign(
                                                    expansion=item.expansion,
                                                    language=item.language,
                                                    condition=condition,
                                                    market=price_lib['market'],
                                                    direct=price_lib['direct'],
                                                    mid=price_lib['mid'],
                                                    low=price_lib['low'],
                                                )

                                                if updated_price is not None:
                                                    item.price = updated_price
                                                    api.update_sku_price(sku, updated_price, _json=True)
                                                    # print(f"{item.name} {item.expansion} {item.condition} {item.price} {item.language}")
                                                    item.save()

                                        elif is_foil == 'Foil':
                                            try:
                                                price_lib = price_lib['Foil']
                                            except KeyError:
                                                price_lib = {}
                                            if price_lib:
                                                if item.language == 'English':
                                                    condition = condition_map(item.condition)
                                                    updated_price = price_foils(
                                                        condition=condition,
                                                        market=price_lib['market'],
                                                        direct=price_lib['direct'],
                                                        mid=price_lib['mid'],
                                                        low=price_lib['low'],
                                                    )
                                                    if updated_price is not None:
                                                        item.price = updated_price
                                                        api.update_sku_price(sku, updated_price, _json=True)
                                                        item.price = updated_price
                                                        item.save()
                                                elif item.language != 'English':
                                                    pass

                                                else:
                                                    print(f"Unknown Unknown: {is_foil} {item.name} {item.expansion} {item.price}")

                                        else:
                                            pass  # raise Exception(f'Card {item.name} {item.expansion} not labeled foil or non-foil, {item.printing}')

                                elif item.condition == 'Unopened':
                                    pass

        stop = time()

        elapsed = stop - start
        send_mail(
            subject='Update Price Time Elapsed',
            message=f'Elapse time {elapsed} seconds',
            from_email='tcgfirst',
            recipient_list=['jermol.jupiter@gmail.com', ],
        )


        print(f"Function finished in {elapsed}")





