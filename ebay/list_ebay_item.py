from .ebay_api import EbayApi
from my_customs.decorators import report_error
from django.core.mail import send_mail
from decouple import config

ebay = EbayApi()


@ report_error
def list_item(sku, title, expansion, image_url, quantity, condition='Near Mint / Lightly Played'):
    ebay.create_item(sku, title, expansion, image_url, quantity, condition)
    offer_id = ebay.create_offer(sku, quantity=quantity, category_id='38292')['offerId']
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
        return True

    else:
        return False


