from time import time
from decouple import config
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from amazon.amazon_mws import MWS
from my_customs.decorators import report_error
from my_customs.functions import time_it
from buylist.ck_buylist import ck_buylist, get_page_count
from buylist.scg_buylist import get_scg_buylist
from buylist.gather_buylist_info import add_buylist_data
from engine.get_group_prices import get_tcg_prices
from engine.models import CardPriceData
from tcg.tcg_functions import tcg_fee_calc, amazon_fee_calc


class Command(BaseCommand):
    @report_error
    def handle(self, *args, **options):

        api = MWS()
        start = time()
        ck_buylist(get_page_count())
        end = time()
        elapsed = (end - start) / 3600

        send_mail(
            subject='CK Buylist for hub',
            message=f'Done in {elapsed} hours',
            from_email='TCG FIRST',
            recipient_list=['jermol.jupiter@gmail.com', ]
        )

        two_start = time()
        get_scg_buylist()
        two_stop = time()
        two_elapsed = (two_stop - two_start) / 3600
        send_mail(
            subject='SCG Buylist for hub',
            message=f'Done in {two_elapsed} hours',
            from_email='TCG FIRST',
            recipient_list=['jermol.jupiter@gmail.com', ]
        )

        three_start = time()
        get_tcg_prices()
        three_stop = time()
        three_elapsed = (three_stop - three_start) / 3600
        send_mail(
            subject='TCG PRices for Hub',
            message=f'Done in {three_elapsed} hours',
            from_email='TCG FIRST',
            recipient_list=['jermol.jupiter@gmail.com', ]
        )

        four_start = time()
        add_buylist_data()
        four_stop = time()
        four_elapsed = (four_stop - four_start) / 3600

        i = time()
        go = True
        if go is True:
            report_id = api.request_and_get_inventory_report('inventory')
            headers, data = api.parse_inventory_report(report_id)
            dic = {}

            for d in data:
                dic[d['sku']] = d['price']

            obj_data = CardPriceData.objects.exclude(sku='')

            for obj in obj_data:
                price = dic.get(obj.sku, None)
                if price is not None:
                    obj.amazon_price = price
                    obj.save()
            j = time()

            ij = time_it(i, j)
            send_mail(
                subject='TCG Time for Amazon Sku prices',
                message=f'{ij}',
                from_email='TCG FIRST',
                recipient_list=['jermol.jupiter@gmail.com', ]
            )

        get_amazon = True
        if get_amazon is True:

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

                net_list = [('TCG Player', tcg_net,), ('TCG Direct', direct_net,), ('Amazon', amazon_net,), ('card Kingdom', ck,), ('Starcity Games', scg,)]

                best_net = sorted(net_list, key=lambda k: k[1], reverse=True)

                d.sell_to = best_net[0][0]
                d.best_net = best_net[0][1]
                d.tcg_net = tcg_net
                d.amazon_net = amazon_net
                try:
                    d.save()
                except Exception as e:
                    print(e)
                    print(best_net)

        send_mail(

            message=f'Buylist Hub Time\nCK: {elapsed} Hours\nSCG: {two_elapsed}\nTCG Prices: {three_elapsed}\ncreate_hub: {four_elapsed}',

            subject=f'Buylist hub finished in {elapsed} hours',
            from_email='TCGFirst',
            recipient_list=[config('my_email'), ]
        )

























