from django.core.management.base import BaseCommand
from scryfall_api import get_card_data
from engine.models import MTG


class Command(BaseCommand):
    def handle(self, *args, **options):

        cards = MTG.objects.filter(mana_cost_encoded='').exclude(mana_cost='')
        print(cards.count())

        for index, card in enumerate(cards):

            scry = get_card_data(card.product_id)
            if scry['object'] != 'error':
                mana_cost = scry['mana_cost']
                if '/' in mana_cost:
                    print(mana_cost)
                card.mana_cost_encoded = mana_cost
                card.save()

            print(index)









