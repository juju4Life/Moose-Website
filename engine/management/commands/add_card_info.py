import json
from django.core.management.base import BaseCommand
from scryfall_api import get_card_data, parse_scryfall_power_toughness
from engine.models import MTG


class Command(BaseCommand):
    def handle(self, *args, **options):
        cards = MTG.objects.filter(condition='Near Mint').filter(converted=False)
        print(cards.count())

        def get_it():
            for index, card in enumerate(cards):
                product_id = card.product_id
                scry = get_card_data(product_id)
                if scry['object'] != 'error':
                    layout = scry['layout']

                    try:
                        image = scry['image_uris']['normal']
                    except KeyError:
                        image = ''

                    try:
                        mana_cost = scry['mana_cost']
                    except KeyError:
                        mana_cost = ''

                    try:
                        colors = scry['colors']
                    except KeyError:
                        colors = ''

                    cmc = scry['cmc']
                    type_line = scry['type_line']
                    set_abreviation = scry['set']
                    number = scry['collector_number']
                    rarity = scry['rarity']
                    color_indentity = ['color_identity']

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
                        card.converted_mana_cost = cmc
                        card.converted = True
                        card.save()
                    except Exception as e:
                        print(e)
                        print(scry)
                        raise Exception

                    print(f"{card_type}-{subtypes} - {index}")
                    print(power, toughness)

        # s = get_card_data('145370')
        get_it()
        # print(json.dumps(s, indent=4))
        # print(s['type_line'].split('—'))
        # type_line = s['type_line'].split('//')


























