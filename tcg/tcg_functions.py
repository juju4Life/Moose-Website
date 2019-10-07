from my_customs.functions import integers_from_string, float_from_string


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


def moose_price_algorithm(seller_data):

    if seller_data:
        updated_price = 0

        # Average price of first 5 listings, excluding First and Moose
        average_price = sum([i['price'] for i in seller_data]) / len(seller_data)

        if len(seller_data) >= 2:
            count = 0

            while count < len(seller_data):
                updated_price = seller_data[count]['price'] - .01
                if updated_price < average_price / 1.10:
                    count += 1
                else:
                    break

            if count == len(seller_data) + 1:
                updated_price = average_price / 1.10

        else:
            updated_price = seller_data[0]['price'] - .01

        for seller in seller_data[1:]:
            if seller['gold'] is True:
                if updated_price < seller['price'] / 1.10:
                    updated_price = seller['price'] - .01

                break

        if updated_price < seller_data[0]['price']:
            updated_price = seller_data[0]['price'] - .01

        if updated_price < 5 and updated_price > 4.21 and updated_price + .78 > 4.99:
            updated_price = 5

        return updated_price


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


def get_product_seller_info(d):
    check = d.find('span', {'class': 'seller__sales'})
    if check is not None:

        seller_total_sales = integers_from_string(d.find('span', {'class': 'seller__sales'}).text)

        # seller_feedback = d.find('span', {'class': 'seller__feedback-rating'}).text
        # function extracts all floating points from string.
        price = float_from_string(d.find('span', {'class': 'product-listing__price'}).text)
        total_price = None

        # Fail Safe in the case where html is changed and no real value is extracted
        if price is not None and price is not 0:
            shipping = float_from_string(d.find('span', {'class': 'product-listing__shipping'}).text.strip())

            # 25 would be extracted from shipping text that state "Free shipping over 25". We make this result 0 and
            # handle additional shipping costs using defaults
            if shipping == 25.:
                shipping = 0

            # Default shipping added to cards under five.
            if price >= 5:
                total_price = price + shipping
            else:
                total_price = price

        return price, total_price, seller_total_sales


def set_map(expansion):

    mapped = {
        "Ravnica: City of Guilds": 'Ravnica',
        "Magic 2010 (2010)": "Magic 2010",
        "Magic 2011 (2011)": "Magic 2011",
        "Magic 2012 (2012)": "Magic 2012",
        "Magic 2013 (2013)": "Magic 2013",
        "Magic 2014 (2014)": "Magic 2014",
        "Magic 2015 (2015)": "Magic 2015",
        "10th Edition": "Tenth Edition",
        "9th Edition": "Ninth Edition",
        "8th Edition": "Eighth Edition",
        "7th Edition": "Seventh Edition",
        "6th Edition": "Sixth Edition",
        "5th Edition": "Fifth Edition",
        "4th Edition": "Fourth Edition",
        "Revised Edition": "Revised",
        "Battle Royale Box Set": "Battle Royale",
        "Conspiracy: Take the Crown": "Conspiracy 2: Take the Crown",

    }











