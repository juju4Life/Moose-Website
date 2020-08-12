from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CustomerConfig(AppConfig):
    name = 'customer.signals'
    label = 'customer.signals'

    def ready(self):
        from customer import signals


