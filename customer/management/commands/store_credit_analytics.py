from collections import defaultdict

from buylist.models import StoreCredit
from django.core.management.base import BaseCommand
from datetime import datetime


class Command(BaseCommand):
    def handle(self, *args, **options):
        records = StoreCredit.objects.all().exclude(name="Name")
        records_by_date = defaultdict(list)

        for record in records:
            name = record.name
            credit_added = record.store_credit
            date_added = record.date_time
            records_by_date[date_added.month].append(record)

        for k, v in records_by_date.items():
            numbers = [i.store_credit for i in records_by_date[k]]
            over_hundred_numbers = [i.store_credit for i in records_by_date[k] if i.store_credit > 100]
            records_by_customer = defaultdict(int)
            for each in v:
                records_by_customer[each.name] += each.store_credit

            c_totals = [(k, v) for k, v in records_by_customer.items()]
            c_totals = sorted(c_totals, key=lambda i: i[1], reverse=True)
            print(f"{k}: Total Credit: {sum(numbers)} - Total Number of Transactions: {len(numbers)} - Total number over $100: {sum(over_hundred_numbers)} "
                  f" - Total number of transactions over $100: {len(over_hundred_numbers)}")
            for each in c_totals[0:5]:
                print(each[0], each[1])
            print('_______________________________________________________________________________________')












