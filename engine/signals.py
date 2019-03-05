from django.dispatch import receiver
# from django.db.models.signals import post_save
from import_export.signals import post_import, post_export

# @receiver(post_save, sender='engine.Upload')


@receiver(post_import, dispatch_uid='Uploading')
def upload_items(model, **kwarg):
    from orders.tasks import task_management
    task_management(model)
    # task_management.apply_async(que='low_priority', args=(model,))

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


