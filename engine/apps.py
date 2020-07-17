from django.apps import AppConfig


class EngineConfig(AppConfig):
    name = 'engine.signals'

    def ready(self):
        from engine import signals

