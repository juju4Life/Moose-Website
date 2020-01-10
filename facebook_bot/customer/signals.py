from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from customer.models import Customer


@receiver(pre_save, sender=Customer, dispatch_uid='tracker')
def track_credit(instance, **kwarg):
    from buylist.models import StoreCredit
    name = instance.name
    print(name)
    print(kwarg)
    print('is it working....')
    credit = instance.credit
    n = StoreCredit(
        name=name,
        store_credit=credit,
    )

    # task_management(model)



