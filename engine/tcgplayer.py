from decimal import Decimal
from math import ceil
import requests
from .tcg_manifest import Manifest
from .models import UpdatedInventory, CaseCards, Product
from tcg.price_alogrithm import price_algorithm, buylist_algorithm
from buylist.models import Buying
from .tcgplayer_api import TcgPlayerApi
from.tcg_credentials import Credentials

tcg = TcgPlayerApi('first')
store_key = Credentials.store_keys
manifest = Manifest()


def create_tcg_buylist(sku):
    product_id = tcg.card_info_by_sku(sku)['results'][0]['productId']
    price_data = tcg.get_prices(str(product_id))['results']
    price = 0
    market_price = 0
    low_price = 0
    mid_price = 0
    for each in price_data:
        if each['subTypeName'] == 'Normal':
            market_price = each['marketPrice']
            low_price = each['lowPrice']
            mid_price = each['midPrice']

        price = market_price
        if price > 0 and price >= 2 and price < low_price:
            price = low_price

        elif price > 0 and price < 2 and mid_price >= low_price * 2:
            price = mid_price * 8

        elif price > 0 and price >= low_price * 1.20:
            price = market_price * .8



    if price > 0:
        updated_price = price * .65
        product_conditions = tcg.get_card_info(product_id)['results'][0]['productConditions']
        for each_card in product_conditions:
            if each_card['isFoil'] == False:
                if each_card['name'] == 'Near Mint':
                    condition_id = each_card['productConditionId']
                    tcg.create_buylist_item(condition_id, updated_price, _json=True)
                if each_card['name'] == 'Lightly Played':
                    condition_id = each_card['productConditionId']
                    tcg.create_buylist_item(condition_id, updated_price, _json=True)
                if each_card['name'] == 'Moderately Played':
                    condition_id = each_card['productConditionId']
                    mp_price = updated_price * .90
                    tcg.create_buylist_item(condition_id, mp_price, _json=True)
        updated_price = format(updated_price, '.2f')
        return updated_price
    else:
        return "No Market Price Data or Foil"


def price_for_rarity(rarity, price):
    print(rarity, price)
    if price < 1:
        if rarity == 'Rare' and price > .0:
            price = .99
        elif rarity == 'Mythic Rare' and price > .0:
            price = .99
        elif rarity == 'Uncommon' and price < .50 and price > .0:
            price = .49
        elif rarity == 'Common' and price < .25 and price > .0:
            price = .25
        elif rarity == 'Common' and price < .50 and price > .25:
            price = .49
        return Decimal(price)
    else:
        new_price = Decimal(ceil(price) - .01)
        return new_price


def card_price(*product_id):
    results = tcg.get_prices(product_id)['results']

    price_dict = {str(i["productId"]): {
        "market_price": Decimal(i["marketPrice"]),
        "low_price": Decimal(i["lowPrice"]) }
        for i in results if  i["marketPrice"] != None and i["lowPrice"] != None}
    for each in price_dict.keys():
        if price_dict[each]["market_price"] < price_dict[each]["low_price"]:
            price_dict[each]["market_price"] = price_dict[each]["low_price"]
    return price_dict


def card_price_single(product_id, rarity):

    if product_id !=  None and product_id != 'None':
        r = tcg.get_prices(product_id)
        market_price = r['results'][0]['marketPrice']
        low_price = r['results'][0]['lowPrice']
        if r['results'][0]['subTypeName'] == 'Foil':
            market_price = r['results'][1]['marketPrice']
            low_price = r['results'][1]['lowPrice']
        count = 1
        try:
            if market_price == None:
                market_price = r['results'][count + 1]['marketPrice']
            if low_price == None:
                low_price = r['results'][count + 1]['lowPrice']
        except IndexError:
            market_price = r['results'][1]['marketPrice']
            low_price = r['results'][1]['lowPrice']
        try:
            if market_price < low_price:
                market_price = low_price
        except TypeError:
            if market_price is None:
                market_price = 0.
            if low_price is None:
                low_price = 0.
            if market_price < low_price:
                market_price = low_price
        if market_price != 0 and market_price > .99:
            market_price = ceil(market_price) - .01
        if rarity == 'Rare' and market_price < 1. and market_price > .0:
            market_price = .99
        elif rarity == 'Mythic Rare' and market_price < 1. and market_price > .0:
            market_price = .99
        elif rarity == 'Uncommon' and market_price < .50 and market_price > .0:
            market_price = .49
        elif rarity == 'Common' and market_price < .25 and market_price > .0:
            market_price = .25
        elif rarity == 'Common' and market_price < .50 and market_price > .25:
            market_price = .49
        return Decimal(market_price)



    else:
        return 0.


def search_inventory(product_id):
    r = tcg.search_inventory(product_id)
    return r['results'][0]['totalQuantity']


def full_order():
    from .models import Orders
    from .tcg_manifest import Manifest
    def get_orders(order_status, limit, offset):
        params = {
            "orderStatusIds": order_status,
            "limit": limit,
            "offset": offset,
        }
        url = "http://api.tcgplayer.com/stores/{}/orders".format(store_key)
        r = requests.get(url, headers=headers, params=params)
        return r.json()
    def get_order_details(order_numbers):
        url = "http://api.tcgplayer.com/stores/{0}/orders/{1}".format(store_key, order_numbers)
        r = requests.get(url, headers=headers)
        return r.json()
    def get_order_items(order_numbers):
        url = "http://api.tcgplayer.com/stores/{0}/orders/{1}/items".format(store_key, order_numbers)
        r = requests.get(url, headers=headers)
        return r.json()['results']
    def card_info_by_sku(sku_id):
        url_price = 'http://api.tcgplayer.com/catalog/skus/{}'.format(sku_id)
        r = requests.get(url_price, headers=headers)
        return r.json()['results'][0]
    def get_card_info(product_id):
        url = "http://api.tcgplayer.com/catalog/products/{}".format(product_id)
        r = requests.get(url, headers=headers
                         )
        return r.json()['results'][0]


    Manifest = Manifest()
    order_marker = 1
    full_db = Orders.objects.only('order_number').values_list('order_number', flat=True)
    db = {
        1: Orders.objects.filter(order_status_type='Processing').only('order_number'),
        2: Orders.objects.filter(order_status_type='Ready to Ship').only('order_number'),

    }
    database = {
        1: db[1].values_list('order_number', flat=True),
        2: db[2].values_list('order_number', flat=True),
    }


    while order_marker <= 2:
        number_of_orders = get_orders(order_marker, 1, 0)['totalItems']
        offset = 0
        orders = []
        while True:
            if number_of_orders < 0:
                break
            partial_orders = get_orders(order_marker, 100, offset)['results']
            for each in partial_orders:
                orders.append(each)
            number_of_orders -= 100
            offset += 100

        orders_to_delete = [i for i in database[order_marker] if i not in orders] # Create list of orders that are no longer processing | Ready to
        if len(orders_to_delete) > 0:
            db[order_marker].filter(order_number__in=orders_to_delete).delete()
        count = 0
        while count < len(orders):
            try:
                if orders[count] not in full_db:
                    results = get_order_details(orders[count])['results'][0]
                    order_status_type = Manifest.order_status(results['orderStatusTypeId'])
                    if order_status_type == 'Processing' or order_status_type == 'Ready to Ship':
                        address = results['customer']['shippingAddress']
                        shipping_name = address['firstName'] + ' ' + address['lastName']
                        shipping_address = address['address1'] + address['address2'] +'\n'+ address['city'] +', '+ address['state']+\
                           ' ' + address['postalCode'] + ' ' + address['country']
                        order_number = results['orderNumber']
                        order_details  = get_order_items(order_number)
                        all_cards = []
                        for each in order_details:
                            sku = card_info_by_sku(each['skuId'])
                            card_details = get_card_info(sku['productId'])
                            name = "{} | {}".format( Manifest.language(sku['languageId']) , card_details['productName'])
                            expansion = Manifest.expansion(card_details['groupId'])
                            condition = Manifest.condition(sku['conditionId'])
                            card = "{} ({}) | {} | ${} | Qty: {} - ".format(name, expansion, condition, each['price'], each['quantity'],)
                            all_cards.append(card)
                        all_cards = "\n".join(all_cards)
                        #order_channel_type = results['orderChannelTypeId']
                        order_delivery_type = Manifest.delivery_type(results['orderDeliveryTypeId'])
                        #direct_order = results['isDirect']
                        #international = results['isInternational']
                        order_date = results['orderedOn']
                        #modified = results['modifiedOn']
                        token = results['customer']['token']
                        name = str(results['customer']['firstName']) + ' ' + str(results['customer']['lastName'])
                        #email = results['customer']['email']
                        #product_value = format(Decimal(results['orderValue']['product']), '.2f')
                        #shipping_paid = format(Decimal(results['orderValue']['shipping']), '.2f')
                        #tax = format(Decimal(results['orderValue']['tax']), '.2f')
                        #gross_earnings = format(Decimal(results['orderValue']['gross']), '.2f')
                       # fees = format(Decimal(results['orderValue']['fees']), '.2f')
                        net_profit = format(Decimal(results['orderValue']['net']), '.2f')
                        db_entry = Orders(
                            shipping_name=shipping_name, shipping_address=shipping_address, order_number=order_number,
                            order_details=all_cards, order_status_type=order_status_type, order_delivery_type=order_delivery_type,
                            order_date=order_date, token=token, name=name,
                            net_profit=net_profit)
                        db_entry.save()
                        count += 1
                    else:
                        count += 1
                else:
                    count += 1
            except IndexError as e:
                print(e)
                count += 1
        order_marker += 1


def render_buylist():
    from buylist.models import Buying, SkuLight
    from .models import Product
    from django.core.exceptions import ObjectDoesNotExist

    buylist_size = tcg.get_buylist_cards(1,0)['totalItems']
    offset = 0
    buylist = Buying.objects
    sku = SkuLight.objects.all()
    product = Product.objects.only('image_url')
    buylist_cards = []
    entries = {}

    while buylist_size > 0:
        data = tcg.get_buylist_cards(100, offset)['results']
        for each in data:
            buylist_cards.append(each)
        offset += 100
        buylist_size -= 100

    for i in buylist_cards:
        id = str(i["skuId"])
        try:
            if buylist.filter(sku=id).exists():
                pass

            else:
                if i['price'] != None:
                    if sku.filter(sku=id).exists():
                        s = sku.get(sku=id)
                        entries[id] = {
                            "name": s.name,
                            "expansion": s.expansion,
                            "price": round((float(i['price']) * .95) * 2) / 2,
                            "image": "no_image.png"
                        }
                        try:
                            entries[id]['image'] = product.filter(set_name=entries[id]['expansion']).get(
                                name=entries[id]['name']).image_url
                        except ObjectDoesNotExist:
                            pass
                    else:
                        print("No Sku Found for ", id)
        except ObjectDoesNotExist:
            pass


    objs = (Buying(name=entries[i]['name'],
                   sku=i,
                   set_name=entries[i]['expansion'],
                   price=entries[i]['price'],
                   image=entries[i]['image'],
                   ) for i in entries.keys())
    buylist.bulk_create(objs)


def update_buylist():
    from buylist.models import Buying as B

    buylist = B.objects.all()
    for each in buylist:
        try:
            price = round((float(tcg.get_prices(tcg.card_info_by_sku(each.sku)['results'][0]['productId'])['results'][0]['marketPrice']) *.60) * 2) / 2
            each.price = price
            each.save()
        except TypeError as e:
            print("{} - Error for {}-{}".format(e, each.name, each.set_name))


def update_inventory():
    from datetime import date
    tcg_api = TcgPlayerApi()

    def get_inventory(group_id, limit, offset):
        url = "http://api.tcgplayer.com/stores/{}/inventory/products".format(store_key)
        params = {
            'groupId': group_id,
            'limit': limit,
            'offset': offset
        }
        response = requests.get(url, params=params, headers=headers)
        return response.json()

    def card_price(*args):
        url = 'http://api.tcgplayer.com/V1.9.0/pricing/product/{}'.format(*args)
        r = requests.get(url, headers=headers)
        return r.json()

    tcg = Manifest()
    weekday = date.today().strftime('%A')
    group_id_list = tcg.group_id_by_day(weekday)
    group_id_count = 0

    # Delete Previous records for day before creating new ones
    old_records = UpdatedInventory.objects.filter(group_id__in=group_id_list)
    old_records.delete()

    # Loop through each mtg set in the online inventory
    while group_id_count < len(group_id_list):
        offset_count = 0
        total = get_inventory(group_id_list[group_id_count], 1, 0)['totalItems']

        # Loop through every 100 items from inventory until var total is reached
        while total > 0:
            foil_prices = {}
            non_foil_prices = {}
            inventory = get_inventory(group_id_list[group_id_count], 100, offset_count)['results']

            # Get Product ID for each card in our inventory (FOil or Non-foil)
            product_ids = [str(i['productId']) for i in inventory]

            # Format to string with comma to mass get_price for product_Ids
            joined_product_ids = ','.join(product_ids)
            card_price_results = card_price(joined_product_ids)['results']

            # Loop through returned card_price_results for card prices and create 2 dictionaries
            # One Dict will have all Normal SKUS and prices. The other will have all foil SKUS
            for each in card_price_results:
                if each['subTypeName'] == 'Normal':
                    non_foil_prices[each['productId']] = {
                        'lowPrice': each['lowPrice'],
                        'marketPrice': each['marketPrice'],
                        'midPrice': each['midPrice'],
                        'directLowPrice': each['directLowPrice'],
                    }
                elif each['subTypeName'] == 'Foil':
                    foil_prices[each['productId']] = {
                        'lowPrice': each['lowPrice'],
                        'marketPrice': each['marketPrice'],
                        'midPrice': each['midPrice'],
                        'directLowPrice': each['directLowPrice'],
                    }

            # Create variables for each item in inventory > This Set > SKU, ProductId etc for each card.
            for each_product in inventory:
                for each_sku in each_product['skus']:
                    condition = each_sku['condition']['name']
                    if condition != 'Unopened':
                        language = each_sku['language']['name']
                        if language == 'English':
                            name = each_product['name']
                            expansion = each_product['group']
                            sku = each_sku['skuId']
                            product_id = each_product['productId']

                            foil = each_sku['foil']
                            previous_price = each_sku['price']

                            # Get dictionary of all prices for foil cards or non-foil cards
                            if foil is False:
                                all_prices = non_foil_prices[product_id]
                            elif foil is True:
                                all_prices = foil_prices[product_id]

                            market = all_prices['marketPrice']
                            low_price = all_prices['lowPrice']
                            mid_price = all_prices['midPrice']
                            direct_price = all_prices['directLowPrice']

                            # Use Pricing Algorithm to determine updated price to list card at
                            upload_price = price_algorithm(condition=condition, market=market, direct=direct_price, low=low_price, mid=mid_price)

                            # Create Exceptions in pricing for certain sets
                            exceptions = ['portal three kingdoms', 'portal second age', 'portal', 'starter 99', 'starter 2000']
                            if expansion.lower().strip() in exceptions:
                                if low_price is not None:
                                    upload_price = low_price
                                else:
                                    pass

                            # Changes pricing variable to Zero if None to display on record page
                            if low_price is None:
                                low_price = 0
                            if mid_price is None:
                                mid_price = 0
                            if market is None:
                                market = 0
                            if direct_price is None:
                                direct_price = 0

                            # Add record of Item to Database
                            record = UpdatedInventory(
                                name=name,
                                expansion=expansion,
                                condition=condition,
                                is_foil=foil,
                                previous_price=previous_price,
                                updated_price=upload_price,
                                market_price=market,
                                low_price=low_price,
                                mid_price=mid_price,
                                direct_price=direct_price,
                                sku=sku,
                                group_id=group_id_list[group_id_count]

                            )
                            record.save()

                            # Update Live TCGPlayer Inventory if there is a valid change in price
                            if upload_price != previous_price:
                                tcg_api.update_sku_price(sku, upload_price, _json=True)

            total -= 100
            offset_count += 100
        group_id_count += 1


def update_case():
    import csv
    from buylist.models import SkuLight

    csv_reader = csv.DictReader(open('Case Cards.csv'))
    error = open('error.txt', 'w')
    sku_light = SkuLight.objects.all()
    for each in csv_reader:
        results = sku_light.filter(name=each['Name'].strip())
        if not results.exists():
            error.write(each['Name']+'\n')
        else:
            for result in results:
                product_id = tcg.card_info_by_sku(result.sku)['results'][0]['productId']

                case_obj = CaseCards(
                    name = result.name,
                    expansion = result.expansion,
                    sku = result.sku,
                    product_id = product_id,
                )

                case_obj.save()


def update_case_price():
    from .models import CaseCards
    from tcg.price_alogrithm import price_algorithm
    from math import ceil

    def card_price(*args):
        url = 'http://api.tcgplayer.com/V1.9.0/pricing/product/{}'.format(*args)
        r = requests.get(url, headers=headers)
        return r.json()
    cards = CaseCards.objects.all()
    update_count = 0

    to_reprice = {i.product_id: {'name': i.name, 'price': i.price} for i in cards}
    product_ids_list = [i for i in to_reprice.keys()]
    start = 0
    stop = 100
    while stop < 801:
        try:
            if stop > 700:
                stop = len(product_ids_list)
            product_ids = ','.join(product_ids_list[start:stop])

            prices = card_price(product_ids)['results']
            for each in prices:
                if each['subTypeName'] == 'Normal':
                    new_price = price_algorithm(condition='Near Mint', market=each['marketPrice'], low=each['lowPrice'], mid=each['midPrice'])
                    print(new_price)
                    new_price = ceil(new_price)- .01
                    to_reprice[str(each['productId'])]['price'] = new_price


            y = CaseCards.objects.filter(product_id__in=product_ids_list)

            for each in y:
                each.Update_status = ''


                updated_price = float(to_reprice[each.product_id]['price'])
                db_price = float(each.price)


                if db_price <= 20. and db_price * 1.10 < updated_price or db_price * .9 > updated_price:
                    each.price = to_reprice[each.product_id]['price']
                    each.Update_status = 'Update Needed'
                    update_count += 1

                elif db_price > 20. and  db_price < 60. and  db_price * 1.04 < updated_price or db_price * .96 > updated_price:
                    each.price = to_reprice[each.product_id]['price']
                    each.Update_status = 'Update Needed'
                    update_count += 1

                elif db_price > 60. and  db_price * 1.02 < updated_price or db_price * .98 > updated_price:
                    each.price = to_reprice[each.product_id]['price']
                    each.Update_status = 'Update Needed'
                    update_count += 1

                each.save()

        except IndexError as e:
            print(e)
            pass

        start += 100
        stop += 100


    # Send message to facebook group chat to update prices for cards
    if update_count > 0:
        def send():
            from customer.facebook import FacebookBot
            facebook_bot = FacebookBot()
            facebook_bot.send_message(
                "There are {} Case Cards that need to be updated".format(update_count)

            )

        send()



def buylist_hub():
    def card_price(*args):
        url = 'http://api.tcgplayer.com/V1.9.0/pricing/product/{}'.format(*args)
        r = requests.get(url, headers=headers)
        return r.json()

    offset = 0
    buylist = Buying.objects
    tcg = TcgPlayerApi()
    manifest = Manifest()


    # Loop through tcgplayer buylist inventory and generate a list with every sku
    buylist_cards = []
    buylist_size = tcg.get_buylist_cards(1, 0)['totalItems']

    while buylist_size > 0:
        data = tcg.get_buylist_cards(100, offset)['results']
        for each in data:
            buylist_cards.append(each)
        offset += 100
        buylist_size -= 100


    # Check if buylist item is already in DB by checking for SKU > Create new list of ready to add buylist cards
    db_cards = buylist.values_list('sku', flat=True)
    buylist_results = [i for i in buylist_cards if i['price'] != None and str(i['skuId']) not in db_cards]


    # Create variables for all buylist info using tcgplayer API
    if len(buylist_results) > 0:
        for i in buylist_results:
            sku = str(i["skuId"])
            sku_info = tcg.card_info_by_sku(sku)['results'][0]
            product_id = str(sku_info['productId'])
            condition = manifest.condition(sku_info['conditionId'])
            product_info = tcg.get_card_info(product_id)['results'][0]
            image = product_info['image']


            # Save Buylist Items to Buylist Hub Database
            created_buylist = Buying(
                name=product_info['productName'],
                set_name=manifest.expansion(product_info['groupId']),
                price=i['price'],
                image=image,
                product_id=product_id,
                condition=condition,
                sku=sku
            )
            created_buylist.save()


    # format product ids from each in Db and call pricing algorithm to get list of updated market prices and store in dictionary
    product_id_list = buylist.values_list('product_id', flat=True)
    start = 0
    stop = 100
    while stop < len(product_id_list):
        if abs(len(product_id_list) - stop) < 100:
            stop = len(product_id_list)
        product_id_string = ','.join(product_id_list[start:stop])

        updated_prices = card_price(product_id_string)['results']
        price_dict = {}
        for each in updated_prices:
            if each['subTypeName'] == 'Normal':
                market = each['marketPrice']
                low = each['lowPrice']
                product_id = each['productId']
                price_dict[str(product_id)] = {
                    'marketPrice': market,
                    'lowPrice': low,
                }


        # Loop through Buylist Db
        for each in buylist.filter(product_id__in=product_id_list[start:stop]):


            #Get tcgplayer market buylist (High) for each card
            try:
                market_buylist_high = tcg.get_tcg_public_buylist(each.sku)['results'][0]['prices']['high']
            except Exception as e:
                print(e)
                market_buylist_high = None


            # Run buylist pricing algorithm on each card from price_dict > Save those results to the database
            new_price = buylist_algorithm(condition=each.condition, market=price_dict[str(each.product_id)]['marketPrice'], low=price_dict[str(each.product_id)]['lowPrice'], market_buylist=market_buylist_high)

            each.price = new_price
            each.save()

            tcg.update_buylist_item_price(each.sku, each.price, _data=True)
            tcg.update_buylist_item_quantity(each.sku, 20, _data=True)


        start += 100
        stop += 100


def new_set(group_id):
    total = tcg.get_set_data(group_id)['totalItems']
    offset = 0
    while total > 0:
        data = tcg.get_set_data(group_id, offset=offset, _bool_=True)['results']
        print(len(data))
        for each in data:
            product_id = each['productId']
            product_name = each['productName']
            image = each['image']
            site = 'database'
            rarity = each['extendedData'][0]['value']
            set_name = manifest.expansion(int(group_id))

            new_products = Product(
                name=product_name,
                tcg_player_id=product_id,
                image_url=image,
                set_name=set_name,
                rarity=rarity,
                site=site,

            )
            new_products.save()

        total -= 100
        offset += 100

















