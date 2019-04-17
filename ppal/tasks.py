from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .paypal_api import PaypalApi

paypal_api = PaypalApi()


@shared_task(name='engine.tasks.update_paypal_token')
def update_paypal_token():
    paypal_api.get_access_token()

