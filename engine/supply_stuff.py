import json
from engine.models import Product



def all():
    with open('seven.json', 'w') as file:
        x = Product.objects.filter(set_name = '7th Edition')
        new = []
        count = 0
        while count < len(x):
            if x[count].price == None:
                x[count].price = 0.
            dict_ = {
                "model": "engine.Product",
                "pk": x[count].id + 45000,
                "fields": {
                    'name': x[count].name,
                    'names': x[count].names,
                    'price': str(x[count].price),
                    'image': str(x[count].image),
                    'quantity': x[count].quantity,
                    'item_type': x[count].item_type,
                    'brand': x[count].brand,
                    'specs': x[count].specs,
                    'set_name': x[count].set_name,
                    'expansion': x[count].expansion,
                    'mana_cost': x[count].mana_cost,
                    'colors': x[count].colors,
                    'color_identity': x[count].color_identity,
                    'cmc': x[count].cmc,
                    'types': x[count].types,
                    'supertypes': x[count].types,
                    'subtypes': x[count].subtypes,
                    'rarity': x[count].rarity,
                    'text': x[count].text,
                    'flavor': x[count].flavor,
                    'artist': x[count].artist,
                    'number': x[count].number,
                    'power': x[count].power,
                    'toughness': x[count].toughness,
                    'layout': x[count].layout,
                    'loyalty': x[count].loyalty,
                    'multiverse_id': x[count].multiverse_id,
                    'variations': x[count].variations,
                    'border': x[count].border,
                    'watermark': x[count].watermark,
                    'timeshifted': x[count].timeshifted,
                    'hand': x[count].hand,
                    'life': x[count].life,
                    'release_date': x[count].release_date,
                    'starter': x[count].starter,
                    'printings': x[count].printings,
                    'original_text': x[count].original_text,
                    'original_type': x[count].original_type,
                    'source': x[count].source,
                    'image_url': x[count].image_url,
                    'card_id': x[count].id,
                    'legalities': x[count].legalities,
                    'rulings': x[count].rulings,
                    'foreign_names': x[count].foreign_names,
                    'site': x[count].site,
                    'tcg_player_id': x[count].tcg_player_id,

                }

            }
            new.append(dict_)
            count += 1
            for each in new:
                print(each['fields']['name'],each['fields']['set_name'])
        json.dump(new, file)


def get_skus():
    from .models import Sku
    import json
    x = Sku.objects.filter(condition='Lightly Played')
    sku_list = []
    for each in x:
        sku_dict = {
            "model": "buylist.SkuLight",
            "pk": each.id,
            "fields": {
                "sku": each.sku,
                "name": each.name,
                "expansion": each.expansion,
                "condition": each.condition,
            }
        }
        sku_list.append(sku_dict)
    json.dump(sku_list, open('sku_light.json', 'w'))

def half(c, file):
    import json
    with open('sku_light.json') as f:
        x = json.load(f)
        count = 0
        sku_list = []
        while count < len(x) / 2:
            sku_dict = {
                "model": "buylist.SkuLight",
                "pk":  c + count + 1,
                "fields": {
                    "sku": x[c + count]["fields"]["sku"],
                    "name": x[c + count]["fields"]["name"],
                    "expansion": x[c + count]["fields"]["expansion"],
                    "condition": x[c + count]["fields"]["condition"],
                }
            }
            print(c + count)
            sku_list.append(sku_dict)
            count += 1
        json.dump(sku_list, open('{}.json'.format(file), 'w'))



