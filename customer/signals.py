
from django.db.models import Sum
from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender='customer.Customer', dispatch_uid='tracking')
def track_store_credit(instance, **kwarg):
    from decimal import Decimal
    from buylist.models import StoreCredit
    from customer.models import Customer

    if instance.credit > instance.last_credit:
        diff = instance.credit - Decimal(instance.last_credit)

        name = instance.name
        store_credit = diff
        current_credit_total = Customer.objects.aggregate(total_credit=Sum("credit"))

        n = StoreCredit(
            name=name,
            store_credit=store_credit,
            total=current_credit_total["total_credit"],
        )
        n.save()

    instance.last_credit = instance.credit
    instance.employee_initial = ''



