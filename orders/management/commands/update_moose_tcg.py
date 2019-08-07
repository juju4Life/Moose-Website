from django.core.management.base import BaseCommand
from orders.tasks import update_moose_tcg


class Command(BaseCommand):
    def handle(self, *args, **options):
        update_moose_tcg.apply_async(que='low_priority')



