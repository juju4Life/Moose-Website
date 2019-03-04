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
        current_groups = GroupName.objects

        for each in GroupName.objects.all():
            each.added = True
            each.save()

        for category in category_ids:
            group_ids = api.get_group_ids(0, category)['results'][0:20]
            for group_id in group_ids:
                if current_groups.filter():
                    pass





