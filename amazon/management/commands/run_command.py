from datetime import datetime
from django.core.management.base import BaseCommand
from amazon.models import AmazonLiveInventory
from amazon.amazon_mws import MWS
import json
import boto3
import xmltodict
from decouple import config
from engine.models import CardPriceData

api = MWS()


class Command(BaseCommand):
    def handle(self, *args, **options):

        # report_id = api.request_and_get_inventory_report('inventory')

        # p = api.parse_inactive_inventory('16611745912018153')
        '''
        update_feed_list = []
        client = boto3.client(
            'sqs',
            aws_access_key_id=config("AWS_ACCESS_KEY"),
            aws_secret_access_key=config("AWS_SECRET_KEY"),
        )

        while True:
            messages = client.receive_message(
                QueueUrl='https://queue.amazonaws.com/963180512106/Alert',
                AttributeNames=['All'],
                MaxNumberOfMessages=10,
            )
            try:
                messages = messages['Messages']
            except KeyError:
                break
            if messages:
                my_seller_id = api.seller_id
                for message in messages:
                    data = message['Body']
                    data = xmltodict.parse(data)['Notification']
                    asin = data['NotificationPayload']['AnyOfferChangedNotification']['OfferChangeTrigger']['ASIN']
                    other_item_data = api.get_product_by_asin(asin)
                    condition = data['NotificationPayload']['AnyOfferChangedNotification']['OfferChangeTrigger']['ItemCondition']
                    my_sub_condition = other_item_data['Product']['Offers']['Offer']['ItemSubCondition']['value']
                    sku = other_item_data['Product']['Offers']['Offer']['SellerSKU']['value']
                    time_of_change = data['NotificationPayload']['AnyOfferChangedNotification']['OfferChangeTrigger']['TimeOfOfferChange']
                    new_conditions = data['NotificationPayload']['AnyOfferChangedNotification']['Summary']['NumberOfOffers']['OfferCount']
                    offers = data['NotificationPayload']['AnyOfferChangedNotification']['Offers']['Offer']
                    for offer in offers:
                        try:
                            seller_id = offer['SellerId']
                            if seller_id == my_seller_id:
                                pass

                            else:
                                if seller_id not in [i for i in api.important_sellers]:
                                    pass

                                else:
                                    seller_sub_condition = offer['SubCondition']
                                    if my_sub_condition == seller_sub_condition:
                                        seller_positive_feedback_rating = offer["SellerFeedbackRating"]["SellerPositiveFeedbackRating"]
                                        seller_feedback_count = offer["SellerFeedbackRating"]["FeedbackCount"]
                                        list_price = offer['ListingPrice']["Amount"]
                                        shipping_price = offer['Shipping']['Amount']
                                        total_price = float(list_price) + float(shipping_price)

                                        update_feed_list.append({
                                            'sku': sku,
                                            'price': total_price,
                                        })
                                        break

                        except TypeError as e:
                            print(e)

                entries = [
                    {'Id': msg['MessageId'], 'ReceiptHandle': msg['ReceiptHandle']}
                    for msg in messages['Messages']
                ]

                resp = client.delete_message_batch(
                    QueueUrl='https://queue.amazonaws.com/963180512106/Alert', Entries=entries
                )

                if len(resp['Successful']) != len(entries):
                    print('Errors')
            else:
                break

        # Upload Feed

        '''

        # z = api.subscriptions.create_subscriptions(subscription_type='AnyOfferChanged', marketplace_id='ATVPDKIKX0DER', enable_subscription='true')
        # z = api.subscriptions.send_test_notification_to_destination()
        # a, b = api.parse_active_listings_report('16381982011018137')
        # a = api.get_sku_prices('1L-ANJF-19DN')

        # print(json.dumps(a, indent=4))
        # a = api.get_asin_lowest_offer(asin='B019CZA9KO', condition='new')
        # print(json.dumps(a, indent=4))
        # print(api.check_feed_submission('151729018128'))

        # api.request_and_get_inventory_report('active_listings')
        # d = api.get_sku_lowest_offer('1U-PLK0-3Q09', 'new')

        '''
         live = AmazonLiveInventory.objects
        report_id = api.request_and_get_inventory_report('inventory')

        headers, data = api.parse_inventory_report(report_id)

        for d in data:
            new_item = live.create(
                sku=d[0],
                old_price=d[1],
                new_price=0,
                time_check_delta=datetime.now(),

            )

            new_item.save()
        '''

        # live = AmazonLiveInventory.objects
        # report_id = api.request_and_get_inventory_report('active_listings')

        from customs.csv_ import save_csv
        header = ['Expansion', 'Name', 'Sku']
        rows = []
        for c in CardPriceData.objects.all():
            name = c.name
            expansion = c.expansion
            sku = ''

            rows.append(
                [expansion, name, sku]
            )

        save_csv(
            'Card_data', header=header, rows=rows
        )









