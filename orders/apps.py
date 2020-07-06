from django.apps import AppConfig


class OrderConfig(AppConfig):
    name = 'orders.signals'
    label = 'orders.signals'

    def ready(self):
        from orders import signals


