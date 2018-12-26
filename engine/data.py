from engine.models import Product
import json


def add_stuff():
    with open('tcg_player_library.json') as file:
        with open('seventh_with_tcgid.json', 'w') as f:
            new = []
            x = json.load(file)
            db = Product.objects.filter(set_name='7th Edition')
            for a in x:
                for b in db:
                    if a['expansion'] in ['7th Edition']:
                        if a['expansion'] == b.set_name:
                            for each in a['cards']:
                                if each['productName'] == b.name:
                                    b.tcg_player_id = each['productId']
                                    b.save()
                    d = {
                        "model": "engine.Product",
                        "pk": b.id,
                        "fields": {
                            'name': b.name,
                            'names': b.names,
                            'price': str(b.price),
                            'image': str(b.image),
                            'quantity': b.quantity,
                            'item_type': b.item_type,
                            'brand': b.brand,
                            'specs': b.specs,
                            'set_name': b.set_name,
                            'expansion': b.expansion,
                            'mana_cost': b.mana_cost,
                            'colors': b.colors,
                            'color_identity': b.color_identity,
                            'cmc': b.cmc,
                            'types': b.types,
                            'supertypes': b.types,
                            'subtypes': b.subtypes,
                            'rarity': b.rarity,
                            'text': b.text,
                            'flavor': b.flavor,
                            'artist': b.artist,
                            'number': b.number,
                            'power': b.power,
                            'toughness': b.toughness,
                            'layout': b.layout,
                            'loyalty': b.loyalty,
                            'multiverse_id': b.multiverse_id,
                            'variations': b.variations,
                            'border': b.border,
                            'watermark': b.watermark,
                            'timeshifted': b.timeshifted,
                            'hand': b.hand,
                            'life': b.life,
                            'release_date': b.release_date,
                            'starter': b.starter,
                            'printings': b.printings,
                            'original_text': b.original_text,
                            'original_type': b.original_type,
                            'source': b.source,
                            'image_url': b.image_url,
                            'card_id': b.id,
                            'legalities': b.legalities,
                            'rulings': b.rulings,
                            'foreign_names': b.foreign_names,
                            'site': b.site,
                            'tcg_player_id': b.tcg_player_id,

                        }
                    }
                    new.append(d)
            for each in new:
                print(each['fields']['name'], each['fields']['set_name'])
            json.dump(new, f)


def create_dict():
    ds = ['Black','Blue','Green','Red'
          ]
    count = 0
    new_list = []
    while count < len(ds):
        dict_supplies = {
            "model": "engine.Product",
            "pk": 208000 + count,
            "fields":
                {
                    'site': 'supplies',
                    'brand': 'Ultimate Guard',
                    'item_type': 'Deckbox',
                    'specs': 'Holds 100+ cards',
                    'colors': '{}'.format(ds[count]),
                    'price': 17.99,
                    'image': 'ug Chroma Skin  {}.png'.format(ds[count]),
                    'name': 'Monster Playmat Tube {}. '.format(ds[count]),
                    'names':'Monster Playmat Tubes',
                    'set_name': '',
                    'expansion': '',
                    'mana_cost': '',
                    'color_identity': '',
                    'cmc': '',
                    'types': '',
                    'supertypes': '',
                    'subtypes': '',
                    'rarity': '',
                    'text': '',
                    'flavor': '',
                    'artist': '',
                    'number': '',
                    'power': '',
                    'toughness': '',
                    'layout': '',
                    'multiverse_id': '',
                    'variations': '',
                    'border': '',
                    'watermark': '',
                    'timeshifted': '',
                    'hand': '',
                    'life': '',
                    'release_date': '',
                    'starter': '',
                    'printings': '',
                    'original_text': '',
                    'original_type': '',
                    'source': '',
                    'image_url': '',
                    'card_id': '',
                    'legalities': '',
                    'rulings': '',
                    'foreign_names': '',

                }

        }

        count += 1
        new_list.append(dict_supplies)

    with open('monster_tubes_.json', 'w') as f:
        json.dump(new_list, f)



def change(read, write):
    from decimal import Decimal
    with open('{}.json'.format(read)) as read_file:
        with open('{}.json'.format(write), 'w') as write_file:
            read = json.load(read_file)
            for each in read:
                each['fields']['price'] = None
            json.dump(read, write_file)
