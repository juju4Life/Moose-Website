from django.core.management.base import BaseCommand
from engine.models import MooseInventory
from customs.csv_ import save_csv
from engine.models import MTG, MtgCardInfo


class Command(BaseCommand):
    def handle(self, *args, **options):
        MtgCardInfo.objects.all().delete()

        sets = list(set(MTG.objects.values_list("expansion", flat=True)))
        sets = list(
            map(
                lambda i: MtgCardInfo(name=i, card_identifier="expansion"), sets
            )
        )

        card_types = list(set(MTG.objects.values_list("card_type", flat=True)))
        card_types = list(
            map(
                lambda i: MtgCardInfo(name=i, card_identifier="card_type"), card_types
            )
        )
        sub_types = list(set(MTG.objects.values_list("subtypes", flat=True)))
        sub_types = list(
            map(
                lambda i: MtgCardInfo(name=i, card_identifier="subtypes"), sub_types
            )
        )
        layouts = list(set(MTG.objects.values_list("layout", flat=True)))
        layouts = list(
            map(
                lambda i: MtgCardInfo(name=i, card_identifier="layout"), layouts
            )
        )
        artists = list(set(MTG.objects.values_list("artist", flat=True)))
        artists = list(
            map(
                lambda i: MtgCardInfo(name=i, card_identifier="artist"), artists
            )
        )
        rarities = list(set(MTG.objects.values_list("rarity", flat=True)))
        rarities = list(
            map(
                lambda i: MtgCardInfo(name=i.title(), card_identifier="rarity"), rarities
            )
        )

        names = list(set(MTG.objects.values_list("name", flat=True)))
        print(len(names))
        names = list(
            map(
                lambda i: MtgCardInfo(name=i, card_identifier="name"), names
            )
        )

        MtgCardInfo.objects.bulk_create(sets)
        MtgCardInfo.objects.bulk_create(card_types)
        MtgCardInfo.objects.bulk_create(sub_types)
        MtgCardInfo.objects.bulk_create(layouts)
        MtgCardInfo.objects.bulk_create(artists)
        MtgCardInfo.objects.bulk_create(rarities)
        MtgCardInfo.objects.bulk_create(names)

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


