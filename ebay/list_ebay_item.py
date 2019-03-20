from .ebay_api import EbayApi

ebay = EbayApi()


def list_item(sku):
    ebay.create_item(sku)
    offer_id = ebay.create_offer(sku, quantity=5, category_id='38292')['offerId']
    print(ebay.publish_offer(offer_id))
