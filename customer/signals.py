
from django.db.models import Sum
from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender='customer.Customer', dispatch_uid='tracking')
def track_store_credit(instance, **kwarg):
    from decimal import Decimal
    from customer.models import StoreCredit
    from customer.models import Customer
    positive_diff = 0
    negative_diff = 0

    # Change value for store credit added
    if instance.credit > instance.last_credit:
        positive_diff = instance.credit - Decimal(instance.last_credit)

    # Change value for store credit used
    elif instance.credit < instance.last_credit:
        negative_diff = Decimal(instance.last_credit) - instance.credit

    name = instance.name

    current_credit_total = Customer.objects.aggregate(total_credit=Sum("credit"))

    n = StoreCredit(
        name=name,
        store_credit=positive_diff,
        used_credit=negative_diff,
        total=current_credit_total["total_credit"],
    )
    n.save()

    instance.last_credit = instance.credit
    instance.employee_initial = ''



