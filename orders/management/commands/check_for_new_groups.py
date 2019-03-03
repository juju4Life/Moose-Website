from django.core.management.base import BaseCommand
from engine.tcgplayer_api import TcgPlayerApi
from django.core.mail import send_mail
from orders.models import GroupName
from my_customs.decorators import report_error

api = TcgPlayerApi()


class Command(BaseCommand):
    @report_error
    def handle(self, **options):
        category_ids = [1, 2, 3, 31, 56, 16, 32, 27, 17, 29, 35, 14, 22]
        current_groups = GroupName.objects.values_list('group_id', flat=True)

        for category in category_ids:
            pass # group_ids = api.get_group_ids(offset=0, cat_id=category_ids[count])['results']




