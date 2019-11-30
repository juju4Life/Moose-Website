import json
from django.core.management.base import BaseCommand
from scryfall_api import get_card_data
from engine.models import MTG


class Command(BaseCommand):
    def handle(self, *args, **options):
        cards = MTG.objects.filter(condition='Near Mint').filter(converted=False)

        for card in cards:
            product_id = card.product_id
            scry = get_card_data(product_id)
            layout = scry['layout']
            image = scry['image_uris']['normal']
            mana_cost = scry['mana_cost']
            cmc = scry['cmc']
            type_line = scry['type_line']
            card_type = type_line
            subtypes = ''
            if '— ' in card_type:
                split = type_line.split('— ')
                card_type = split[0]
                subtypes = split[1]
            oracle_text = scry['oracle_text']
            colors = scry['colors']
            loyalty = ''
            color_indentity = ['color_identity']
            artist = scry['artist']
            set_abreviation = scry['set']
            number = scry['collector_number']
            rarity = scry['rarity']
            power = ''
            toughness = ''
            flavor_text = ''
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
            except Exception as e:
                print(e)
                print(product_id)
                raise Exception

            print(card_type, subtypes)
























