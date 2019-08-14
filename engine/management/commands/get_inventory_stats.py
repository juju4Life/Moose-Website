from django.core.management.base import BaseCommand
from engine.models import MooseInventory
from customs.csv_ import save_csv


class Command(BaseCommand):
    def handle(self, *args, **options):
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


