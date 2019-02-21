from .price_alogrithm import *
from engine.tcgplayer_api import TcgPlayerApi
from my_customs.decorators import report_error
from django.core.mail import send_mail
from orders.models import Inventory

api = TcgPlayerApi()


@report_error
def upload(data_dict):
    if not isinstance(data_dict, dict):
        raise TypeError("Object must be a dict")

    errors_list = []
    inventory = Inventory.objects

    if len(data_dict) <= 100:
        sku_list = [i for i in data_dict]
        api_market_data = api.market_prices_by_sku(sku_list)

        if not api_market_data['errors']:
            price_data = api_market_data['results']
            print(price_data)
            for each in price_data:
                sku = str(each['skuId'])
                market_price = each['marketPrice']
                low_price = each['lowPrice']
                direct_low_price = each['directLowPrice']
                # lowest_listing = each['lowestListingPrice']

                upload_price = sku_price_algorithm(market_price, direct=direct_low_price, low=low_price)
                data_dict[sku]['upload_price'] = upload_price
        else:
            print(api_market_data['errors'])

        for sku, values in data_dict.items():
            quantity = values['quantity']
            price = values['upload_price']
            uploaded_card = api.upload(sku, price=price, quantity=quantity)

            '''if uploaded_card['errors']:
                errors_list.append(uploaded_card['errors'] + f' for sku: {sku}' + '\n')
                
            else:
                pass'''

    if errors_list:
        subject = "Errors uploading card(S)"
        message = f"There were error uploading the following list of cards\n{','.join(errors_list)}"
        mail_from = 'tcgfirst'
        mail_to = 'jermol.jupiter@gmai.com'
        send_mail(subject, message, mail_from, mail_to)




