import traceback
from django.core.management.base import BaseCommand
from orders.tasks import update_moose_tcg
from my_customs.decorators import report_error
from engine.tcgplayer_api import TcgPlayerApi
from engine.update_moose_tcg import moose_price


api = TcgPlayerApi('moose')


class Command(BaseCommand):
    @report_error
    def handle(self, *args, **options):
        update_moose_tcg.apply_async(que='low_priority')
        # update_moose_tcg()



