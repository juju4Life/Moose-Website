from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    def handle(self, *args, **options):
        with connection.cursor() as cursor:

            print(
                cursor.execute(
                    'show table status from MTG;'
                )
            )









