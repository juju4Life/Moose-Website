from my_customs.functions import request_soup
from my_customs.standardize_sets import Standardize
from buylist.models import CardKingdomBuylist


def ck_buylist(page):

    path = "https://www.cardkingdom.com/purchasing/mtg_singles?filter%5Bipp%5D=100&filter%5Bsort%5D=name&filter%5Bsearch%5D=mtg_advanced&filter%5Bname%5D=&filter%5Bcategory_id%5D=0&filter%5Bfoil%5D=1&filter%5Bnonfoil%5D=1&filter%5Bprice_op%5D=&filter%5Bprice%5D=&page="

    CardKingdomBuylist.objects.all().delete()

    standardize = Standardize()
    card_list = []
    pages = []

    count = 0
    while count < page:
        pages.append(path + str(count + 1))
        count += 1
    for each in pages:
        print('Page ', pages.index(each) + 1)
        soup = request_soup(each)

        card_data = soup.find_all("div", {"class": "itemContentWrapper"})
        for card in card_data:
            try:
                name = standardize.name(card.table.tr.td.span.text.strip())
                foil = False
                if "FOIL" in card.table.tr.td.div.text.strip():
                    foil = True

                expansion = standardize.expansion(card.table.tr.td.div.text.strip())
                dollar = card.contents[3].div.find("span", {"class": "sellDollarAmount"}).text.strip()
                if len(dollar) > 3:
                    dollar = dollar.replace(",", "")
                cents = card.contents[3].div.find("span", {"class": "sellCentsAmount"}).text.strip()
                price = format(float("{0}.{1}".format(dollar, cents)), ".2f")

                nm_price = calculate_condition(ck_price=price, condition='near_mint', is_foil=foil, expansion=expansion)
                ex_price = calculate_condition(ck_price=price, condition='played', is_foil=foil, expansion=expansion)
                vg_price = calculate_condition(ck_price=price, condition='heavily_played', is_foil=foil, expansion=expansion)

                quantity = card.contents[3].find("ul", {"class": "dropdown-menu"}).find_all("li")
                for q in quantity[:-1].pop():
                    quantity = int(q)

                card_list.append(
                    CardKingdomBuylist(
                        name=name,
                        expansion=expansion,
                        is_foil=foil,
                        price_nm=nm_price,
                        price_ex=ex_price,
                        price_vg=vg_price,
                    )
                )

            except AttributeError:
                pass

    CardKingdomBuylist.objects.bulk_create(
        card_list
    )


def calculate_condition(ck_price, condition, is_foil, expansion):

    ck_price = float(ck_price)

    if is_foil is True:
        condition_map = {
            'near_mint': 1,
            'played': .75,
            'heavily_played': .50,
            'very_heavily_played': .30,
        }

    else:
        if expansion == 'Alpha Edition' or expansion == 'Beta Edition' or expansion == 'Unlimited Edition':
            condition_map = {
                'near_mint': 1,
                'played': .80,
                'heavily_played': .60,
                'very_heavily_played': .40,
            }

        else:

            if ck_price < 15:
                condition_map = {
                    'near_mint': 1,
                    'played': .80,
                    'heavily_played': .70,
                    'very_heavily_played': .50,
                }

            elif 14.99 < ck_price < 25:
                condition_map = {
                    'near_mint': 1,
                    'played': .85,
                    'heavily_played': .70,
                    'very_heavily_played': .50,
                }

            elif 24.99 < ck_price < 100:
                condition_map = {
                    'near_mint': 1,
                    'played': .85,
                    'heavily_played': .75,
                    'very_heavily_played': .65,
                }

            else:
                condition_map = {
                    'near_mint': 1,
                    'played': .90,
                    'heavily_played': .80,
                    'very_heavily_played': .70,
                }

    return condition_map[condition]

def get_page_count():
    path = "https://www.cardkingdom.com/purchasing/mtg_singles?filter%5Bipp%5D=100&filter%5Bsort%5D=name&filter%5Bsearch%5D=mtg_advanced&filter%5Bname%5D=&filter%5Bcategory_id%5D=0&filter%5Bfoil%5D=1&filter%5Bnonfoil%5D=1&filter%5Bprice_op%5D=&filter%5Bprice%5D=&page="
    url = path + '0'
    soup = request_soup(url)
    pages = soup.find('span', {'class': 'resultsHeader'}).text
    count = 0
    while count < len(pages):
        if pages[count] + pages[count+1] == 'of':
            pages = pages[count+2:]
            count_2 = 0
            while count_2 < len(pages):
                if pages[count_2] == 'r':
                    pages = pages[0:count_2]
                else:
                    count_2 += 1
        else:
            count += 1
    pages = int(pages.strip())
    remainder = pages % 100
    if remainder > 0:
        remainder = 1
    page_number = (pages // 100) + remainder
    print(pages, 'cards')
    return page_number















