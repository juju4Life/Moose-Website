

def add_shipping_if_lower_than_five(value_dict):
    mapped = map(lambda i: i['price'] + .78 if i['price'] < 5 and i['default_shipping'] is True else i['price'], value_dict)

    return list(mapped)


def tcg_condition_map(condition):
    condition = condition_from_string(condition)
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


def moose_price_algorithm(seller_data_list, market_price, low_price, condition):
    if len(seller_data_list) == 2:
        seller_prices = sorted(seller_data_list)
        update_price = seller_prices[0] - .01

        if low_price > 2:
            if seller_prices[0] < seller_prices[1] / 1.1 + 1:
                update_price = seller_prices[1] - .01
        else:
            if seller_prices[0] < seller_prices[1] / 1.2:
                update_price = seller_prices[1] - .01

        condition = tcg_condition_map(condition)
        if update_price is not None:
            if market_price is not None:
                if update_price < market_price * condition:
                    update_price = market_price
            else:
                update_price = None

            if update_price < low_price - .02:
                update_price = None

        return update_price


def condition_from_string(string):
    string = string.lower()

    if 'near mint' in string:
        return 'Near Mint'

    elif 'lightly played' in string:
        return 'Lightly Played'

    elif 'moderately played' in string:
        return 'Moderately Played'

    elif 'heavily played' in string:
        return 'Heavily Played'

    elif 'damaged' in string:
        return 'Damaged'












