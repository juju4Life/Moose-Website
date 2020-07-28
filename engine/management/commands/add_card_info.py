from django.core.management.base import BaseCommand
from scryfall_api import get_card_data, parse_scryfall_power_toughness
from engine.models import MTG


class Command(BaseCommand):
    def handle(self, *args, **options):
        cards = MTG.objects.filter(converted=False)

        def get_it():

            # s = get_card_data('145370')
            get_it()
            # print(json.dumps(s, indent=4))
            # print(s['type_line'].split('—'))
            # type_line = s['type_line'].split('//')




























