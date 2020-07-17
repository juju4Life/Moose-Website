import time
from . import mws
from decouple import config
from django.core.mail import send_mail


class MWS:
    access_key = config('MWS_ACCESS_KEY')
    seller_id = config('MWS_SELLER_ID')
    secret_key = config('MWS_SECRET_KEY')
    marketplace_usa = 'ATVPDKIKX0DER'

    important_sellers = {
        "A196LH8Y51V5YV": "Tales of Adventure",
        "A3I2YLR8TUD023": "Owl Central",
        "A1T016OEUJ4VUL": "TrollAndToad",
        "A16FC7FL4EVQKY": "Channel_Fireball",
        "A1NOA5XM9FHGQD": "Pink Bunny Games",
        "A139QX3K5TIQJJ": "Ninety Five",
        "A56F7MCHH0H20": "Strike Zone Online",
        "A1G1QJKXJJSAN2": "CoolStuffIncgames",
        "A18UWFFZ54ORCD": "MTG Mint Card Ltd.",
    }

    condition_guide = {
        "1": 'UsedLikeNew',
        "2": "UsedVeryGood",
        "3": "UsedGood",
        "4": "UsedAcceptable",
        "5": {"full": "CollectibleLikeNew", "short": 'Collectible'},
        "6": {"full": "CollectibleVeryGood", "short": 'Collectible'},
        "7": {"full": "CollectibleGood", "short": 'Collectible'},
        "8": {"full": "CollectibleAcceptable", "short": 'Collectible'},
        "9": "Used",
        "10": "Refurbished",
        "11": {'full': "New", 'short': 'New'},
    }

    reports = mws.Reports(access_key=access_key, account_id=seller_id, secret_key=secret_key, region='US')
    products = mws.Products(access_key=access_key, account_id=seller_id, secret_key=secret_key, region='US')
    feeds = mws.Feeds(access_key=access_key, account_id=seller_id, secret_key=secret_key, region='US')
    orders = mws.Orders(access_key=access_key, account_id=seller_id, secret_key=secret_key, region='US')
    inbound_shipments = mws.InboundShipments(access_key=access_key, account_id=seller_id, secret_key=secret_key, region='US')
    inventory = mws.Inventory(access_key=access_key, account_id=seller_id, secret_key=secret_key, region='US')
    recommendations = mws.Recommendations(access_key=access_key, account_id=seller_id, secret_key=secret_key, region='US')
    sellers = mws.Sellers(access_key=access_key, account_id=seller_id, secret_key=secret_key, region='US')
    finances = mws.Finances(access_key=access_key, account_id=seller_id, secret_key=secret_key, region='US')
    subscriptions = mws.Subscriptions(access_key=access_key, account_id=seller_id, secret_key=secret_key, region='US',
                                      uri='/Subscriptions/2013-07-01', version='2013-07-01')

    mws_errors = mws.MWSError()

    def request_and_get_inventory_report(self, request_type, start_date=None, end_date=None):
        request_map = {
            'inventory': '_GET_FLAT_FILE_OPEN_LISTINGS_DATA_',
            'all_listings': '_GET_MERCHANT_LISTINGS_ALL_DATA_',
            'active_listings': '_GET_MERCHANT_LISTINGS_DATA_',
            'inactive_listings': '_GET_MERCHANT_LISTINGS_INACTIVE_DATA_',
            'open_listings': '_GET_MERCHANT_LISTINGS_DATA_BACK_COMPAT_',
            'open_listings_lite': '_GET_MERCHANT_LISTINGS_DATA_LITE_',
            'open_listings_liter': '_GET_MERCHANT_LISTINGS_DATA_LITER_',
            'canceled_listings': '_GET_MERCHANT_CANCELLED_LISTINGS_DATA_',
            'sold_listings': '_GET_CONVERGED_FLAT_FILE_SOLD_LISTINGS_DATA_',
            'listings_quality_and_suppressed': '_GET_MERCHANT_LISTINGS_DEFECT_DATA_',
        }

        if request_type not in request_map:
            options = [i for i in request_map]
            raise KeyError(f'Options are: {options}')

        else:
            request_report = self.reports.request_report(report_type=request_map[request_type], start_date=start_date, end_date=end_date).parsed
            request_id = request_report['ReportRequestInfo']['ReportRequestId']['value']
            repeat_count = 0
            while True:
                try:
                    report_id = self.reports.get_report_list(requestids=request_id).parsed['ReportInfo']['ReportId']['value']
                    break
                except KeyError as e:
                    print(e)
                    time.sleep(10)
                    repeat_count += 1
                    if repeat_count > 12:

                        send_mail(
                            message=f'Unable to process request for Amazon. Took longer than 2 minutes.',
                            subject='Request Inventory Report to MWS Failed',
                            from_email='TCG First',
                            recipient_list=['jermol.jupiter@gmail.com'],
                        )
                        report_id = None
                        break
            print(report_id)
            return report_id

    def parse_inventory_report(self, report_id):
        report = self.reports.get_report(report_id=report_id)
        rep = ''.join(chr(x) for x in report.parsed).split('\n')
        data = [i.split('\t') for i in rep[1:]]

        # 0: sku, 1: asin, 2: price, 3: quantity
        headers = [i.split('\t') for i in rep][0]

        sku_and_price = [{'sku': i[0], 'price': i[2]} for i in data if i[0] != '' and i[3] != '\r' and int(i[3].replace('\r', '')) > 0]

        return headers, sku_and_price

    def parse_inactive_inventory(self, report_id):
        report = self.reports.get_report(report_id=report_id)
        rep = ''.join(chr(x) for x in report.parsed).split('\n')
        data = [i.split('\t') for i in rep[1:]]
        # headers = [i.split('\t') for i in rep][0]
        parsed_data = [
            {
                'sku': i[3],
                'price': i[4],
                'name': i[0],
                'quantity': i[5],
                'condition': i[12],
            } for i in data if i[0] != '' and 'yugioh' not in i[0].lower() and 'yu-gi-oh' not in i[0].lower() and 'sleeve' not in i[0].lower()
                               and 'deck box' not in i[0].lower() and 'booster box' not in i[0].lower() and ' lot ' not in i[0].lower()
        ]

        return parsed_data

    def parse_active_listings_report(self, report_id):
        report = self.reports.get_report(report_id=report_id)

        '''
        0 item-name
        1 item-description
        2 listing-id
        3 seller-sku
        4 price
        5 quantity
        6 open-date
        7 image-url
        8 item-is-marketplace
        9 product-id-type
        10 zshop=shipping-fee
        11 item-note
        12 item-condition
        13 zshop category1
        14 zshop-browse-path
        15 zshop-storefront-feature
        16 asin1
        17 asin2
        18 asin3
        19 will-ship-internationally
        20 expedited-shipping
        21 zshop-boldface
        22 product-id
        23 bid-for-featured-placement
        24 add-delete
        25 pending-quantity
        26 fulfillment-channel
        27 merchant-shipping-group

        '''

        rep = ''.join(chr(x) for x in report.parsed).split('\n')
        data = [i.split('\t') for i in rep[1:]]
        new_conditions = [
            {
                'sku': i[3],
                'price': i[4],
                'condition': self.condition_guide[i[12]],
                'name': i[0],
            }
                          for i in data if i[0] != '' and i[5] != '' and i[5] != '\r' and
                int(i[5].replace('\r', '')) > 0 and self.condition_guide[i[12]]['short'] == 'New']

        new__like_conditions = new_conditions + [{'sku': i[3], 'price': i[4], 'condition': self.condition_guide[i[12]]} for i in data if i[0] != '' and i[5] !=
                                             '' and i[5] != '\r' and
                int(i[5].replace('\r', '')) > 0 and self.condition_guide[i[12]]['full'] == 'CollectibleLikeNew']

        collectible_conditions = [{'sku': i[3], 'price': i[4], 'condition': self.condition_guide[i[12]]} for i in data if i[0] != '' and i[5] != '' and i[5] != '\r' and
                int(i[5].replace('\r', '')) > 0 and self.condition_guide[i[12]]['short'] == 'Collectible']
        return new_conditions, collectible_conditions

    def update_sku_price(self, xml_file):
        updated = self.feeds.submit_feed(feed=xml_file, feed_type='_POST_PRODUCT_PRICING_DATA_').parsed
        return updated

    def check_feed_submission(self, feed_id):
        return self.feeds.get_feed_submission_result(feedid=feed_id).parsed

    def get_feed_submission_list(self, feed_id):
        return self.feeds.get_feed_submission_list(feedids=feed_id).parsed

    def get_sku_prices(self, skus):
        prices = self.products.get_competitive_pricing_for_sku(marketplaceid=self.marketplace_usa, skus=skus).parsed
        return prices

    def get_sku_lowest_offer(self, skus, condition):
        return self.products.get_lowest_offer_listings_for_sku(skus=skus, condition=condition, marketplaceid=self.marketplace_usa).parsed

    def get_asin_lowest_offer(self, asin, condition):
        return self.products.get_lowest_offer_listings_for_asin(asins=asin, condition=condition, marketplaceid=self.marketplace_usa).parsed

    def get_sku_lowest_priced_offer(self, skus, condition):
        return self.products.get_lowest_priced_offers_for_sku(sku=skus, marketplaceid=self.marketplace_usa, condition=condition).parsed

    def get_matching_product(self, product_id, product_type):
        return self.products.get_matching_product_for_id(type_=product_type, ids=product_id, marketplaceid=self.marketplace_usa).parsed

    def get_product_by_asin(self, asins):
        return self.products.get_my_price_for_asin(asins=asins, marketplaceid=self.marketplace_usa).parsed



