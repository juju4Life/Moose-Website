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

