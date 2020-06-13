import string
import random
import re
import math
import requests
from time import sleep
from bs4 import BeautifulSoup as b
from.decorators import offset


def create_random_id(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


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









