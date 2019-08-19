from django.core.management.base import BaseCommand
from amazon.models import FeedSubmission
from amazon.amazon_mws import MWS
from my_customs.exml import CreateXML
from django.utils import timezone

api = MWS()
x = CreateXML()


class Command(BaseCommand):
    def handle(self, *args, **options):

        # We first check to see if the latest feed submission has been successful.
        # If False, we do nothing and check again when this code block runs again.

        last_feed = FeedSubmission.objects.latest('feed_created_on')
        update_prices = True
        if last_feed.success is False:
            try:
                # If the check return is False, we request an update from MWS and update the Feed Status accordingly.
                # If it is true we continue to run the script

                check_feed_status = api.get_feed_submission_list(last_feed.feed_id)
                if check_feed_status['FeedSubmissionInfo']['FeedProcessingStatus']['value'] == '_DONE_':
                    last_feed.feed_successful_on = timezone.now()
                    last_feed.success = True
                    update_prices = True
                    last_feed.save()

                else:
                    print(check_feed_status['FeedSubmissionInfo']['FeedProcessingStatus']['value'])

            except Exception as e:
                print(e)
                pass

        if update_prices is True:
            update_feeds = []

            report_id = api.request_and_get_inventory_report('all_listings')
            if report_id is not None:

                # Inventory is separated in New or Collectible Condition
                inventory_new, inventory_collectible = api.parse_active_listings_report(report_id)
                inventory = {
                    0: inventory_new,
                    1: inventory_collectible,
                }

                count = 0
                while count <= 1:

                    # Below we page the entire inventory report in groups of 20

                    num_items = len(inventory[count])
                    start = 0
                    stop = 19

                    while num_items > 0:
                        if stop > len(inventory[count]):
                            stop = len(inventory[count])
                        items = inventory[count][start:stop]

                        skus = [i['sku'] for i in items if items]

                        # For simplicity to only loop over actual lists and avoid error when 1 object would be a string
                        # Every once in a while 1 item is not updated. To update in future

                        if len(items) > 1:
                            if count == 0:
                                prices = api.get_sku_lowest_offer(skus=skus, condition='new')
                            else:
                                prices = api.get_sku_lowest_offer(skus=skus, condition='collectible')

                            for i in prices:
                                sku = i['SellerSKU']['value']
                                try:
                                    try:
                                        competitive_price = float(i['Product']['LowestOfferListings']['LowestOfferListing'][0]['Price']['LandedPrice']['Amount']['value'])
                                    except KeyError:
                                        competitive_price = float(
                                            i['Product']['LowestOfferListings']['LowestOfferListing']['Price']['LandedPrice']['Amount']['value'])

                                    old_price = [float(i['price']) for i in items if i['sku'] == sku][0]
                                    condition = [i['condition'] for i in items if i['sku'] == sku][0]

                                    if old_price != competitive_price:

                                        if 'LikeNew' in condition['full']:
                                            competitive_price = competitive_price * .9
                                        else:
                                            competitive_price = round(competitive_price - .01, 2)

                                        # print(sku, condition['full'], old_price, competitive_price)

                                        update_feeds.append({
                                            'sku': sku,
                                            'price': competitive_price,
                                        })

                                except KeyError as e:
                                    print(e)
                                    print(sku)
                                    for each in prices:
                                        if each['SellerSKU']['value'] == sku:
                                            print(each)

                        start += 20
                        stop += 20
                        num_items -= 20
                    count += 1

                # Generate the XML file in MWS required format, then submit that file as a feed to MWS
                feed = x.generate_mws_price_xml(update_feeds)
                feed_submission = api.update_sku_price(feed)

                # Store the Feed ID and other associated information for reference. Used to check feed status.
                feed_id = feed_submission['FeedSubmissionInfo']['FeedSubmissionId']['value']
                submit_date = feed_submission['FeedSubmissionInfo']['SubmittedDate']['value']

                new_feed = FeedSubmission.objects.create(
                    success=False,
                    feed_id=feed_id,
                    feed_successful_on=submit_date,
                )

                new_feed.save()
















