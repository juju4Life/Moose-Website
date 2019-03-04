from django.core.management.base import BaseCommand
from engine.tcgplayer_api import TcgPlayerApi
from orders.models import GroupName
from my_customs.decorators import report_error
from engine.tcg_manifest import Manifest

api = TcgPlayerApi()
M = Manifest()


class Command(BaseCommand):
    @report_error
    def handle(self, **options):
        category_ids = [1, 2, 3, 31, 56, 16, 32, 27, 17, 29, 35, 14, 22]
        current_groups = GroupName.objects

        for category in category_ids:
            group_ids = api.get_group_ids(0, category)['results'][0:20]
            for group_id in group_ids:
                group = str(group_id['groupId'])
                if current_groups.filter(group_id=group).exists() is False:

                    new_group = GroupName(
                        group_id=group,
                        group_name=group_id['name'],
                        category=M.game(category),
                        added=False,
                    )
                    new_group.save()
                    print(group_id['name'] + ' added')





