from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .ebay_api import EbayApi
from .list_ebay_item import list_item
from orders.models import Inventory
from engine.tcgplayer_api import TcgPlayerApi
from .models import EbayListing
import math

tcgApi = TcgPlayerApi()
ebay = EbayApi()


@shared_task(name='ebay.tasks.refresh_access_token')
def refresh_access_token():
    ebay.refresh()


@shared_task(name='ebay.tasks.manage_ebay')
def manage_ebay(sku, status):
    item = Inventory.objects.get(sku=sku)

    if status == 'upload':
        if EbayListing.objects.filter(sku=sku).exists() is False:
            quantity = tcgApi.get_sku_quantity(sku)['results'][0]['quantity']
            image = tcgApi.get_card_info(tcgApi.card_info_by_sku(sku)['results'][0]['productId'])['results'][0]['imageUrl']
            price = math.ceil(item.price) - 0.01
            list_item(
                sku=sku,
                title=item.name,
                expansion=item.expansion,
                image_url=image,
                quantity=quantity,
                price=price,
                condition=item.condition,

            )

        else:
            pass
    elif status == 'remove':
        ebay.delete_ebay_item(sku)


