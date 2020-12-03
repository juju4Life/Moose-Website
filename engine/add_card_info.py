from django.db import transaction
from engine.models import MTG
from scryfall_api import get_card_data, parse_scryfall_power_toughness


def add_info():

    # Map rarity to single letter
    rarity_dict = {
        "mythic": "M",
        "rare": "R",
        "uncommon": "U",
        "common": "C",
        "special": "S",
    }

    exclude_list = ['World Championship Decks', 'Oversize Cards', 'magic premiere shop', ]

    with transaction.atomic():
        cards = MTG.objects.filter(converted=False).exclude(layout__in=['supplies', 'Sealed', 'token']).exclude(expansion__in=exclude_list)

        for index, card in enumerate(cards):
            product_id = card.product_id

            # Use Scrfall API to get card info
            scry = get_card_data(product_id)

            if scry and scry['object'] != 'error':
                layout = scry['layout']

                try:
                    image = scry['image_uris']['normal']
                except KeyError:
                    image = ''

                try:
                    mana_cost = scry['mana_cost'].replace('{', '').replace('}', '').replace('/', '')
                    encoded_mana_cost = scry["mana_cost"]

                except KeyError:
                    mana_cost = ''
                    encoded_mana_cost = ''

                try:
                    colors = ''.join(scry['colors'])
                except KeyError:
                    colors = ''

                cmc = scry['cmc']
                type_line = scry['type_line']
                set_abreviation = scry['set']
                number = scry['collector_number']
                rarity = rarity_dict[scry['rarity']]
                color_indentity = ''.join(scry['color_identity'])

                power = ''
                toughness = ''
                flavor_text = ''
                loyalty = ''
                subtypes = ''

                if layout == 'transform':
                    card_faces = scry['card_faces']
                    image = card_faces[0]['image_uris']['normal']
                    oracle_text = card_faces[0]['oracle_text'] + '\n\n' + card_faces[1]['oracle_text']
                    colors = card_faces[0]['colors']
                    mana_cost = ''
                    encoded_mana_cost = ''
                    split = scry["card_faces"]

                    for ind, each in enumerate(split):
                        if ind == 0:
                            encoded_mana_cost += each["mana_cost"]
                            mana_cost += each["mana_cost"].replace('{', '').replace('}', '').replace('/', '')

                    if '—' in type_line:
                        type_line = type_line.split('//')
                        first_half = type_line[0].split('—')
                        card_type = first_half[0].strip() + ' // ' + type_line[1].strip()
                        try:
                            subtypes = first_half[1].strip()

                        except IndexError:
                            first = type_line[0].strip()
                            type_line = type_line[1].split('—')

                            card_type = first + ' // ' + type_line[0].strip()
                            subtypes = type_line[1].strip()
                    else:
                        card_type = type_line

                    artist = card_faces[0]['artist'] + ' // ' + card_faces[1]['artist']

                elif layout == 'split':
                    card_type = type_line
                    card_faces = scry['card_faces']
                    try:
                        artist = card_faces[0]['artist'] + ' // ' + card_faces[1]['artist']
                    except KeyError:
                        artist = scry['artist']

                    oracle_text = card_faces[0]['oracle_text'] + '\n\n' + card_faces[1]['oracle_text']
                    power, toughness = parse_scryfall_power_toughness(card_faces)

                elif layout == 'adventure':
                    card_faces = scry['card_faces']
                    type_line = type_line.split('—')
                    card_type = type_line[0].strip()
                    subtypes = type_line[1].strip()
                    artist = card_faces[0]['artist'] + ' // ' + card_faces[1]['artist']
                    oracle_text = card_faces[0]['oracle_text'] + '\n\n' + card_faces[1]['oracle_text']

                elif layout == 'flip':
                    card_faces = scry['card_faces']
                    type_line = type_line.split('//')
                    first = type_line[0].split('—')
                    second = type_line[1].split('—')
                    card_type = first[0] + '// ' + second[0].strip()
                    subtypes = first[1].strip() + ' //' + first[1]
                    power, toughness = parse_scryfall_power_toughness(card_faces)
                    artist = card_faces[0]['artist'] + ' // ' + card_faces[1]['artist']
                    oracle_text = card_faces[0]['oracle_text'] + '\n\n' + card_faces[1]['oracle_text']

                else:
                    card_type = type_line
                    subtypes = ''
                    if '—' in card_type:
                        split = type_line.split('—')
                        card_type = split[0].strip()
                        subtypes = split[1].strip()

                    try:
                        oracle_text = scry['oracle_text']
                    except KeyError:
                        oracle_text = ''
                    artist = scry['artist']

                    try:
                        scry['flavor_text']
                    except KeyError:
                        pass

                    try:
                        power = scry['power']
                        toughness = scry['toughness']
                    except KeyError:
                        pass

                try:
                    loyalty = scry['loyalty']
                except KeyError:
                    pass

                try:
                    card.set_abbreviation = set_abreviation
                    card.rarity = rarity
                    card.image_url = image
                    card.oracle_text = oracle_text
                    card.flavor_text = flavor_text
                    card.colors = colors
                    card.color_identity = color_indentity
                    card.card_type = card_type
                    card.subtypes = subtypes
                    card.loyalty = loyalty
                    card.power = power
                    card.toughness = toughness
                    card.layout = layout
                    card.artist = artist
                    card.collector_number = number
                    card.mana_cost = mana_cost
                    card.mana_cost_encoded = encoded_mana_cost
                    card.converted_mana_cost = cmc
                    card.converted = True
                    card.save()
                except Exception as e:
                    print(e)
                    print(scry)
                    raise Exception
            else:
                other_printings = MTG.objects.filter(name=card.name).exclude(product_id=card.product_id)
                if other_printings:
                    start = 0
                    stop = len(other_printings) - 1
                    while start > stop:
                        if other_printings[start].rarity != '':
                            card.set_abbreviation = other_printings[start].set_abreviation
                            card.rarity = other_printings[start].rarity
                            card.image_url = other_printings[start].image
                            card.oracle_text = other_printings[start].oracle_text
                            card.flavor_text = other_printings[start].flavor_text
                            card.colors = other_printings[start].colors
                            card.color_identity = other_printings[start].color_indentity
                            card.card_type = other_printings[start].card_type
                            card.subtypes = other_printings[start].subtypes
                            card.loyalty = other_printings[start].oyalty
                            card.power = other_printings[start].power
                            card.toughness = other_printings[start].toughness
                            card.layout = other_printings[start].layout
                            card.artist = other_printings[start].artist
                            card.collector_number = other_printings[start].number
                            card.mana_cost = other_printings[start].mana_cost
                            card.mana_cost_encoded = other_printings[start].encoded_mana_cost
                            card.converted_mana_cost = other_printings[start].cmc
                            card.converted = True
                            card.save()
                        else:
                            start += 1
                else:
                    pass








