from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

# from django.db.models.signals import post_save
# from import_export.signals import post_import, post_export


@receiver(pre_save, sender='engine.MTG')
def manage_pages(instance, **kwargs):
    if instance.normal_buylist:
        pass

    if instance.sick_deal:
        pass


