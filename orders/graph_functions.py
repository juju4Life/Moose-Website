from collections import Counter


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

    ordered_items = [{i.order_date: i.ordered_items} for i in sorted_orders if i.category == 'Magic the Gathering']

    for ordered in ordered_items:
        for k, v in ordered.items():
            k = str(k)
            order = v.split('\n')
            for o in order:
                card = o.split('<>')
                if card[0] == 'Magic the Gathering':
                    quantity = int(card[1])
                    printing = card[6]
                    language = card[4]
                    condition = card[5]

                    if printing == 'Foil' and language == 'English':
                        foil_english_dict[k] += quantity
                    elif printing == 'Foil' and language != 'English':
                        foreign_foil_dict[k] += quantity
                    elif printing == 'Normal' and language == 'English' and condition != 'Unopened':
                        english_dict[k] += quantity
                    elif printing == 'Normal' and printing != 'English' and condition != 'Unopened':
                        foreign_dict[k] += quantity
                    elif condition == 'Unopened':
                        box_dict[k] += quantity

    non_foil_english = [i for i in english_dict.values()]
    foil_english = [i for i in foil_english_dict.values()]
    foil_foreign = [i for i in foreign_foil_dict.values()]
    non_foil_foreign = [i for i in foreign_dict.values()]
    boxes = [i for i in box_dict.values()]

    return {
        'non_foil_english': non_foil_english,
        'foil_english': foil_english,
        'foil_foreign': foil_foreign,
        'non_foil_foreign': non_foil_foreign,
        'boxes': boxes,
    }


