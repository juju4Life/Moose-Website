import base64
from calendar import monthrange
from collections import OrderedDict, defaultdict
from datetime import date, timedelta
from decimal import Decimal
import io
import urllib

from customer.models import StoreCredit
from django.db import transaction
from django.utils import timezone
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np


class Stats:

    @staticmethod
    def create_io_uri(fig, file_type):

        buf = io.BytesIO()
        fig.savefig(buf, format=file_type)
        buf.seek(0)
        string = base64.b64encode(buf.read())
        uri = urllib.parse.quote(string)

        return uri

    def create_bar_graph(self, x, y, x_label, y_label, title, color, legend_label=None):
        # Plot and create figure
        bar = plt.bar(x, y, color=color, label=legend_label)
        if legend_label:
            plt.legend()

        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.xticks(np.arange(1, 11, step=1), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', ])

        plt.title(title)
        fig = plt.gcf()

        for rect in bar:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2.0, height, '%d' % int(height), ha='center', va='bottom')
        return self.create_io_uri(fig, 'png')

    def create_graph(self, x, y, color, legend_label, x_label, y_label, title):
        # Plot and create figure
        plt.plot(x, y, c=color, label=legend_label)
        plt.legend()
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.xticks(np.arange(min(x), max(x) + timedelta(days=1), 9), rotation=30)

        plt.title(title)
        fig = plt.gcf()
        return self.create_io_uri(fig, 'png')

    def store_credit_daily_transactions(self):
        today = timezone.localtime().today()
        delta = timedelta(days=45)
        n_days_ago = today - delta
        year = date.today().year
        # all_credit_ytd = StoreCredit.objects.filter(date_time__year=year)

        credit_last_three_months = StoreCredit.objects.filter(date_time__range=(n_days_ago, today))
        # Tuple of each Unique month from last 90 days. Tuple contains years to keep items ordered and still separate previous year
        months = sorted(list(set([(timezone.localtime(i.date_time).year, timezone.localtime(i.date_time).month) for i in credit_last_three_months])))

        # Add each day from every unique month from months with default value of 0 to account for days where there is 0 volume for added and used
        dates_of_last_n_days_added = OrderedDict()
        dates_of_last_n_days_added_volume = OrderedDict()
        dates_of_last_n_days_used = OrderedDict()
        dates_of_last_n_days_used_volume = OrderedDict()
        day_one = n_days_ago.day
        months_days = list()
        for index, each in enumerate(months):
            year = each[0]
            month = each[1]
            days = monthrange(year, month)
            start = 1
            stop = days[1] + 1

            # Avoid creating inaccurate data for starting days of month and ending days. By default we would have created a value for every day of the
            # month even if it's ont in our 90-day query
            if index == 0:
                start = day_one
            elif index == len(months) - 1:
                stop = today.day + 1

            for day in range(start, stop):
                months_days.append(date(year, month, day))
                dates_of_last_n_days_added[f'{year}-{month}-{day}'] = 0
                dates_of_last_n_days_added_volume[f'{year}-{month}-{day}'] = 0
                dates_of_last_n_days_used[f'{year}-{month}-{day}'] = 0
                dates_of_last_n_days_used_volume[f'{year}-{month}-{day}'] = 0

        # Populate respective date with credit used / added
        for each in credit_last_three_months:
            date_obj = timezone.localtime(each.date_time)
            change_date = f'{date_obj.year}-{date_obj.month}-{date_obj.day}'
            if each.store_credit > 0:
                dates_of_last_n_days_added[change_date] += each.store_credit
                dates_of_last_n_days_added_volume[change_date] += 1
            if each.used_credit > 0:
                dates_of_last_n_days_used[change_date] += each.used_credit
                dates_of_last_n_days_used_volume[change_date] += 1

        y_credit_added = [v for k, v in dates_of_last_n_days_added.items()]
        y_credit_added_volume = [v for k, v in dates_of_last_n_days_added_volume.items()]

        y_credit_used = [v for k, v in dates_of_last_n_days_used.items()]
        y_credit_used_volume = [v for k, v in dates_of_last_n_days_used_volume.items()]

        plt.plot(months_days, y_credit_added, c='green', label='added')
        in_out_graph = self.create_graph(x=months_days, y=y_credit_used, color='red', x_label='Last 90 days',
                                         y_label='Store Credit', title='Credit In Out', legend_label='spent')

        plt.close()

        plt.plot(months_days, y_credit_added_volume, c='green', label='added')
        ninety_day_volume = self.create_graph(x=months_days, y=y_credit_used_volume, color='red', x_label='Last 90 days',
                                              y_label='Transactions', title='Transaction volume', legend_label='spent')
        plt.close()
        return {
            'in_out_graph': in_out_graph,
            'ninety_day_volume': ninety_day_volume,
        }

    def store_credit_by_month(self):

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

            for record in records:
                date_added = timezone.localtime(record.date_time)
                if date_added.month == 5:
                    records_by_date[4] = list()
                records_by_date[date_added.month].append(record)

            for k, v in records_by_date.items():
                if month_start_balances.get(k):
                    numbers = [i.store_credit for i in records_by_date[k]]

                    if k != 10:
                        credit_spent_by_month.append(
                            (month_start_balances[k] + sum(numbers)) - month_start_balances[k + 1]
                        )
                    else:
                        credit_spent_by_month.append(
                            (month_start_balances[k] + sum(numbers)) - records.last().total
                        )

                    credit_added_per_month.append(sum(numbers))
                    num_transactions_by_month.append(len(numbers))

            months = list(range(1, 11))
            credit_added = self.create_bar_graph(x=months, y=credit_added_per_month, color='green',
                                                 x_label='Months', y_label='Store Credit', title='Credit added each month', )
            plt.close()

            credit_spent = self.create_bar_graph(x=months, y=credit_spent_by_month, color='red',
                                                 x_label='Months', y_label='Store Credit', title='Credit spent each month', )
            plt.close()

            return {
                'ytd_credit_added_by_month': credit_added,
                'ytd_credit_spent_by_month': credit_spent,
            }


