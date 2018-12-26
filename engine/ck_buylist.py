import json
from engine.models import Product
from engine.tcgplayer_api import card_price



def get_standard():
    with open('card_kingdom_buylist.json') as f:
        new = []
        buylist = json.load(f)
        sets = ['Kaladesh', 'Hour of Devastation', 'Amonkhet', 'Aether Revolt']
        count = 0
        while count < len(sets):
            for each in buylist:
                if sets[count] in each['expansion'] and each['is_foil'] == False:
                    new.append(each)
            count += 1
        return new


def get_db():
    with open('ck_standard_buylist.json', 'w') as file:
        ck = get_standard()
        database = Product.objects.filter(set_name__in=['Kaladesh', 'Aether Revolt', 'Hour of Devastation', 'Amonkhet'])
        new = []
        for each in database:
            d = {
                'name': each.name,
                'expansion': each.set_name,
                'price': card_price(each.tcg_player_id)
            }
            new.append(d)
        count = 0
        to_buylist = []
        while count < len(ck):
            for each in new:
                if float(ck[count]['price']) > .10 and each['name'] == ck[count]['name'] and float(ck[count]['price']) >= (float(each['price']) * .5):
                    to_buylist.append(ck[count])
            count += 1
        json.dump(to_buylist, file)


get_db()