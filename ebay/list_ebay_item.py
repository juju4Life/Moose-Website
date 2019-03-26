from .ebay_api import EbayApi
from .models import EbayListing
from my_customs.decorators import report_error
from django.core.mail import send_mail
from decouple import config
import math

ebay = EbayApi()


@ report_error
def list_item(sku, title, expansion, image_url, quantity, price, condition='Near Mint / Lightly Played', ebay_condition="NEW",
              fulfillment_id='33310623022',
              payment_id="24992594022",
              return_policy_id="153557924022"):

    shipping_cost = {
        '33310623022': 0,
    }
    price = math.ceil(price) - 0.01
    title = f"1x {title} - {expansion} - Magic the Gathering - Fast Shipping"
    description = f"<strong>Shipping for this item is *Fast and Free*</strong><br><br>" \
                  f"This auction is for <strong>1x {title}</strong> from the {expansion} expansion and will be in"\
                  f"<strong>{condition}</strong> condition.<br>These card(s) will be  inserted into a sleeve, top-loader, team  bag, and padded bubble-mailer "\
                  f"envelop to provide the maximum level of protection for your purchase.<br>We have many great auctions at affordable prices "\
                  f"and provide combined shipping.Be sure to check out our full inventory for the hottest deals around!<br>"\
                  f"If you have any questions or concerns, please let us know. We'll do everything we can to help.<br>"

    condition_description = 'The items in this auction are in Near Mint or Lightly Played condition with "No" or "minor" marks / edge-wear'

    ebay.create_item(sku=sku, title=title, image_url=image_url, quantity=quantity, description=description, ebay_condition=ebay_condition,
                     condition_description=condition_description)

    offer_id = ebay.create_offer(sku, price=price, quantity=quantity, category_id='38292', fulfillment_id=fulfillment_id, payment_id=payment_id,
                                 return_policy_id=return_policy_id, description=description)
    print(offer_id)
    offer_id = offer_id['offerId']

    upload = ebay.publish_offer(offer_id)
    try:
        listing_id = upload['listingId']

    except Exception as e:
        subject = f'Error listing ebay item'
        message = f'Error listing ebay item\nError: {e}\n\n Items Info:\n sku: {sku}, title: {title}, offer ID:{offer_id}'
        send_to = [config('my_email'), ]
        email_from = 'TCGFirst'
        send_mail(subject=subject, message=message, recipient_list=send_to, from_email=email_from)
        listing_id = {}

    if listing_id:
        new_listing = EbayListing(
            title=title,
            sku=sku,
            listing_id=listing_id,
            payment_policy_id=payment_id,
            offer_id=offer_id,
            category_id='38292',
            fulfillment_policy_id=fulfillment_id,
            return_policy_id=return_policy_id,
            quantity=quantity,
            price=price,
            description=description,
            format='FIXED_PRICE',
            shipping_cost=shipping_cost[fulfillment_id],

        )

        new_listing.save()

        return True

    else:
        return False



