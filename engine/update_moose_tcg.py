import traceback
from time import time
from django.core.mail import send_mail
from engine.tcgplayer_api import TcgPlayerApi
from engine.models import MooseAutopriceMetrics, DirectData
from my_customs.decorators import report_error
from tcg.tcg_functions import metrics_update, process_card, convert_foil


api = TcgPlayerApi('moose')
first_api = TcgPlayerApi('first')


@report_error
def moose_price():

    for index, dc in enumerate(DirectData.objects.filter(in_stock=True)):
        process_card(
            api=first_api,
            sku=dc.sku,
            product_id=dc.product_id,
            condition=dc.condition,
            printing=convert_foil(dc.foil),
            language=dc.language,
            name=dc.name,
            expansion=dc.expansion,
            current_price=dc.current_price,
            market=dc.market,
            low=dc.low,
            index=index,
        )

    start_time = time()
    # Entire Moose Loot Listed inventory
    listed_cards = api.get_category_skus('magic')
    if listed_cards['success'] is True:
        print(f"Updating {listed_cards['totalItems']} for Moose Inventory")
        for index, card in enumerate(listed_cards['results']):
            try:
                condition = card['conditionName']
                printing = card['printingName']
                current_price = card['currentPrice']
                low = card['lowPrice']
                sku = card['skuId']
                product_id = card['productId']
                name = card['productName']
                expansion = card['groupName']
                market = card['marketPrice']
                language = card['languageName']

                '''    
                If the card is not English it will be priced at the low price minus one cent.

                For each card in the MooseLoot inventory we will make a request to the tcgplayer page containing all seller data for a given 
                product. 
                We request and scan pages (10 results per page) until we find 2 listings with sellers that have 10,000 sales or more. We break the while loop 
                once we have found those two listings and move on to the next card. In the case where only one or zero listings are found, 
                we break the loop and use one price to match against or default to the market price.      
                '''

                if condition == 'Unopened':
                    if current_price != low:
                        try:
                            updated_price = low - .01
                        except TypeError:
                            updated_price = None

                        if updated_price is not None:
                            if updated_price < .25:
                                updated_price = .25
                            api.update_sku_price(sku_id=sku, price=updated_price, _json=True)

                            updated_price = updated_price * .95
                            if updated_price < .25:
                                updated_price = .25
                            api.update_sku_price(sku_id=sku, price=updated_price, _json=True, channel='1')

                if language != 'English' and printing != 'Foil' and condition != 'Unopened':
                    # catch instances where there is no low price

                    good_languages = ['Japanese', 'Korean', 'Russian', 'German']

                    compare_price = api.get_market_price(product_id)
                    if compare_price['success']is True:
                        english_data = compare_price['results'][0]
                        if english_data['subTypeName'] == 'Foil':
                            english_data = compare_price['results'][1]

                        english_low = english_data['lowPrice']

                        if current_price != english_low:

                            if language in good_languages:
                                try:
                                    updated_price = english_low - .01
                                except TypeError:
                                    updated_price = None
                            else:
                                try:
                                    updated_price = english_low * .90
                                except TypeError:
                                    updated_price = None

                            if updated_price is not None:
                                if updated_price < .25:
                                    updated_price = .25
                                api.update_sku_price(sku_id=sku, price=updated_price, _json=True)
                                metrics, created = MooseAutopriceMetrics.objects.get_or_create(sku=sku)
                                metrics_update(
                                    metrics=metrics,
                                    expansion=expansion,
                                    name=name,
                                    condition=condition,
                                    printing=printing,
                                    language=language,
                                    current_price=current_price,
                                    updated_price=updated_price,
                                    low=low,
                                )
                                updated_price = updated_price * .95
                                if updated_price < .25:
                                    updated_price = .25
                                api.update_sku_price(sku_id=sku, price=updated_price, _json=True, channel='1')

                elif language == 'English' and condition != 'Unopened':

                    process_card(
                        api=api,
                        sku=sku,
                        product_id=product_id,
                        condition=condition,
                        expansion=expansion,
                        name=name,
                        printing=printing,
                        language=language,
                        current_price=current_price,
                        market=market,
                        low=low,
                        index=index,
                    )

            except Exception as e:
                print(e)
                traceback_str = ''.join(traceback.format_tb(e.__traceback__))
                subject = "Error on function to update MooseLoot tcg"
                message = f"Error on function to update MooseLoot tcg:\n {card}\n\nFull Traceback:\n\n{traceback_str}"
                mail_from = 'tcgfirst'
                mail_to = ['jermol.jupiter@gmail.com', ]
                send_mail(subject, message, mail_from, mail_to)
            print(f"Moose Card #{index}")
    end_time = time()
    elapsed = (end_time - start_time) / 3600
    subject = "Time elapsed for Moose Tcg Auto Price - 1 cycle"
    message = f"Time auto price completed: {elapsed} hours"
    mail_from = 'tcgfirst'
    mail_to = ['jermol.jupiter@gmail.com', ]
    send_mail(subject, message, mail_from, mail_to)





