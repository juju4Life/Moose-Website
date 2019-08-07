from engine.tcgplayer_api import TcgPlayerApi


api = TcgPlayerApi()


def add_shipping_if_lower_than_five(value_dict):
    mapped = map(lambda i: i['price'] + .78 if i['price'] < 5 and i['default_shipping'] is True else i, value_dict)

    return [i['price'] for i in mapped]


def moose_price_algorithm(seller_data_list, market_price, condition):
    seller_prices = add_shipping_if_lower_than_five(seller_data_list)

    update_price = seller_prices[0] - .01
    if seller_prices[0] < seller_prices[1] / 1.2:
        update_price = seller_prices[1] - .01

    condition_map = {
        'Near Mint': .8,
        'Lightly Played': .7,
        'Moderately Played': .6,
        'Heavily Played': .5,
    }

    if update_price < market_price * condition_map[condition]:
        update_price = market_price

    return update_price














