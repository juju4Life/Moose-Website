from django.core.management.base import BaseCommand
from engine.tcgplayer import new_set


class Command(BaseCommand):
    def handle(self, **options):
        user_input = input('Input Group ID: ')
        new_set(str(user_input))





