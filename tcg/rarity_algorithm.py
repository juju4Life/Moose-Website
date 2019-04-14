from math import ceil


def rarity_round(rarity, price):
    if rarity == 'C':
        if price < 0.25:
            price = 0.25
        elif price > 0.25 and price < 0.49:
            price = 0.49

        else:
            price = ceil(price) - 0.01

    elif rarity == 'U':
        if price < 0.49:
            price = 0.49

        else:
            price = ceil(price) - 0.01

    else:
        price = ceil(price) - 0.01

    return price


