from __future__ import absolute_import, unicode_literals
from celery import shared_task
from customer.secrets import Secrets
from engine.tcgplayer_api import TcgPlayerApi
from engine.tcg_credentials import Credentials
from datetime import datetime
from django.core.mail import send_mail


tcg = TcgPlayerApi('first')
credentials = Credentials()


@shared_task(name='customer.tasks.alert')
def alert(ip, obj_name, obj_credit, obj_id):
    time_of_change = datetime.now()
    ip_list = ['73.201.91.50', '208.54.70.156', '99.203.1.55', '2600:1:9103:7512:245a:71d4:7', '172.56.7.5', '66.87.112.131', '172.58.110.200']
    if str(ip) not in ip_list:
        subject = 'Odd Activity Detected in Store Credit Database'
        message = "A change was made to the store credit system from an unauthorized Source.\n" \
                  "TIME: {}\n" \
                  "IP ADDRESS: {}\n" \
                  "Name: {}\n" \
                  "Current Store Credit: {}\n" \
                  "Unique ID: {}\n".format(
                        time_of_change, ip, obj_name, obj_credit, obj_id,
        )

        emailFrom = 'DATABASE ALERTS'
        emailTo = ['jermol@mtgfirst.com']
        send_mail(subject, message, emailFrom, emailTo, fail_silently=True)


@shared_task(name='customer.tasks.update_tcg_key')
def update_tcg_key():
    credentials.new_bearer_token()
