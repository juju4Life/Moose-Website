from engine.tcgplayer_api import TcgPlayerApi
from tcg.tcg_functions import tcg_condition_map

api = TcgPlayerApi('first')


def update():
    listed_cards = api.get_category_skus('magic')
    success = listed_cards['success']
    c = 0
    if success is True:
        non_direct = 0
        # total_listed = listed_cards['totalItems']
        cards = listed_cards['results']

        for card in cards:
            direct_low_price = card['directLowPrice']
            if direct_low_price is None:
                print(card['productName'], card['groupName'], card['conditionName'], card['currentPrice'], direct_low_price)
                c += 1

            if direct_low_price is not None:
                sku = card['skuId']
                current_price = card['currentPrice']
                market_price = card['marketPrice']
                low_price = card['lowPrice']

                if current_price > direct_low_price:
                    new_price = direct_low_price - .01

                    condition = card['conditionName'].replace('Foil', '').strip()

                    try:
                        if new_price < market_price * tcg_condition_map(condition):
                            new_price = market_price * tcg_condition_map(condition)
                    except TypeError:
                        pass

                    api.update_sku_price(sku_id=sku, price=new_price, _json=True)
            else:
                non_direct += 1

    else:
        # errors = listed_cards['errors']
        pass

    print(c)







