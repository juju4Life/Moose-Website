from engine.models import MTG
from django.db.models import Q
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from engine.models import MTGDatabase
import csv
from engine.tcgplayer_api import TcgPlayerApi


api = TcgPlayerApi("moose")


def q():
    data = MTG.objects.filter(
        Q(normal_clean_stock__gt=0) | Q(normal_played_stock__gt=0) | Q(normal_heavily_played_stock__gt=0) |
        Q(foil_clean_stock__gt=0) | Q(foil_played_stock__gt=0) | Q(foil_heavily_played_stock__gt=0)
    )

    with open('inventory.csv', 'w', newline='') as f:
        writer = csv.writer(f)

        headers = ['Expansion', 'Name', 'Clean', 'Played', 'HP', 'Foil Clean', 'Foil Played', 'Foil HP', ]

        writer.writerow(headers)

        ready = [
            [
                i.expansion, i.name, i.normal_clean_stock, i.normal_played_stock, i.normal_heavily_played_stock,
                i.foil_clean_stock, i.foil_played_stock, i.foil_heavily_played_stock,
            ] for i in data

        ]

        writer.writerows(ready)


def up():
    with open('web.csv', newline='') as f:
        cards = csv.reader(f)
        next(cards)
        for card in cards:
            print(card)


def adjust():
    with open('new_cards.csv', 'w', newline='') as f:
        with open('web.csv', 'r', newline='') as old:
            cards = csv.reader(old)
            next(cards)
            writer = csv.writer(f)
            new_header = ['TCGplayer Id', 'Product Line', 'Set Name', 'Product Name', 'Title', 'Number', 'Rarity', 'Condition', 'TCG Market Price',
                          'TCG Direct Low',
                        'TCG Low Price With Shipping', 'TCG Low Price', 'Total Quantity', 'Add to Quantity', 'TCG Marketplace Price', 'Photo URL', ]
            writer.writerow(new_header)

            rows = list()

            def create_row(condition, quantity, product_expansion, product_name, sku):
                rows.append(
                    [sku, 'Magic', product_expansion, product_name, '', '', '', condition, '', '', '', '', '', quantity, '', '']
                )

            def get_obj(query, condition, printing):
                try:
                    sku = query.filter(condition=condition).get(printing=printing).sku
                    return sku
                except ObjectDoesNotExist:
                    return None

            with transaction.atomic():
                database = MTGDatabase.objects.filter(language='English')

                for index, card in enumerate(cards):
                    print(index)
                    expansion = card[0]
                    name = card[1]
                    clean = int(card[2])
                    played = int(card[3])
                    hp = int(card[4])
                    foil_clean = int(card[5])
                    foil_played = int(card[6])
                    foil_hp = int(card[7])

                    data_query = database.filter(expansion=expansion, name=name)
                    if clean > 0:
                        sku = get_obj(data_query, 'Clean', 'Normal')
                        if sku:
                            create_row('Lightly Played', clean, expansion, name, sku)

                    if played > 0:
                        sku = get_obj(data_query, 'Played', 'Normal')

                        if sku:
                            create_row('Moderately Played', played, expansion, name, sku)

                    if hp > 0:
                        sku = get_obj(data_query, 'Heavily Played', 'Normal')
                        if sku:
                            create_row('Heavily Played', hp, expansion, name, sku)

                    if foil_clean > 0:
                        sku = get_obj(data_query, 'Clean', 'Foil')
                        if sku:
                            create_row('Lightly Played Foil', foil_clean, expansion, name, sku)

                    if foil_played > 0:
                        sku = get_obj(data_query, 'Played', 'Foil')
                        if sku:
                            create_row('Moderately Played Foil', foil_played, expansion, name, sku)

                    if foil_hp > 0:
                        sku = get_obj(data_query, 'Heavily Played', 'Foil')
                        if sku:
                            create_row('Heavily Played Foil', foil_hp, expansion, name, sku)

            writer.writerows(rows)


def price():
    with open('new_cards.csv', 'r', newline='') as not_priced:
        with open('priced_inventory.csv', 'w', newline='') as priced:
            rows = list()

            def create_row(condition, quantity, product_expansion, product_name, sku, low, market, up_price):
                rows.append(
                    [sku, 'Magic', product_expansion, product_name, '', '', '', condition, market, '', low, '', '', quantity, up_price, '']
                )
            writer = csv.writer(priced)
            header = ['TCGplayer Id', 'Product Line', 'Set Name', 'Product Name', 'Title', 'Number', 'Rarity', 'Condition', 'TCG Market Price',
                          'TCG Direct Low',
                          'TCG Low Price With Shipping', 'TCG Low Price', 'Total Quantity', 'Add to Quantity', 'TCG Marketplace Price', 'Photo URL', ]
            writer.writerow(header)

            old = csv.reader(not_priced)
            next(old)

            for index, card in enumerate(old):
                print(index)
                prices = api.market_prices_by_sku(card[0])['results'][0]
                print(prices)
                low_price = prices['lowestListingPrice']
                market_price = prices['marketPrice']

                if low_price is not None and market_price is not None:
                    upload_price = market_price
                    if low_price > market_price:
                        upload_price = low_price

                elif market_price is not None:
                    upload_price = market_price

                else:
                    upload_price = None

                if upload_price:
                    if upload_price < .38:
                        upload_price = .38

                    create_row(condition=card[7], quantity=card[13], product_expansion=card[2], product_name=card[3], sku=card[0], low=low_price,
                               market=market_price, up_price=upload_price)

            writer.writerows(rows)










