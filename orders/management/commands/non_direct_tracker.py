from django.core.management.base import BaseCommand
from engine.tcgplayer_api import TcgPlayerApi
from engine.models import DirectData
from datetime import date, timedelta

api = TcgPlayerApi()


class Command(BaseCommand):
    def handle(self, **options):
        listed_cards = api.get_category_skus('magic')

        success = listed_cards['success']
        if success is True:
            direct_database = DirectData.objects
            cards = listed_cards['results']
            non_direct = 0

            for card in cards:
                if card['directLowPrice'] is None:
                    non_direct += 1
                    sku = card['skuId']
                    database_entry_check = direct_database.filter(sku=sku).exists()

                    if database_entry_check is True:
                        entry = direct_database.get(sku=sku)
                        entry.total_days_non_direct += 1

                        if date.today() - timedelta(days=1) == entry.last_add:
                            entry.consecutive_days_non_direct += 1

                        else:

                            # Track how many total consecutive days card was on TcgPlayer Direct
                            entry.last_consecutive_run = entry.consecutive_days_non_direct
                            entry.consecutive_days_non_direct = 1

                            # Track how many days since card was not TcgPlayer Direct
                            delta = date.today() - entry.last_add
                            entry.days_non_direct = delta.days

                        entry.last_add = date.today()
                        entry.save()

                    else:

                        printing_map = {
                            'Foil': True,
                            'Normal': False,
                        }
                        new_entry = DirectData(
                            name=card['productName'],
                            expansion=card['groupName'],
                            condition=card['conditionName'],
                            language=card['languageName'],
                            foil=printing_map[card['printingName']],
                            sku=sku,
                            product_id=card['productId'],
                            last_add=date.today(),
                            consecutive_days_non_direct=1,
                            total_days_non_direct=1,
                            last_consecutive_run=1,
                            days_non_direct=1,

                        )

                        new_entry.save()







