from django.dispatch import receiver
from django.db.models.signals import post_save

# When certain fields on main MTG model is saved, update related models
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

        )
        
        item.image_url = instance.image_url
        item.sick_deal_percentage = instance.sick_deal_percentage
        item.sick_deal = instance.sick_deal
        item.normal_clean_price = instance.normal_clean_price
        item.normal_clean_stock = instance.normal_clean_stock
        item.normal_played_price = instance.normal_played_price
        item.normal_played_stock = instance.normal_played_stock
        item.normal_heavily_played_price = instance.normal_heavily_played_price
        item.normal_heavily_played_stock = instance.normal_heavily_played_stock

        item.foil_clean_price = instance.foil_clean_price
        item.foil_clean_stock = instance.foil_clean_stock
        item.foil_played_price = instance.foil_played_price
        item.foil_played_stock = instance.foil_played_stock
        item.foil_heavily_played_price = instance.foil_heavily_played_price
        item.foil_heavily_played_stock = instance.foil_heavily_played_stock

        item.save()

    # Non-foil Hotlist card
    if instance.normal_hotlist and instance.normal_hotlist_price > 0:

        item, created = HotListCards.objects.get_or_create(
            product_id=instance.product_id,
            name=instance.name,
            expansion=instance.expansion,
            release_date=instance.release_date,
        )

        item.image_url = instance.image_url
        item.normal_hotlist = item.normal_hotlist
        item.normal_hotlist_price = item.normal_hotlist_price
        item.normal_buylist = item.normal_buylist
        item.normal_buylist_price = item.normal_buylist_price
        item.normal_buylist_max_quantity = item.normal_buylist_max_quantity
        item.save()

    # Foil Hotlist Cards
    if instance.foil_hotlist and instance.foil_hotlist_price > 0:
        item, created = HotListCards.objects.get_or_create(
            product_id=instance.product_id,
            name=instance.name,
            expansion=instance.expansion,
            release_date=instance.release_date,
        )

        item.image_url = instance.image_url
        item.foil_hotlist = item.foil_hotlist
        item.foil_hotlist_price = item.foil_hotlist_price
        item.foil_buylist = item.foil_buylist
        item.foil_buylist_price = item.foil_buylist_price
        item.foil_buylist_max_quantity = item.foil_buylist_max_quantity
        item.save()


