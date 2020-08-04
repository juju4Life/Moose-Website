from __future__ import absolute_import, unicode_literals
from celery import shared_task
from engine.models import MTG, MTGUpload
from django.db import transaction
from my_customs.decorators import report_error


@shared_task(name='engine.tasks.complete_order')
@report_error
def complete_order(cart, name, email, order_number):
    pass


@shared_task(name="engine.tasks.upload_cards")
def upload_mtg_cards():
    with transaction.atomic():
        to_be_uploaded = MTGUpload.objects.filter(upload_status=False)
        for item in to_be_uploaded:
            product = MTG.objects.get(product_id=item.product_id)
            product.normal_clean_stock += item.normal_clean_stock
            product.normal_played_stock += item.normal_played_stock
            product.normal_heavily_played_stock += item.normal_heavily_played_stock
            product.foil_clean_stock += item.foil_clean_stock
            product.foil_played_stock += item.foil_played_stock
            product.foil_heavily_played_stock += item.foil_heavily_played_stock
            product.save()
            item.upload_status = True
            item.save()




