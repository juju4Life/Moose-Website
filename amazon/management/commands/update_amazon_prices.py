import time
from django.core.management.base import BaseCommand
from amazon.models import FeedSubmission, AmazonPriceExclusions
from amazon.amazon_mws import MWS
from my_customs.exml import CreateXML
from django.utils import timezone

api = MWS()
x = CreateXML()


class Command(BaseCommand):
    def handle(self, *args, **options):
        send_list = list()
        recipient_list = ['jermol.jupiter@gmail.com', ]  # 'Jlkelsey94@gmail.com',

        # We first check to see if the latest feed submission has been successful.
        # If False, we do nothing and check again when this code block runs.

        last_feed = FeedSubmission.objects.latest('feed_created_on')
        update_prices = False
        if last_feed.success is False:  # Add success
            try:

                # If the check return is False, we request an update from MWS and update the Feed Status accordingly.
                # If it is true we continue to run the script

                check_feed_status = api.get_feed_submission_list(last_feed.feed_id)
                if check_feed_status['FeedSubmissionInfo']['FeedProcessingStatus']['value'] == '_DONE_':
                    last_feed.feed_successful_on = timezone.now()
                    last_feed.success = True
                    last_feed.save()
                    update_prices = True
                else:
                    print(check_feed_status['FeedSubmissionInfo']['FeedProcessingStatus']['value'])

            except Exception as e:
                print(f"Error in Main Amazon MWS file: {e}")
        else:
            update_prices = True

        if update_prices is True:
            update_feeds = []
            exclude_list = AmazonPriceExclusions.objects.filter(exclude=True).values_list('sku', flat=True)
            print(f'Length of Exclude list {len(exclude_list)}')

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

                        '''
                        For simplicity to only loop over actual lists and avoid error when one object would be a string
                        Every once in a while one item is not updated. To update in future
                        '''

                        if len(items) > 1:
                            try:
                                if count == 0:
                                    prices = api.get_sku_lowest_offer(skus=skus, condition='new')
                                else:
                                    prices = api.get_sku_lowest_offer(skus=skus, condition='collectible')
                                time.sleep(1)

                            except Exception as e:
                                print(e)
                                prices = None

                            if prices is not None:
                                for i in prices:
                                    sku = i['SellerSKU']['value']
                                    price_list = list()
                                    card_num = 0

                                    '''
                                        Get the five cheapest prices from amazon (buyBox eligible listings only). Appending up to 5 and breaking while 
                                        loop when wither five prices a re appended to "price_list" or except an indexError when there are less than 
                                        five prices
                                    '''
                                    try:
                                        while len(price_list) < 5:
                                            try:
                                                competitive_price = float(
                                                    i['Product']['LowestOfferListings']['LowestOfferListing']['Price']['LandedPrice']['Amount']['value'])

                                            except TypeError:
                                                try:
                                                    competitive_price = float(i['Product']['LowestOfferListings']['LowestOfferListing'][card_num]['Price'][
                                                                                  'LandedPrice']['Amount']['value'])
                                                except IndexError:
                                                    break

                                            price_list.append(float(competitive_price))
                                            card_num += 1

                                        '''Match sku of queried Amazon inventory with current lowest listings. WIll always match if amazon price is
                                        with the 5 cheapest listings. Otherwise the current price will not be sued'''
                                        try:
                                            old_price = [float(i['price']) for i in items if i['sku'] == sku][0]
                                        except ValueError as e:
                                            print(e)
                                            print([i for i in items if i['sku'] == sku[0]])
                                            old_price = None

                                        if old_price is not None:
                                            old_price = float(old_price)

                                            # Create average price for returned lowest listings and make amazon competitive price the first result in list
                                            if price_list:
                                                average_price = sum(price_list) / len(price_list)
                                                competitive_price = price_list[0]

                                                #  Send Item details via email if price is too much lower than the average
                                                if competitive_price < average_price / 1.7:
                                                    send_list.append(f"{sku} - ${round(competitive_price, 2)}")

                                                avg_count = 1

                                                '''If the old price is equal to the low price, it means that the item belongs to our inventory or is
                                                matched with the lowest offer. If so, we change the competitive price to the next lowest in list.
                                                It is possible to make the competitive listing the same as the old_price if the two cheapest listings
                                                are the same.'''
                                                if old_price == competitive_price:
                                                    competitive_price = price_list[1]
                                                    avg_count = 2

                                                '''Check to make sure competitive price is not too low. if it is, relative to the average price, then
                                                make the competitive price the next one in the price_list. repeat until price is found or an index
                                                error due to there being zero desired prices found. Defaults to cheapest when all are below average'''
                                                while True:
                                                    # Break when avg_count would cause an index error
                                                    if avg_count > len(price_list) - 1:
                                                        break
                                                    if competitive_price < average_price / 1.3:
                                                        competitive_price = price_list[avg_count]
                                                        avg_count += 1
                                                    else:
                                                        break

                                                # Set minimum for certain user-specified cards
                                                if sku in exclude_list:
                                                    data = AmazonPriceExclusions.objects.get(sku=sku)
                                                    min_price = data.min_price
                                                    max_price = data.max_price

                                                    if competitive_price < min_price:
                                                        competitive_price = min_price

                                                    elif competitive_price > max_price:
                                                        competitive_price = max_price
                                                        if competitive_price > old_price * 1.5:
                                                            competitive_price = old_price * 1.5
                                                    data.price_metrics = price_list
                                                    data.save()

                                                else:
                                                    if competitive_price < 1.99:
                                                        competitive_price = 1.99
                                                    if competitive_price > 19.99 and competitive_price <= 22.25:
                                                        competitive_price = 19.99
                                                    card_metrics, created = AmazonPriceExclusions.objects.get_or_create(sku=sku)
                                                    card_metrics.price_metrics = price_list
                                                    card_metrics.price = competitive_price
                                                    card_metrics.exclude = False
                                                    card_metrics.save()

                                                update_feeds.append({
                                                    'sku': sku,
                                                    'price': competitive_price,
                                                })

                                            else:
                                                pass
                                                # print(sku, condition['full'], old_price, competitive_price)

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
                if update_feeds:
                    pass

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

        # send_mail(subject='Amazon Price Alerts', recipient_list=recipient_list, message="\n".join(send_list), from_email='TcgFirst')















