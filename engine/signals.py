from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save, sender='engine.MTG')
def manage_pages(instance, **kwargs):
    from buylist.models import HotListCards
    from engine.models import SickDeal
    if instance.normal_buylist:
        pass

    if instance.sick_deal and instance.sick_deal_percentage > 0:
        item, created = SickDeal.objects.get_or_create(
            product_id=instance.product_id,
            name=instance.name,
            expansion=instance.expansion,
            printing='',
        )

        item.price = instance.sick_deal_percentage
        item.save()

    # Non-foil Hotlist card
    if instance.normal_hotlist and instance.normal_hotlist_price > 0:

        item, created = HotListCards.objects.get_or_create(
            product_id=instance.product_id,
            name=instance.name,
            expansion=instance.expansion,
        )

        item.price = instance.normal_hotlist_price
        item.image_url = instance.image_url
        item.save()

    # Foil Hotlist Cards
    if instance.foil_hotlist and instance.foil_hotlist_price > 0:
        item, created = HotListCards.objects.get_or_create(
            product_id=instance.product_id,
            name=instance.name,
            expansion=instance.expansion,
        )

        item.price = instance.foil_hotlist_price
        item.image_url = instance.image_url
        item.save()


