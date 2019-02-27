from django.core.management.base import BaseCommand
from engine.tcgplayer_api import TcgPlayerApi
from engine.tcg_manifest import Manifest
from orders.models import GroupName

api = TcgPlayerApi()
M = Manifest()


class Command(BaseCommand):
    def handle(self, **options):

        groups = GroupName.objects.all()
        for index, group in enumerate(groups):
            category = api.get_group_id_info(str(group.group_id))['results'][0]['categoryId']
            cat = M.game(category)
            group.category = cat
            group.save()
            print(index)



