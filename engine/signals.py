from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save, sender='engine.MTG')
def manage_pages(instance, **kwargs):
    from buylist.models import HotList
    if instance.normal_buylist:
        pass

    if instance.sick_deal and instance.sick_deal_price > 0:
        pass

    if instance.hotlist and instance.hotlist_price > 0:

        item, created = HotList.objects.get_or_create(
            name=instance.name,
            expansion=instance.expansion,
            image=instance.image,
            price=instance.hotlist_price,


        )

