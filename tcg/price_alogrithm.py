


def price_algorithm(condition ,market, direct=None, mid=None, low=None):
    new_price = market
    low_price = low
    mid_price = mid
    direct_price = direct

    # Use Pricing Algorithm to determine updated price to list card at
    if new_price != None:
        if new_price > 1.99:
            if low_price != None:
                if new_price < low_price:
                    new_price = low_price
                    if mid_price != None:
                        if new_price * 1.3 < mid_price:
                            new_price = mid_price
                    
                elif new_price > low_price * 1.15:
                    if mid_price != None:
                        new_price = mid_price * .9
                    else:
                        new_price = new_price * .9
                else:
                    pass
            else:
                pass
        else:
            if low_price != None:
                if new_price < low_price:
                    new_price = low_price
                    if mid_price != None:
                        if low_price * 3 < mid_price:
                            new_price = mid_price
                        elif low_price * 1.3 < mid_price:
                            new_price = mid_price
                else:
                    if mid_price != None:
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
        if direct_price != None:
            if direct_price > new_price:
                if condition.lower() != 'moderately played':
                    if direct_price > new_price * 1.15:
                        new_price = new_price * 1.15
                    else:
                        new_price = direct_price
                    
                    
    else:
        if mid_price != None:
            new_price = mid_price
        else:
            if low_price != None:
                new_price = low_price
            else:
                new_price = None
    

    if new_price != None:
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

    if new_price != None:
        if new_price > 1.99:
            if low_price != None:
                if new_price < low_price:
                    new_price = low_price

                elif new_price > low_price * 1.15:
                    if mid_price != None:

                        new_price = mid_price * .75
                    else:
                        new_price = new_price * .75
                else:
                    pass
            else:
                pass
        else:
            if low_price != None:
                if new_price < low_price:
                    new_price = low_price
                    if mid_price != None:
                        if low_price * 3 < mid_price:
                            new_price = mid_price
            else:
                pass


    else:
        if mid_price != None:
            new_price = mid_price
        else:
            if low_price != None:
                new_price = low_price
            else:
                new_price = None

    if market_buylist != None:
        if market_buylist < new_price * (percentage + .05):
            new_price = market_buylist * 1.05
        else:
            new_price = new_price * percentage / 100

    else:
        new_price = new_price * percentage / 100

    if new_price != None:
        if 'moderately played' in condition.lower().strip():
            new_price = new_price * .9

    return new_price



