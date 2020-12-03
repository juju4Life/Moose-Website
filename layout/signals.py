from django.dispatch import receiver
from django.db.models.signals import post_save


# Backend user adds sets that are foil only or non-foil only to remove incorrection information about cards
# --> # Should just be a property function of model. Much more efficient
@receiver(post_save, sender='layout.SinglePrintingSet', dispatch_uid='update_printing')
def changing_printing_value(instance, **kwargs):

    if instance.foil_only is True:
        from engine.models import MTG

        cards = MTG.objects.filter(expansion=instance.expansion)
        cards.update(foil_only=True)

    elif instance.normal_only is True:
        from engine.models import MTG

        cards = MTG.objects.filter(expansion=instance.expansion)
        cards.update(normal_only=True)

    elif instance.normal_only is False and instance.foil_only is False:
        from engine.models import MTG

        cards = MTG.objects.filter(expansion=instance.expansion)
        cards.update(normal_only=False)
        cards.update(foil_only=False)


# Change an entire set's status to Preorder = True
@receiver(post_save, sender='layout.PreorderItem', dispatch_uid='update MTG preorders')
def update_preorder_status(instance, **kwargs):
    if kwargs['created']:
        from engine.models import MTG
        cards = MTG.objects.filter(expansion=instance.expansion.group_name)
        cards.update(preorder=True)




