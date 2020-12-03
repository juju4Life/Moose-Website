from django.core.management.base import BaseCommand
from engine.quick_update_moose_tcg import update_tcg


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Should be ran as a celery task in the background
        update_tcg()
        # update_moose_tcg.apply_async(que='low_priority')




