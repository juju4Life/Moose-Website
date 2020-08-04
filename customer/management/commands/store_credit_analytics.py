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








