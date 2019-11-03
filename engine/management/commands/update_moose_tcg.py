import traceback
from django.core.management.base import BaseCommand
from orders.tasks import update_moose_tcg
from my_customs.decorators import report_error
import random
from bs4 import BeautifulSoup as B
from my_customs.functions import float_from_string, null_to_zero, check_if_foil, integers_from_string, convert_to_number_of_pages, request_pages_data
from tcg.tcg_functions import moose_price_algorithm, get_product_seller_info
import requests
from time import time
from engine.tcgplayer_api import TcgPlayerApi
from engine.models import MooseInventory
from django.core.mail import send_mail
import csv
from engine.models import MooseAutopriceMetrics

api = TcgPlayerApi('moose')


class Command(BaseCommand):
    @report_error
    def handle(self, *args, **options):
        update_moose_tcg.apply_async(que='low_priority')



