from django.core.management.base import BaseCommand
from customer.facebook_listen import ListenBot
from customer.secrets import Secrets


class Command(BaseCommand):
    def handle(self, **options):
        client = ListenBot(Secrets.facebook_email, Secrets.facebook_password)
        while True:
            if not client.isLoggedIn():
                client = ListenBot(Secrets.facebook_email, Secrets.facebook_password)
            client.listen(end_time=70)





