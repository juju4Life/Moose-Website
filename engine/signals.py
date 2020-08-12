from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

# from django.db.models.signals import post_save
# from import_export.signals import post_import, post_export


'''@receiver(post_save, sender='orders.Inventory')
def manage_inventory(instance, **kwargs):
    print(instance.update_item)
    if instance.update_item == 'remove':
        raise ValidationError(
            _('Nope, try again')
        )
    else:
        print("This works!")'''


