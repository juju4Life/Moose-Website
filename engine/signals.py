from django.dispatch import receiver
from django.db.models.signals import pre_save
from import_export.signals import post_import, post_export

# @receiver(post_save, sender='engine.Upload')


@receiver(post_import, dispatch_uid='balabala...')
def upload_items(model, **kwarg):
    from tcg.price_and_upload import task_management
    task_management(model)

# post_save.connect(upload_items, sender=Events)

