from django.core.management.base import BaseCommand
from amazon.amazon_mws import MWS
from other.models import CardKingdomAnalytics

api = MWS()


class Command(BaseCommand):
    def handle(self, *args, **options):
        cards = CardKingdomAnalytics.objects.filter(name='Polluted Delta').filter(expansion='Khans of Tarkir').filter(printing='Normal')

        for card in cards:
            all_price_data = card.price_history.split('|')
            print(len(all_price_data))











