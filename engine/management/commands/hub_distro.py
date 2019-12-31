from django.core.management.base import BaseCommand
from engine.models import CardPriceData
from tcg.tcg_functions import tcg_fee_calc, amazon_fee_calc


class Command(BaseCommand):
    def handle(self, *args, **options):

        data = CardPriceData.objects.all()

        for index, d in enumerate(data):
            ck = d.ck_buylist
            scg = d.scg_buylist

            tcg = d.tcg_price
            direct = d.tcg_direct_price
            amazon = d.amazon_price

            tcg_net, fees = tcg_fee_calc(tcg)
            direct_net, direct_fees = tcg_fee_calc(direct, direct=True)
            amazon_net, a_fees = amazon_fee_calc(amazon)

            net_list = [('TCG Player', tcg_net, ), ('TCG Direct', direct_net, ), ('Amazon', amazon_net, ), ('card Kingdom', ck, ), ('Starcity Games', scg, )]

            best_net = sorted(net_list, key=lambda i: i[1], reverse=True)

            d.sell_to = best_net[0][0]
            d.save()
            print(d.sell_to)
            print(index)











