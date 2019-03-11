from django.core.management.base import BaseCommand
from engine.tcgplayer_api import TcgPlayerApi
import csv
from customer.models import Customer

api = TcgPlayerApi()


class Command(BaseCommand):
    def handle(self, **options):
        with open('credit.csv', 'w', newline='') as f:
            customers = Customer.objects.all()
            writer = csv.writer(f)
            writer.writerow(['name', 'credit'])

            for each in customers:
                writer.writerow([each.name, each.credit])









