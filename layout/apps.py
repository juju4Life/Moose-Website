from django.apps import AppConfig


class LayoutConfig(AppConfig):
    name = 'layout.signals'
    label = 'layout.signals'

    def ready(self):
        from layout import signals

