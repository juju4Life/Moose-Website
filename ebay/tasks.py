from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .ebay_api import EbayApi

ebay = EbayApi()


@shared_task(name='ebay.tasks.refresh_access_token')
def refresh_access_token():
    ebay.refresh()

