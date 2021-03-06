
from django.db import transaction
from engine.models import MTG, TcgGroupPrice
from engine.tcg_reports import Report
from tcg.price_alogrithm import tcg_low_market


class Inventory:

    @staticmethod
    def update_store_inventory():
        TcgGroupPrice.objects.all().delete()

        # Loop through prices by each tcg set. Report contains dictionary with keys "Data" containing list of prices and "expansion" holding the set name
        for report in Report().prices_by_set():
            if report:
                group_price_upload_list = list()
                with transaction.atomic():
                    # Get corresponding set filter from MTG Database
                    expansion_data = MTG.objects.filter(expansion=report['expansion'])

                    for card in report['data']:
                        product_id = str(card['productId'])
                        printing = card['subTypeName']
                        low = card['lowPrice']
                        market = card['marketPrice']
                        mid = card['midPrice']
                        direct = card['directLowPrice']

                        # Check if card is in db
                        card_in_db = expansion_data.filter(product_id=product_id)
                        if card_in_db and low is not None and low < 50:

                            # Update correct field for normal vs foil after price algorithm
                            if printing == 'Foil':
                                clean, played, hp = tcg_low_market(low=low, market=market)
                                card_in_db.update(foil_clean_price=clean)
                                card_in_db.update(foil_played_price=played)
                                card_in_db.update(foil_heavily_played_price=hp)

                            else:
                                clean, played, hp = tcg_low_market(low=low, market=market)
                                card_in_db.update(normal_clean_price=clean)
                                card_in_db.update(normal_played_price=played)
                                card_in_db.update(normal_heavily_played_price=hp)

                        if market is not None:
                            if market >= 1.5:
                                group_price_upload_list.append(
                                    TcgGroupPrice(
                                        product_id=product_id,
                                        printing=printing,
                                        low_price=low,
                                        mid_price=mid,
                                        market_price=market,
                                        direct_low_price=direct,
                                    )
                                )

                TcgGroupPrice.objects.bulk_create(group_price_upload_list)




