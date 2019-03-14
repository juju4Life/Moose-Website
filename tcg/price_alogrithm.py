from engine.tcgplayer_api import TcgPlayerApi

api = TcgPlayerApi()


def price_foreign(expansion, condition, language, low, direct=None, mid=None, market=None):
    print(f'Inside price foreign function {low} {mid} {market}')
    condition_map = {
        'near mint': 1.,
        'lightly played': 1.,
        'moderately played': .85,
        'heavily played': .70,
        'damaged': .60,
    }

    old_sets = ["urza's saga", " urza's legacy", "urza's destiny", "exodus", "stronghold", "tempest", "mirage", "visions",

                "weatherlight", "fifth edition", "fourth edition", ]

    expansion_list = ['beta edition', 'alpha edition', 'legends', 'the dark', 'arabian nights', 'portal second age', 'portal three kingdoms', 'portal',
                      'unlimited', ]
    if low is not None:
        price = low
        if market is not None and mid is not None:
            if expansion.lower() not in expansion_list:
                average = (market + low + mid) / 3
                if low < average * .9:
                    price = average * .9
        elif market is not None:
            if market > low * 1.5:
                price = price * 1.3
        price = price * condition_map[condition.lower()]

        if language == 'korean' and expansion.lower() in old_sets:
            price = price * 1.25

        if price < 2.:
            price = 2.

        if market > price * 1.5:
            price = price * 1.20

        return price

    else:
        return None


def price_foils(condition, low, direct=None, mid=None, market=None):
    condition_map = {
        'near mint': 1.,
        'lightly played': 1.,
        'moderately played': .85,
        'heavily played': .70,
        'damaged': .60,
    }

    if low is not None:
        if market is not None and mid is not None:
            average = (market + low + mid) / 3
            if low < average * .85:
                low = average * .85
        price = low * condition_map[condition.lower()]

        if direct is not None:
            if direct > price:
                if condition.lower() != 'moderately played':
                    if direct > price * 1.15:
                        price = price * 1.15
                    else:
                        price = price

        if price < .25:
            price = .25

        if market is not None:
            if market > price * 1.5:
                price = price * 1.20

        if price >= 2. and price <= 2.25:
            price = 1.99

        return price

    else:
        return None


def price_algorithm(condition, market, direct=None, mid=None, low=None):
    new_price = market
    low_price = low
    mid_price = mid
    direct_price = direct

    # Use Pricing Algorithm to determine updated price to list card at
    if new_price is not None:
        if mid_price is not None and low_price is not None:
            average = (new_price + low_price + mid_price) / 3
            if new_price < average * .9:
                new_price = average * .9

        if new_price > 1.99:
            if low_price is not None:
                if new_price < low_price:
                    new_price = low_price
                    if mid_price is not None:
                        if new_price * 1.3 < mid_price:
                            new_price = mid_price

                elif new_price > low_price * 1.15:
                    if mid_price is not None:
                        new_price = mid_price * .9
                    else:
                        new_price = new_price * .9
                else:
                    pass
            else:
                pass
        else:
            if low_price is not None:
                if new_price < low_price:
                    new_price = low_price
                    if mid_price is not None:
                        if low_price * 3 < mid_price:
                            new_price = mid_price
                        elif low_price * 1.3 < mid_price:
                            new_price = mid_price

                else:
                    if mid_price is not None:
                        if low_price * 3 < mid_price:
                            new_price = mid_price
                            if market * 1.4 < mid_price:
                                new_price = mid_price
                            new_price = new_price * .9

                        elif low_price * 1.3 < mid_price:
                            new_price = mid_price
                            if market * 1.4 < mid_price:
                                new_price = mid_price
                            new_price = new_price * .9

            else:
                pass
        if direct_price is not None:
            if direct_price > new_price:
                if condition.lower() != 'moderately played':
                    if direct_price > new_price * 1.15:
                        new_price = new_price * 1.15
                    else:
                        new_price = direct_price

    else:
        if mid_price is not None:
            new_price = mid_price
        else:
            if low_price is not None:
                new_price = low_price
            else:
                new_price = None

    if new_price is not None:
        if 'moderately played' in condition.lower():
            new_price = new_price * .85
        elif 'heavily played' in condition.lower():
            new_price = new_price * .75
        elif 'damaged' in condition.lower():
            new_price = new_price * .50

        if new_price < .25:
            new_price = .25

        if new_price >= 2. and new_price <= 2.25:
            new_price = 1.99

    return new_price


def buylist_algorithm(condition, market, low=None, mid=None, market_buylist=None, percentage=60):
    new_price = market
    low_price = low
    mid_price = mid

    if new_price is not None:
        if new_price > 1.99:
            if low_price is not None:
                if new_price < low_price:
                    new_price = low_price

                elif new_price > low_price * 1.15:
                    if mid_price is not None:

                        new_price = mid_price * .75
                    else:
                        new_price = new_price * .75
                else:
                    pass
            else:
                pass
        else:
            if low_price is not None:
                if new_price < low_price:
                    new_price = low_price
                    if mid_price is not None:
                        if low_price * 3 < mid_price:
                            new_price = mid_price
            else:
                pass

    else:
        if mid_price is not None:
            new_price = mid_price
        else:
            if low_price is not None:
                new_price = low_price
            else:
                new_price = None

    if market_buylist is not None:
        if market_buylist < new_price * (percentage + .05):
            new_price = market_buylist * 1.05
        else:
            new_price = new_price * percentage / 100

    else:
        new_price = new_price * percentage / 100

    if new_price is not None:
        if 'moderately played' in condition.lower().strip():
            new_price = new_price * .9

    return new_price


def sku_price_algorithm(language, expansion, category, printing, condition, sku, market, direct=None, low=None):
    condition = condition.replace('-', '').strip()
    new_price = market
    low_price = low
    direct_price = direct

    if new_price is None and low_price is None or language != 'English':
        condition_dict = {
            'near mint': 1,
            'lightly played': 1,
            'moderately played': .85,
            'heavily played': .65,
            'damaged': .5,

        }

        condition_price = 'near mint'

        if 'lightly played' in condition.lower():
            condition_price = condition_dict['lightly played']

        elif 'moderately played' in condition.lower():
            condition_price = condition_dict['moderately played']

        elif 'heavily played' in condition.lower():
            condition_price = condition_dict['heavily played']

        elif 'damaged' in condition.lower():
            condition_price = condition_dict['damaged']

        product_id = api.card_info_by_sku(sku)['results'][0]['productId']
        market_data = api.get_market_price(str(product_id))['results']

        if category != "Magic" and category != 'Magic the Gathering':
            count = 0
            try:
                while True:
                    if market_data[count]['subTypeName'].lower() in condition.lower():
                        market_data = market_data[count]
                        break
                    count += 1
            except IndexError:
                market_data = []

        else:
            check_foil = {
                True: 'Foil',
                False: "Normal",
            }

            foil = check_foil[printing]
            if market_data[0]['subTypeName'] == foil:
                market_data = market_data[0]
            else:
                market_data = market_data[1]

        if market_data:
            market_price = market_data['marketPrice']
            low_market_price = market_data['lowPrice']
            direct_market_price = market_data['lowPrice']
            mid_market_price = market_data['midPrice']
            print(f'Market data for foreign cards{market_price}, {low_market_price}, {mid_market_price}')

            if language != 'English':
                print('Definitely Foreign')
                upload_price = price_foreign(
                    condition=condition,
                    language=language,
                    expansion=expansion,
                    low=low_market_price,
                    mid=mid_market_price,
                    market=market_price,
                )
                print(upload_price)
                return upload_price

            else:
                if market_price is not None:
                    if low_market_price is not None:
                        if low_market_price > market_price:
                            market_price = low_market_price
                    if direct_market_price is not None:
                        if direct_market_price > market_price:
                            if direct_market_price > market_price * 1.15:
                                market_price = market_price * 1.15
                            else:
                                market_price = direct_market_price

                else:
                    market_price = low_market_price

                if market_price is not None:
                    market_price = market_price * condition_price

                    if market_price < .25:
                        market_price = .25

                    if market_price >= 2. and market_price < 2.25:
                        market_price = 1.99

                    return market_price

    else:

        # Use Pricing Algorithm to determine updated price to list card at
        if new_price is not None:

            if new_price > 1.99:

                if low_price is not None:

                    if new_price < low_price:
                        new_price = low_price

                    elif new_price > low_price * 1.15:
                            new_price = new_price * .9
                    else:
                        pass
                else:
                    pass
            else:
                pass

            if low_price is not None:
                if new_price < low_price:
                    new_price = low_price

                else:
                    pass

            if direct_price is not None:
                if direct_price > new_price:
                    if direct_price > new_price * 1.15:
                        new_price = new_price * 1.15
                    else:
                        new_price = direct_price

        else:

            if low_price is not None:
                new_price = low_price
            else:
                new_price = 0

        if new_price < .25:
            new_price = .25

        if new_price >= 2. and new_price <= 2.25:
            new_price = 1.99

        return new_price


