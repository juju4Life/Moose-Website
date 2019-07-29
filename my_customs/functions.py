from.decorators import offset


@offset
def set_offset(func, group_id, *args, **kwargs):
    pass


def check_direct_status(value):
    direct_map = {
        None: False,
    }

    is_direct = direct_map.get(value, True)

    return is_direct


def check_if_foil(value):
    foil = {
        'Foil': True,
        'Normal': False,
    }

    return foil[value]

