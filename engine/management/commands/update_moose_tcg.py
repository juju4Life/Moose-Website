from django.core.management.base import BaseCommand
from engine.quick_update_moose_tcg import update_tcg
# from my_customs.decorators import report_error


class Command(BaseCommand):
    def handle(self, *args, **options):
        update_tcg()
        # update_moose_tcg.apply_async(que='low_priority')
        # update_moose_tcg()




