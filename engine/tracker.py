from .models import ForeignOrder, Orders
from django.db.models import Q
from functools import reduce
from operator import or_

class Database:
    def update_foreign(self):
        languages = ['Japanese', 'Chinese', 'Korean', 'French', 'Spanish', 'Italian', 'Russian', 'German', 'Portuguese']
        orders = Orders.objects.filter(reduce(or_, (Q(order_details__icontains=itm.strip()) for itm in languages)))
        foreign_orders_list = ForeignOrder.objects.values_list('order_number', flat=True)
        order_list = orders.values_list('order_number', flat=True)

        updating = [i for i in order_list if i not in foreign_orders_list]
        orders = orders.filter(order_number__in=updating)
        for each_order in orders:
            x = each_order.order_details.split('\n')
            for each in x:
                if 'English' in each:
                    x.remove(each)
            x = '\n'.join(x)
            to_save = ForeignOrder(
                order_number = each_order.order_number,
                order_date = each_order.order_date,
                cards = x,

            )
            to_save.save()

