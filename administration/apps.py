from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AdministrationConfig(AppConfig):
    name = 'administration.signals'
    label = 'administration.signals'

    def ready(self):
        from administration import signals


