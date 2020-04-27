from __future__ import absolute_import, unicode_literals
from celery import shared_task
from tcg.price_alogrithm import *
from engine.tcgplayer_api import TcgPlayerApi
from engine.models import MTG
from my_customs.decorators import report_error
from django.core.mail import send_mail
from datetime import date
from django.core.exceptions import ObjectDoesNotExist
from scryfall_api import get_image
from engine.update_moose_tcg import moose_price


api = TcgPlayerApi('moose')


@shared_task(name='orders.tasks.update_moose_tcg')
def update_moose_tcg():
    moose_price()

