from.decorators import offset
import re


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

