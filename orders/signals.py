from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save


@receiver(pre_save, sender='orders.Order', dispatch_uid='orders')
def process_order(instance, **kwarg):
    print(instance.order_number, instance.name)

