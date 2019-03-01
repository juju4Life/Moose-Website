from django.core.management.base import BaseCommand
from engine.tcgplayer_api import TcgPlayerApi
from django.core.mail import send_mail
from orders.models import Inventory
from my_customs.decorators import report_error
from datetime import date, timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError


api = TcgPlayerApi()


class Command(BaseCommand):
    def handle(self, **options):
        pass



