from collections import Counter
from decimal import Decimal


def sales_data(obj, category):
    price = sum([i.product_value for i in obj if i.category == category])
    return price


def scatter_plot(obj, event_type, max_num):
    filtered = obj.filter(event=event_type)
    points = [{'x': str(i.date), 'y': max_num} for i in filtered]
    return points


# Create list of category specific dates filling in empty dates with o.
def map_dates(dates_list, dictionary):
    new_dict = {i: 0 for i in dates_list}
    new_dict.update(dictionary)
    num_orders = [i for i in new_dict.values()]
    sum_orders = sum(num_orders)
    return num_orders, sum_orders


def orders_by_category(cat, sorted_orders):
    cat_list = [i.order_date for i in sorted_orders if i.category == cat]
    cat_list_counted = Counter(map(str, cat_list))
    return cat_list_counted


def mtg_card_info(dates, sorted_orders):
    english_dict = {i: 0 for i in dates}
    foil_english_dict = english_dict.copy()
    foreign_dict = english_dict.copy()
    foreign_foil_dict = english_dict.copy()
    box_dict = english_dict.copy()
    other_dict = english_dict.copy()
    refunds = 0

    sum_english = 0
    sum_foil_english = 0
    sum_foreign = 0
    sum_foreign_foil = 0
    sum_box = 0
    sum_other = 0

    ordered_items = [{i.order_date: i.ordered_items, 'total': i.product_value} for i in sorted_orders if i.category == 'Magic the Gathering']

    for ordered in ordered_items:
        added = 0
        total = ordered['total']
        for k, v in ordered.items():
            if k == 'total':
                pass

            else:
                k = str(k)
                order = v.split('\n')
                for o in order:
                    card = o.split('<>')
                    if card[0] == 'Magic the Gathering':
                        quantity = int(card[1])
                        printing = card[6]
                        language = card[4]
                        condition = card[5]
                        price = Decimal(card[7])
                        price = price * quantity

                        added += price

                        if printing == 'Foil' and language == 'English':
                            foil_english_dict[k] += quantity
                            sum_foil_english += price
                        elif printing == 'Foil' and language != 'English':
                            foreign_foil_dict[k] += quantity
                            sum_foreign_foil += price
                        elif printing == 'Normal' and language == 'English' and condition != 'Unopened':
                            english_dict[k] += quantity
                            sum_english += price
                        elif printing == 'Normal' and printing != 'English' and condition != 'Unopened':
                            foreign_dict[k] += quantity
                            sum_foreign += price
                        elif condition == 'Unopened':
                            box_dict[k] += quantity
                            sum_box += price
                        else:
                            print(card[1], card[2], card[3], card[4], card[5], card[6])
                    else:
                        quantity = int(card[1])
                        price = Decimal(card[7]) * quantity
                        other_dict[k] += quantity
                        sum_other += price
            if total != added:
                if k != 'total':
                    difference = total - added
                    refunds += difference

    non_foil_english = [i for i in english_dict.values()]
    foil_english = [i for i in foil_english_dict.values()]
    foil_foreign = [i for i in foreign_foil_dict.values()]
    non_foil_foreign = [i for i in foreign_dict.values()]
    boxes = [i for i in box_dict.values()]
    other = [i for i in other_dict.values()]

    return {
        'non_foil_english': non_foil_english,
        'foil_english': foil_english,
        'foil_foreign': foil_foreign,
        'non_foil_foreign': non_foil_foreign,
        'boxes': boxes,
        'other': other,
        'sum_english': sum_english,
        'sum_foreign': sum_foreign,
        'sum_foreign_foil': sum_foreign_foil,
        'sum_english_foil': sum_foil_english,
        'sum_boxes': sum_box,
        'sum_other': sum_other,
        'refunds': refunds,
    }


