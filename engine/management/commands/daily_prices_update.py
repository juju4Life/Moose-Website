from django.core.management.base import BaseCommand
from engine.models import CardPriceData


class Command(BaseCommand):
    def handle(self, *args, **options):
        excluded_sets = [
            ''
        ]
        cards = CardPriceData.objects.exclude(expansion__in=excluded_sets)














