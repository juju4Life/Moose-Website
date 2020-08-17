from django.db.models import Q
from django.db import transaction
from engine.models import MTG, MtgCardInfo
from layout.models import SinglePrintingSet
from scryfall_api import get_card_data


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
    includes = ["Booster Box", "Theme Deck", "Booster Pack", "Fat Pack", "Bundle", "Boxed Set", "Box Set", "Gift Box", "Starter",
                "World Championship Deck", "World Championship Deck", "Intro Pack", ]

    query_list = list()
    with transaction.atomic():
        for include in includes:

            query = MTG.objects.filter(name__icontains=include).filter(layout="")
            print(query.count())
            for each in query:
                query_list.append(each)

        for q in query_list:
            q.layout = "Sealed"
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
    blues = ["Blue", "Turquoise", ]
    reds = ["Red", ]
    purples = ["Purple", "", ]
    greens = ["Green", ]
    yellows = ["Yellow", ]
    pinks = ["Pink", ]


