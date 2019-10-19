import random
from django.core.management.base import BaseCommand
from engine.models import CardPriceData
from my_customs.functions import request_pages_data
from tcg.tcg_functions import moose_price_algorithm, get_product_seller_info


def url(product_id, foil, condition, page=1):
    random_string = str(random.randint(1000000000000, 9999999999999))
    condition = condition.replace(" ", "")
    url_path = {
        'Normal': f'https://shop.tcgplayer.com/productcatalog/product/changepricetablepage?filterName=Condition&filterValue={condition}&productId={product_id}&'
        f'gameName=magic&page={page}&X-Requested-With=XMLHttpRequest&_={random_string}',

        'Foil': f'https://shop.tcgplayer.com/productcatalog/product/changepricetablepage?filterName=Printing&filterValue=Foil&productId={product_id}&'
        f'gameName=magic&page={page}&X-Requested-With=XMLHttpRequest&_={random_string}',
        }

    return url_path[foil]


class Command(BaseCommand):
    def handle(self, *args, **options):
        excluded_sets = [
            ''
        ]

        cards = CardPriceData.objects.exclude(expansion__in=excluded_sets)

        for index, card in enumerate(cards):
            try:
                next_page = True
                page = 1
                seller_data_list = []
                product_id = card.product_id

                while next_page is True:
                    request_path = url(product_id=product_id, condition="LightlyPlayed", foil='Normal', page=page)

                    data, page_source = request_pages_data(
                        url=request_path,
                        tag='div',
                        attribute='class',
                        attribute_value='product-listing ',
                    )

                    # Check if there are products in the request. If not that indicates no more listings and thus we break the loop
                    if not data:
                        break

                    # loop over each item on the page and get Seller Info
                    for d in data:
                        seller_condition = d.find('div', {'class': 'product-listing__condition'}).text.strip()
                        seller_name = d.find('a', {'class': 'seller__name'}).text.strip()

                        if seller_name != 'MTGFirst' and seller_name != 'Moose Loot' and 'Lightly Played' == seller_condition:
                            price, total_price, seller_total_sales = get_product_seller_info(d)

                            price_dict = {
                                'price': total_price,
                                'gold': True if seller_total_sales >= 10000 else False,
                            }

                            seller_data_list.append(price_dict)
                            if len(seller_data_list) == 5:
                                next_page = False
                                break

                    page += 1

                '''
                We will check the number of other seller listings.
                If there were zero listings found we simply make the updated price the market price.
    
                If just one listing is found, we run the price algorithm which will just add shipping if default and price .01c less.
    
                If there are 2 10,000+ listings, algorithm will compare and take the best/cheapest listings price
                '''

                updated_price = moose_price_algorithm(seller_data=seller_data_list, )

                if updated_price is not None:
                    card.tcg_price = updated_price
                    tcg_fee = 12.75
                    flat_fee = .30
                    shipping_fees = 2.85
                    tracking_fee = .55

                    net = (updated_price * ((100 - tcg_fee) / 100)) - flat_fee - shipping_fees
                    if updated_price > 9.99:
                        net = net - tracking_fee

                    card.tcg_net = net
                    card.save()
                    print(index)
            except Exception as e:
                print(e)
                print(card.name, card.expansion)













