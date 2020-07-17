from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save


def handle_order(instance):
    from orders.admin_actions import OrderAction
    from orders.models import CompletedOrder, PullingOrder, ReadyToShipOrder, Order

    if instance.order_action == "cancel":
        OrderAction().process_instance(instance=instance, obj=CompletedOrder, order_status="canceled")

    elif instance.order_action == "ship":
        OrderAction().process_instance(instance=instance, obj=CompletedOrder, order_status="shipped")

    elif instance.order_action == "pull":
        OrderAction().process_instance(instance=instance, obj=PullingOrder, order_status="")

    elif instance.order_action == "ready_to_ship":
        OrderAction().process_instance(instance=instance, obj=ReadyToShipOrder, order_status="")

    elif instance.order_action == "open_order":
        OrderAction().process_instance(instance=instance, obj=Order, order_status="")


@receiver(pre_save, sender='orders.CompletedOrder', dispatch_uid='completed')
@receiver(pre_save, sender='orders.PendingPaymentOrder', dispatch_uid='pending')
@receiver(pre_save, sender='orders.ReadyToShipOrder', dispatch_uid='ready_to_ship')
@receiver(pre_save, sender='orders.PullingOrder', dispatch_uid='pulled_orders')
@receiver(pre_save, sender='orders.Order', dispatch_uid='orders')
def process_order(instance, **kwarg):
    handle_order(instance)


@receiver(post_save, sender='orders.PendingPaymentOrder', dispatch_uid='pending')
@receiver(post_save, sender='orders.ReadyToShipOrder', dispatch_uid='ready_to_ship')
@receiver(post_save, sender='orders.PullingOrder', dispatch_uid='pulled_orders')
@receiver(post_save, sender='orders.Order', dispatch_uid='orders')
def delete_order_object(instance, **kwargs):
    if instance.order_action != "":
        instance.delete()


