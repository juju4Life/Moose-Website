import time
import mws
from decouple import config
from my_customs.exml import CreateXML


class MWS:
    access_key = config('MWS_ACCESS_KEY')
    seller_id = config('MWS_SELLER_ID')
    secret_key = config('MWS_SECRET_KEY')
    marketplace_usa = 'ATVPDKIKX0DER'

    reports = mws.Reports(access_key=access_key, account_id=seller_id, secret_key=secret_key, region='US')
    products = mws.Products(access_key=access_key, account_id=seller_id, secret_key=secret_key, region='US')
    feeds = mws.Feeds(access_key=access_key, account_id=seller_id, secret_key=secret_key, region='US')
    orders = mws.Orders(access_key=access_key, account_id=seller_id, secret_key=secret_key, region='US')
    inbound_shipments = mws.InboundShipments(access_key=access_key, account_id=seller_id, secret_key=secret_key, region='US')
    inventory = mws.Inventory(access_key=access_key, account_id=seller_id, secret_key=secret_key, region='US')
    recommendations = mws.Recommendations(access_key=access_key, account_id=seller_id, secret_key=secret_key, region='US')
    sellers = mws.Sellers(access_key=access_key, account_id=seller_id, secret_key=secret_key, region='US')
    finances = mws.Finances(access_key=access_key, account_id=seller_id, secret_key=secret_key, region='US')
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
            while True:
                try:
                    report_id = self.reports.get_report_list(requestids=request_id).parsed['ReportInfo']['ReportId']['value']
                    break
                except KeyError as e:
                    print(e)
                    time.sleep(15)

            print(report_id)
            report = self.reports.get_report(report_id=report_id).parsed

            return report

    def parse_inventory_report(self, report_id):
        report = self.reports.get_report(report_id=report_id)
        print(report)
        rep = ''.join(chr(x) for x in report.parsed).split('\n')
        data = [i.split('\t') for i, in rep[1:]]

        # 0: sku, 1: asin, 2: price, 3: quantity
        headers = [i.split('\t') for i in rep[0]]

        sku_and_price = [(i[0], i[2]) for i in data if i[0] != '' and i[3] != '\r' and int(i[3].replace('\r', '')) > 0]

        return headers, sku_and_price

    def update_sku_price(self, sku, price, message_number):
        xml_file = CreateXML().generate_mws_price_xml(sku, price, message_number)
        updated = self.feeds.submit_feed(feed=xml_file, feed_type='_POST_PRODUCT_PRICING_DATA_').parsed
        return updated

    def check_feed_submission(self, feed_id):
        return self.feeds.get_feed_submission_result(feedid=feed_id)

    def get_sku_prices(self, skus):
        prices = self.products.get_competitive_pricing_for_sku(marketplaceid=self.marketplace_usa, skus=skus).parsed
        return prices


