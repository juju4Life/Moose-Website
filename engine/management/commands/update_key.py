from django.core.management.base import BaseCommand

from collections import defaultdict

from engine.tcg_credentials import Credentials
from other.models import CardKingdomAnalytics, StarCityAnalytics

tcg = Credentials()


class Command(BaseCommand):
    def handle(self, **options):
        # tcg.new_bearer_token()

        def parse(buylist_obj):
            data = defaultdict(float)
            buylist = buylist_obj.objects.all()

            for index, card in enumerate(buylist):
                print(index)
                card_data = card.price_history.split('|')[0:-1]

                for each_card in card_data:
                    each_card = each_card.split(',')
                    date_added = each_card[2].strip()
                    if date_added != '2020-03-28':
                        price = each_card[0]

                        data[date_added] += float(price)
            print(data)

        parse(CardKingdomAnalytics)


