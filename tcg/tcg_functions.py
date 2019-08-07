

def add_shipping_if_lower_than_five(value_dict):
    mapped = map(lambda i: i['price'] + .78 if i['price'] < 5 and i['default_shipping'] is True else i, value_dict)

    return [i['price'] for i in mapped]


def tcg_condition_map(condition):
    condition_map = {
        'Near Mint': .9,
        'Near Mint Foil': .9,
        'Lightly Played': .9,
        'Lightly Played Foil': .9,
        'Moderately Played': .7,
        'Moderately Played Foil': .7,
        'Heavily Played': .6,
        'Heavily Played Foil': .6,
        'Damaged': .5,
        'Damaged Foil': .5,
        'Unopened': .9,
        }

    return condition_map[condition]


def moose_price_algorithm(seller_data_list, market_price, condition):
    if len(seller_data_list) == 2:
        seller_prices = add_shipping_if_lower_than_five(seller_data_list)
        seller_prices = sorted(seller_prices)
        update_price = seller_prices[0] - .01
        if seller_prices[0] < seller_prices[1] / 1.2:
            update_price = seller_prices[1] - .01

        if update_price < market_price * tcg_condition_map(condition):
            if 'Foil' not in condition:
                update_price = market_price

        return update_price

    elif len(seller_data_list) == 1:
        seller_prices = add_shipping_if_lower_than_five(seller_data_list)
        update_price = seller_prices[0] - .01
        if update_price < market_price * tcg_condition_map(condition):
            if 'Foil' not in condition:
                update_price = market_price
                return update_price

        else:
            return None

    else:
        return None














