from datetime import date
from .models import CardKingdomAnalytics


def analyze(name, expansion, printing, buylist_price):
    obj = CardKingdomAnalytics.objects.get_or_create(name=name, expansion=expansion, printing=printing)

    data = [buylist_price, date.today(), ]








