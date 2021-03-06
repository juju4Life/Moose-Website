
from engine.models import TcgGroupPrice, MTG, CardPriceData
from engine.tcgplayer_api import TcgPlayerApi
from my_customs.functions import check_direct_status, null_to_zero
from orders.models import GroupName

api = TcgPlayerApi('first')


def get_tcg_prices():
    under = 0
    groups = GroupName.objects.filter(category='Magic the Gathering').filter(added=True).exclude(
        group_name__in=[
            'World Championship Decks', 'MagicFest Cards', "Collector's Edition", "Legends", "Arabian Nights",
            "The Dark", "Antiquities", 'Oversize Cards', "Unlimited Edition", "Alpha Edition", "Beta Edition", "APAC Lands",
            "Arena Promos", "Champs Promos", "Duels of the Planeswalkers", "European Lands", "Explorers of Ixalan",
            "Game Day & Store Championship Promos", "Guilds of Ravnica: Mythic Edition", "Guru Lands", "Magic Player Rewards",
            "Magic Premiere Shop", "Media Promos", "Open House Promos", "Portal", "Portal Second Age", "Portal Three Kingdoms",
            "Prerelease Cards", "Signature Spellbook: Jace", "Special Occasion", "Starter 1999", "Starter 2000", "The Dark",
            "Ugin's Fate Promos", "	Unhinged", "Unique and Miscellaneous Promos", "Vanguard", "International Edition", "Promo Pack: Core Set 2020",
            "Art Series: Modern Horizons", "Signature Spellbook: Gideon", "War of the Spark: Mythic Edition", "Duel Decks", "Box Sets",
            "Astral", "Battle Royale Box Set", "Beatdown Box Set", "Deckmasters Garfield vs Finkel", "Premium Deck Series: Slivers",
            "Premium Deck Series: Graveborn", "From the Vault: Dragons", "From the Vault: Exiled", "From the Vault: Relics", "From the Vault: Legends",
            "From the Vault: Realms", "From the Vault: Twenty", "From the Vault: Annihilation", "Duel Decks: Elves vs. Goblins",
            "Duel Decks: Jace vs. Chandra", "Duel Decks: Divine vs. Demonic", "Duel Decks: Garruk vs. Liliana", "Duel Decks: Phyrexia vs. the Coalition",
            "Duel Decks: Elspeth vs. Tezzeret", "Duel Decks: Knights vs. Dragons", "Duel Decks: Ajani vs. Nicol Bolas", "Duel Decks: Venser vs. Koth",
            "Duel Decks: Izzet vs. Golgari", "Duel Decks: Sorin vs. Tibalt", "Duel Decks: Heroes vs. Monsters", "Duel Decks: Jace vs. Vraska",
            "Duel Decks: Speed vs. Cunning",
        ]
    )[0:]

    for index, group in enumerate(groups):
        cards_over_five = 0

        mtg_obj = MTG.objects.filter(expansion=group.group_name)

        # print(index, group)
        price_data = api.price_by_group_id(group.group_id)

        if price_data['success'] is True:
            for i, card in enumerate(price_data['results']):
                if card['subTypeName'] == 'Normal':
                    product_id = card['productId']
                    market_price = null_to_zero(card['marketPrice'])
                    low_price = null_to_zero(card['lowPrice'])
                    direct_low_price = null_to_zero(card['directLowPrice'])
                    mid_price = null_to_zero(card['midPrice'])
                    high_price = null_to_zero(card['highPrice'])
                    is_direct = check_direct_status(direct_low_price)
                    printing = card['subTypeName']

                    card_info = mtg_obj.filter(product_id=product_id).first()

                    history = f'{market_price},{low_price},{mid_price}-'

                    if card_info is not None:
                        if market_price > .99 or low_price > .99:
                            name = card_info.product_name
                            expansion = card_info.set_name

                            obj, created = TcgGroupPrice.objects.get_or_create(
                                product_id=product_id,
                                name=name,
                                expansion=expansion,
                                printing=printing,
                            )

                            obj.is_direct = is_direct
                            obj.low_price = low_price
                            obj.market_price = market_price
                            obj.mid_price = mid_price
                            obj.high_price = high_price
                            obj.direct_low_price = direct_low_price
                            obj.price_history = obj.price_history + history
                            obj.save()

                            buylist_data, created = CardPriceData.objects.get_or_create(
                                name=name,
                                expansion=expansion,
                                printing=printing,
                                product_id=product_id,
                            )

                            buylist_data.tcg_price = low_price
                            buylist_data.tcg_direct_price = direct_low_price
                            buylist_data.tcg_market = market_price

                            buylist_data.save()

                            cards_over_five += 1

                        elif low_price >.49 and low_price < 1.50 or market_price > .49 and market_price < 1.50:
                            under += 1

                    else:
                        pass













