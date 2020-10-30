import csv
from decimal import Decimal
from datetime import datetime

from administration.models import Safe
from django.db.models import Q
from django.db import transaction
from django.utils import timezone
from engine.models import MTG, MtgCardInfo
from layout.models import SinglePrintingSet
from scryfall_api import get_card_data
from tcg.tcg_functions import categorize_product_layout


def safe_stuff():
    with open('safe.csv', newline='') as f:
        file = csv.reader(f)
        convert = {
            "trade ins": 'trade in',
            "drawer balancing": "drawer balance",
            "trade": "trade in",
            "balance drawer": "drawer balance",
            'safe restock from bank': 'safe restock',
            'safe restock from bernie': 'safe restock',
            'paying josh for boxes': 'other purchase',
            'Safe balancing (reopening)': 'safe balance',
            'buy': 'trade in',
            'safe rebalance': 'safe balance',
            'Daily Deposit + money from josh': 'daily deposit',
            'daily depsit': 'daily deposit',
            "josh's buy": 'trade in',
            'deposit': 'daily deposit',
            'bank run': 'safe restock',
            'drawer replenish': 'drawer balance',
            'taderade': 'trade in',
            'jumpstart': 'trade in',
            'balance': 'safe balance',
            'safe balancing ': 'safe balance',
            'rtade': 'trade in',
            'adjustment': 'safe balance',
            'deposit from a sale (josh)': 'safe restock',
            'costco run': 'other purchase',
            'dail deposit': 'daily deposit',
            'safe restock josh': 'safe restock',
            'nick money': 'safe restock',
            'daily deposit. register $18 off': 'daily deposit',
            'daily deposit. drop $2 over.': 'daily deposit',
            'trade in': 'trade in',
            'daily deposit': 'daily deposit',
            'safe balance': 'safe balance',
            'drawer balance': 'drawer balance',
            'restock from bank': 'safe restock',
            'balancing': 'safe balance',
            'josh restock': 'safe restock',
            'for the drawer': 'drawer balance',
            'safe restock': 'safe restock',
            'paypal buy for $596': 'trade in',
            'trade in ': 'trade in',
            'daily deposit ': 'daily deposit',
            'bernie replenish': 'safe restock',
            'daily d': 'daily restock',
            'daily': 'daily restock',
            'trdae': 'trade in',
            'safe restock ': 'safe restock',
            'daily deposit + money from josh': 'safe restock',
            'replenish': 'safe restock',
            'safe balancing (reopening)': 'safe balance',
            'costco': 'other purchase',
            '': 'safe balance',
            'daily restock': 'daily deposit',


        }

        converted_reason = {
            'daily deposit': 'daily_deposit',
            'drawer balance': 'drawer_balance',
            'other purchase': 'other_purchase',
            'safe restock': 'safe_restock',
            'safe balance': 'safe_balance',
            'trade in': 'trade_in',
            'daily restock': 'daily_deposit',

        }
        next(file)
        data = Safe.objects.all()
        for old, new in zip(file, data):

            reason = convert.get(old[6].lower())
            new.reason = converted_reason[reason]
            new.save()



def go():
    exclude_list = ["Revised Edition (Foreign White Border)", "Revised Edition (Foreign Black Border)", "Fourth Edition (Foreign White Border)",
                    "Fourth Edition (Foreign Black Border)"]
    other_exclude = ["Land", "Basic Land", "Legendary Land", "Emblem", "Artifact Land", "Snow Land", "Basic Snow Land — Swamp", "Basic Snow Land — Island",
                     "Basic Snow Land — Mountain", "Basic Snow Land — Forest", "Basic Snow Land — Plains"]
    cards = MTG.objects.exclude(expansion__in=exclude_list).exclude(card_type__in=other_exclude).exclude(layout="token").filter(mana_cost_encoded="")
    print(cards.count())
    no_list = ["Booster Box", "Booster Pack", "Fat Pack", "Bundle", "Token", "Island (", "Plains (", "Forest (", "Mountain (", "Swamp (", "Intro Pack",
               "World Championship Deck", "1998", "1999", "2000", "2001", "2002", "2003", "2004", "1997", "1996", "Deck", "Oversize", "Prerelease Pack",
               "Art Series", "Box Set", "Boxed Set", "Theme Booster"]
    for card in cards:
        check = list(map(lambda i: False if i in card.name else True, no_list))
        if False not in check:

            product_id = card.product_id
            data = get_card_data(product_id)
            mana_cost = None
            encoded_mana_cost = None
            if data['object'] != 'error':
                if data.get("mana_cost"):
                    mana_cost = data["mana_cost"].replace('{', '').replace('}', '').replace('/', '')
                    encoded_mana_cost = data["mana_cost"]
                else:
                    if data["layout"] == "transform":
                        mana_cost = ''
                        encoded_mana_cost = ''

                        split = data["card_faces"]
                        for index, each in enumerate(split):
                            if index == 0:
                                encoded_mana_cost += each["mana_cost"]
                                mana_cost += each["mana_cost"].replace('{', '').replace('}', '').replace('/', '')

                        print(data["name"], encoded_mana_cost, mana_cost)
                    else:
                        pass
            card.mana_cost = mana_cost
            card.mana_cost_encoded = encoded_mana_cost
            card.save()


def el(product_id):
    ai = get_card_data(product_id)
    print(ai)


def cs():
    includes = [
        "Booster Box", "Theme Deck", "Booster Pack", "Fat Pack", "Bundle", "Boxed Set",
        "Box Set", "Gift Box", "Starter", "World Championship Deck", "World Championship Deck",
        "Intro Pack", "Planeswalker Deck", "Deck Builder's Toolkit", "Token",
                ]

    query_list = list()
    with transaction.atomic():

        query = MTG.objects.filter(layout="")
        print(query.count())

        for each in query:
            query_list.append(each)

    for q in query_list:
        q.layout = categorize_product_layout(q.name)
        q.save()


def add_cards():
    expansions = MtgCardInfo.objects.filter(card_identifier="expansion")
    upload = list()

    for expansion in expansions:
        upload.append(
            SinglePrintingSet(
                expansion=expansion.name,
                foil_only=False,
                normal_only=False,
            )
        )

    SinglePrintingSet.objects.bulk_create(upload)


def some():
    change_list = [
        "rare", "mythic", "uncommon", "common", "special",
    ]

    rarity_dict = {
        "mythic": "M",
        "rare": "R",
        "uncommon": "U",
        "common": "C",
        "special": "S",
    }

    cards = MTG.objects.filter(rarity__in=change_list)
    print(cards.count())

    for card in cards:
        card.rarity = rarity_dict[card.rarity]
        card.save()


def dates():
    from engine.models import StateInfo
    import json

    states = StateInfo.objects.all()
    with open("salesTaxByState.JSON") as f:
        data = json.load(f)

        for d in data:
            try:
                state = states.get(name=d["State"])
                state.abbreviation = d["Abbreviation"]
                state.local_tax_rate = d["Local Tax Rate"]
                state.state_tax_rate = d["State Tax Rate"]
                state.save()
            except Exception as e:
                print(e)
                state = states.get(name="District Of Columbia")
                state.abbreviation = d["Abbreviation"]
                state.local_tax_rate = d["Local Tax Rate"]
                state.state_tax_rate = d["State Tax Rate"]
                state.save()


def supply_color():
    with transaction.atomic():
        colors = ["Blue", "Black", "White", "Green", "Purple", "Orange", "Red", "Brown", "Yellow", "Pink", "Gray", "Silver", "Gold", "Turquoise", ]
        for color in colors:
            mod = MTG.objects.filter(layout="supplies", name__icontains=color, solid_color='')
            mod.update(solid_color=color)


