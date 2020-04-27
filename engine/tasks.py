from __future__ import absolute_import, unicode_literals
from celery import shared_task
from my_customs.decorators import report_error


@shared_task(name='engine.tasks.complete_order')
@report_error
def complete_order(cart, name, email, order_number):
    pass



