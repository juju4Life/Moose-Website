from django.core.management.base import BaseCommand
from engine.tcg_credentials import Credentials

tcg = Credentials()


class Command(BaseCommand):
    def handle(self, **options):
        tcg.new_bearer_token()


