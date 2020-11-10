
from engine.tcgplayer_api import TcgPlayerApi
from orders.models import GroupName

api = TcgPlayerApi('moose')


class Report:

    @staticmethod
    def prices_by_set():
        expansions = GroupName.objects.filter(category="Magic the Gathering")
        for expansion in expansions:
            group_id = expansion.group_id
            set_data = api.price_by_group_id(group_id=group_id)

            if set_data['success'] is True:
                yield {"data": set_data['results'], "expansion": expansion.group_name}
            else:
                yield None



