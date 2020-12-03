import re
import math
import requests
from time import sleep, strftime, localtime
from uuid import uuid4
from bs4 import BeautifulSoup as b
from.decorators import offset

"""

Useful functions used throughout the project

"""


def change_str_to_zero(value):
    if value == '':
        return 0
    else:
        return value


def sort_model_query(obj, sort_type):

    field = {
        'sort_by_set': 'expansion',
        'sort_by_set_reverse': 'expansion',
        'sort_by_name': 'name',
        'sort_by_name_reverse': 'name',
    }

    if sort_type == 'sort_by_set' or sort_type == 'sort_by_name':
        return obj.order_by(field[sort_type])

    elif sort_type == 'sort_by_set_reverse' or sort_type == 'sort_by_name_reverse':
        return obj.order_by(f'-{field[sort_type]}')

    elif sort_type == 'in-stock':
        return obj.filter(in_stock=True)

    else:
        return obj


def change_order_status(string, order_status):
    new_status = replace_text_between_two_words("<status_start>", "<status_end>", replacement=order_status, string=string)
    return new_status


def format_cart_for_text_field_storage(cart, order_number, payment_type, paypal_email, total_price, store_credit_total=None, order_status='Not Received'):
    master = ""
    date_time_processed = strftime("%Y-%m-%d at %I:%M%p", localtime())

    for each in cart:
        master = master + f"{each['name']}<attribute>{each['expansion']}<attribute>{each['printing']}<attribute>{each['condition']}" \
                          f"<attribute>{each['language']}<attribute>" \
                          f"{each['quantity']}<attribute>{each['price']}<attribute>{each['total']}<attribute>{each['product_id']}<card>"

    if store_credit_total:
        total = store_credit_total
    else:
        total = total_price

    order_info = f"{date_time_processed}<card>{order_number}<card>{total}<card><status_start>{order_status}<status_end><payment_type_start>" \
                 f"{payment_type}<payment_type_end><paypal_email_start>{paypal_email}<paypal_email_end><order>"
    master = master + order_info

    return master


def split_text_field_string_for_orders(string):
    if string:
        orders = string.split("<order>")[:-1]
        orders_list = list()

        for order in orders:
            order_status = text_between_two_words("<status_start>", "<status_end>", order)
            payment_type = text_between_two_words("<payment_type_start>", "<payment_type_end>", order)
            paypal_email = text_between_two_words("<paypal_email_start>", "<paypal_email_end>", order)
            attributes = order.split("<card>")[:-1]
            order_date = attributes[-3]
            order_number = attributes[-2]
            total = attributes[-1]

            order_details = {
                "order_date": order_date,
                "order_number": order_number,
                "order_status": order_status,
                "payment_type": payment_type,
                "paypal_email": paypal_email,
                "total": total,
                "items": list(),
            }

            for each in attributes[0:-3]:
                attribute = each.split("<attribute>")
                order_details["items"].append(
                    {
                        "name": attribute[0],
                        "expansion": attribute[1],
                        "printing": attribute[2],
                        "condition": attribute[3],
                        "language": attribute[4],
                        "quantity": attribute[5],
                        "price": attribute[6],
                        "total_price": attribute[7],
                        "product_id": attribute[8],
                    }
                )

            orders_list.append(order_details)
    else:
        orders_list = list()

    return orders_list


def create_random_id(size=6):
    return uuid4().hex[:size]


def request_soup(url):
    r = requests.get(url).content
    soup = b(r, "html.parser")
    return soup


@offset
def set_offset(func, group_id, *args, **kwargs):
    pass


def check_direct_status(value):
    direct_map = {
        None: False,
        0: False,
    }

    is_direct = direct_map.get(value, True)

    return is_direct


def check_if_foil(value):
    foil = {
        'Foil': True,
        'Normal': False,
    }

    return foil[value]


def null_to_zero(value):
    d = {
        None: 0,
    }
    return d.get(value, value)


def float_from_string(string):
    parsed_string = re.findall(r"[-+]?\d*\.\d+|\d+", string)
    if len(parsed_string) > 0:
        return float(parsed_string[0])
    else:
        return 0


def integers_from_string(string):
    integers = [i for i in string if i.isdigit()]
    if len(integers) > 0:
        return int(''.join(integers))
    else:
        return 0


def text_between_two_words(word_1, word_2, string):
    p = re.compile(r'(?<={}).*?(?={})'.format(word_1, word_2))
    extracted = re.search(p, string).group()
    return extracted


def replace_text_between_two_words(word1, word2, replacement, string):
    replacement = re.sub(f'{word1}.*?{word2}', f'{word1}{replacement}{word2}', string, flags=re.DOTALL)
    return replacement


def convert_to_number_of_pages(number):
    return math.ceil(number / 10)


def request_pages_data(url, tag, attribute, attribute_value):
    sleep(.5)
    r = requests.get(url).content
    soup = b(r, 'html.parser')
    data = soup.find_all(tag, {attribute: attribute_value})

    return data, soup


def integers_to_percentage(old_num, new_num):
    old_num = float(old_num)
    new_num = float(new_num)

    try:
        percent = (new_num - old_num) / old_num * 100
    except ZeroDivisionError:
        percent = 0

    return percent


def time_it(start, stop):
    elapsed = (stop - start)

    minutes = round(elapsed / 60, 2)

    hours = round(elapsed / 3600, 2)

    return f'Seconds: {round(elapsed, 2)}', f'Minutes: {minutes}', f'Hours: {hours}'









