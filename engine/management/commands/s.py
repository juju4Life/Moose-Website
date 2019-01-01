from django.core.management.base import BaseCommand
from django.core.management import call_command
from customer.models import Customer
import csv

class Command(BaseCommand):
    def handle(self, **options):

        data = Customer.objects.all()
        file = open('credit.csv', 'w', newline='')
        writer = csv.writer(file)
        writer.writerow(['Name', 'Store Credit', 'Medals', 'Email'])

        for each in data:
            name = each.name
            credit = each.credit
            medals = each.medal
            email = each.email
            print(name, credit)
            writer.writerow([name, credit, medals, email])

        
