from django.apps import AppConfig


class ContactConfig(AppConfig):
    name = 'contact.signals'
    label = 'contact.signals'

    def ready(self):
        import contact.signals
