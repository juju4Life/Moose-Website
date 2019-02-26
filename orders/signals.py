from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender='orders.models.Inventory')
def manage_inventory(instance, **kwargs):
    print(instance.name)


