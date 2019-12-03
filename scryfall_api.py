import requests


def get_image(product_id):
    url = f'https://api.scryfall.com/cards/tcgplayer/{product_id}'
    r = requests.get(url)
    try:
        image = r.json()['image_uris']['normal']
        return image
    except Exception as e:
        print(e)
        return ''


def get_card_data(product_id):
    url = f'https://api.scryfall.com/cards/tcgplayer/{product_id}'
    r = requests.get(url)
    return r.json()


def parse_scryfall_power_toughness(card_faces):
    try:
        power_1 = card_faces[0]['power']
        toughness_1 = card_faces[0]['toughness']
    except KeyError:
        power_1 = ''
        toughness_1 = ''

    try:
        power_2 = card_faces[0]['power']
        toughness_2 = card_faces[0]['toughness']

    except KeyError:
        power_2 = ''
        toughness_2 = ''

    if power_1 and power_2:
        power = power_1 + '//' + power_2
        toughness = toughness_1 + '//' + toughness_2

    else:
        if power_1:
            power = power_1
            toughness = toughness_1

        elif power_2:
            power = power_2
            toughness = toughness_2
        else:
            power = ''
            toughness = ''

    return power, toughness

