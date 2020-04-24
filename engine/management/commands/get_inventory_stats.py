from django.core.management.base import BaseCommand
from engine.models import MooseInventory
from customs.csv_ import save_csv
from engine.models import MTG


class Command(BaseCommand):
    def handle(self, *args, **options):

        sets = list(set(MTG.objects.values_list("expansion", flat=True)))
        card_types = list(set(MTG.objects.values_list("card_type", flat=True)))
        sub_types = list(set(MTG.objects.values_list("subtypes", flat=True)))
        layouts = list(set(MTG.objects.values_list("layout", flat=True)))
        artists = list(set(MTG.objects.values_list("artist", flat=True)))


        '''
        cards = MooseInventory.objects.all()
        header = ['name', 'set', 'condition', 'seller 1 price', 'seller 2 price', 'updated_price']
        csv_list = []

        for card in cards:
            csv_list.append(
                [card.name, card.expansion, card.condition, card.seller_1_total_price, card.seller_2_total_price,
                 card.updated_price]
            )

        save_csv(
            'moose_inv', header=header, rows=csv_list
        )
        '''


