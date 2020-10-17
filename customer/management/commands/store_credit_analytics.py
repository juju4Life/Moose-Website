from collections import defaultdict
from datetime import datetime
from decimal import Decimal

from buylist.models import StoreCredit
from customer.models import Customer
from django.core.management.base import BaseCommand
from django.db.models import Sum
from django.db import transaction
from datetime import datetime
from matplotlib import pyplot as plt
import numpy as np

# Total Credit added to
# Number of transactions


class Command(BaseCommand):
    def handle(self, *args, **options):
        with transaction.atomic():
            records = StoreCredit.objects.all().exclude(name="Name")
            records_by_date = defaultdict(list)
            credit_spent_by_month = list()
            credit_added_per_month = list()
            num_transactions_by_month = list()

            month_start_balances = {
                1: Decimal(26175.94),
                2: Decimal(26479.71),
                3: Decimal(25198.69),
                4: Decimal(26018.93),
                5: Decimal(26018.93),
                6: Decimal(28156.43),
                7: Decimal(27953.18),
                8: Decimal(30526.17),
                9: Decimal(31002.09),
                10: Decimal(32559.62),
            }


            '''
            for i in range(1, 11):
                print(f"On month {i}")
                month_start_total = sum([i.credit for i in Customer.history.as_of(datetime(2020, i, 1))])
                month_start_balances[i] = month_start_total
            '''

            for record in records:
                name = record.name
                credit_added = record.store_credit
                date_added = record.date_time
                if date_added.month == 5:
                    records_by_date[4] = list()
                records_by_date[date_added.month].append(record)

            for k, v in records_by_date.items():
                print(month_start_balances[k])
                if month_start_balances.get(k):
                    numbers = [i.store_credit for i in records_by_date[k]]

                    if k != 10:
                        credit_spent_by_month.append(
                            (month_start_balances[k] + sum(numbers)) - month_start_balances[k+1]
                        )
                    else:
                        credit_spent_by_month.append(
                            (month_start_balances[k] + sum(numbers)) - records.last().total
                        )

                    credit_added_per_month.append(sum(numbers))
                    num_transactions_by_month.append(len(numbers))
                    '''
                    over_hundred_numbers = [i.store_credit for i in records_by_date[k] if i.store_credit > 100]
                    records_by_customer = defaultdict(int)
                    for each in v:
                        records_by_customer[each.name] += each.store_credit
                    
                    c_totals = [(k, v) for k, v in records_by_customer.items()]
                    c_totals = sorted(c_totals, key=lambda i: i[1], reverse=True)
                    print(f"{k}: Total Credit: {sum(numbers)} - Total Number of Transactions: {len(numbers)} - Total number over $100: {sum(over_hundred_numbers)} "
                          f" - Total number of transactions over $100: {len(over_hundred_numbers)}")
                    for each in c_totals[0:5]:
                        print(each[0], each[1])
                    print('_______________________________________________________________________________________')'''

            # print(f"Month Start Balances: {month_start_balances}")
            # print(f"Credit spent by month: {credit_spent_by_month}")
            # print(f"credit_added_per_month: {credit_added_per_month}")
            # print(f"num_transactions_by_month: {num_transactions_by_month}")
            months = list(range(1, 11))

            def plot_graph(data, color, title):
                bar = plt.bar(months, data, color=color)
                plt.xlabel('Month')
                plt.ylabel('Store Credit')
                plt.xticks(np.arange(1, 11, step=1), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', ])
                plt.title(title)

                for rect in bar:
                    height = rect.get_height()
                    plt.text(rect.get_x() + rect.get_width() / 2.0, height, '%d' % int(height), ha='center', va='bottom')

                plt.show()

            plot_graph(credit_added_per_month, 'green', 'Credit added each month')
            plot_graph(credit_spent_by_month, 'red', 'Credit spent each month')

            plt.plot(months, num_transactions_by_month)
            plt.xlabel('Month')
            plt.ylabel('Transactions')
            plt.xticks(np.arange(1, 11, step=1), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', ])
            plt.title('Trade-in Volume')
            plt.show()















