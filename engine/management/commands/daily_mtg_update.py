from django.core.management.base import BaseCommand
from engine.daily_mtg_rss import daily_mtg_update


class Command(BaseCommand):
    def handle(self, *args, **options):
        daily_mtg_update()

