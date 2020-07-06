from django.core.management.base import BaseCommand
from ppal.paypal_setup import PayPal


paypal = PayPal()


class Command(BaseCommand):
    def handle(self, *args, **options):
        # order_id = paypal.create_order()
        # print(order_id)
        # paypal.capture_order("7V136933JN047743G")
        paypal.get_order("6JC94749LU257173A")


