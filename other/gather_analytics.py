from datetime import date
from my_customs.functions import integers_to_percentage


def analyze(store, name, expansion, printing, buylist_price):

    obj, created = store.objects.get_or_create(name=name, expansion=expansion, printing=printing)

    if obj:
        last_price = obj.last_price

        if created:
            diff = 0
        else:
            if last_price == 0:
                diff = 0
            else:
                diff = integers_to_percentage(old_num=last_price, new_num=buylist_price)

            if diff > 0:
                obj.consecutive_increase += 1
                obj.consecutive_decrease = 0
            elif diff < 0:
                obj.consecutive_decrease += 1
                obj.consecutive_increase = 0
            else:
                if diff >= 0:
                    obj.total_days_without_decrease += 1

        data = f"{buylist_price}, {diff}, {date.today()}|"
        
        obj.price_history = obj.price_history + data
        obj.last_price = obj.current_price
        obj.current_price = buylist_price
        obj.last_percent_change = diff











