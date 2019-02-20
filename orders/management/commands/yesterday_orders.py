from django.core.management.base import BaseCommand
from engine.tcgplayer_api import TcgPlayerApi
from django.core.mail import send_mail
from orders.models import Orders, NewOrders
from my_customs.decorators import report_error
from datetime import date, timedelta
from django.core.exceptions import ObjectDoesNotExist


api = TcgPlayerApi()


class Command(BaseCommand):
    @report_error
    def handle(self, **options):
        orders = Orders.objects.filter(order_date=date.today()-timedelta(1))
        for each in orders:
            for order_item in each.ordered_items:
                order = order_item.split('\n')
                for o in order:
                    card = o.split('<>')
                    category = card[0]
                    quantity = int(card[1])
                    name = card[2]
                    expansion = card[3]
                    printing = card[6]
                    language = card[4]
                    condition = card[5]
                    price = card[7]
                    sku = card[8]

                    db_data = NewOrders(
                        check_order_date=date.today(),
                        order_number=each.order_number,
                        order_date=each.order_date,
                        sku=sku,
                        name=name,
                        expansion=expansion,
                        category=category,
                        condition=condition,
                        printing=printing,
                        language=language,
                        price=price,
                        quantity=quantity,
                    )
                    db_data.save()











