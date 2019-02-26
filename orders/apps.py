from django.apps import AppConfig


class OrdersConfig(AppConfig):
    name = 'orders.signals'
    def ready(self):
        from orders import signals

