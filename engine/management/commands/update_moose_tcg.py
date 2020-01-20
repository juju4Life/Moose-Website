from django.core.management.base import BaseCommand
from orders.tasks import update_moose_tcg
from my_customs.decorators import report_error


class Command(BaseCommand):
    @report_error
    def handle(self, *args, **options):
        update_moose_tcg.apply_async(que='low_priority')
        # update_moose_tcg()



