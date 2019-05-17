from django.core.management.base import BaseCommand
from engine.tcgplayer_api import TcgPlayerApi
from engine.models import Upload
from orders.models import Inventory
from datetime import date


api = TcgPlayerApi()


class Command(BaseCommand):
    def handle(self, **options):
        uploads = Upload.objects.filter(upload_date=date.today())
        for u in uploads:
            duplicate_check = uploads.filter(sku=u.sku)

            if len(duplicate_check) > 1:
                decrement = u.upload_quantity - (u.upload_quantity * 2)
                print(decrement, len(duplicate_check))

                inventory = Inventory.objects.get(sku=u.sku)

                print(api.increment_sku_quantity(inventory.sku, quantity=decrement))
                inventory.quantity -= u.upload_quantity
                inventory.save()
                u.delete()

            else:
                print(f'Just one: {len(duplicate_check)}')












