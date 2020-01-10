from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

# from django.db.models.signals import post_save
# from import_export.signals import post_import, post_export


# @receiver(post_save, sender='engine.Upload')


@receiver(pre_save, sender='customer.Customer', dispatch_uid='Uploading')
def upload_items(instance, **kwarg):
    from decimal import Decimal
    from buylist.models import StoreCredit

    if instance.credit > instance.last_credit:
        diff = instance.credit - Decimal(instance.last_credit)

        name = instance.name
        store_credit = diff

        n = StoreCredit(
            name=name,
            store_credit=store_credit
        )

        n.save()

    instance.last_credit = instance.credit
    instance.employee_initial = ''

    # from orders.tasks import task_management
    # task_management(model)
    # task_management.apply_async(que='low_priority')

# post_save.connect(upload_items, sender=Events)


'''@receiver(post_save, sender='orders.Inventory')
def manage_inventory(instance, **kwargs):
    print(instance.update_item)
    if instance.update_item == 'remove':
        raise ValidationError(
            _('Nope, try again')
        )
    else:
        print("This works!")'''


