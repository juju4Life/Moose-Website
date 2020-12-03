from __future__ import absolute_import, unicode_literals

from datetime import datetime

from celery import shared_task
from engine.tcgplayer_api import TcgPlayerApi
from engine.tcg_credentials import Credentials
from mail.mailgun_api import MailGun


tcg = TcgPlayerApi('moose')
credentials = Credentials()
mailgun = MailGun()


# Task to create asynchronous task to check IP of address of a client that made a change to a customer's store credit if it's not in accepted IP address list
# --> # Currently not used
@shared_task(name='customer.tasks.alert')
def alert(ip, obj_name, obj_credit, obj_id):
    time_of_change = datetime.now()
    ip_list = list()
    if str(ip) not in ip_list:
        # --> # Subject / message added to model for backend users to customize
        subject = 'Odd Activity Detected in Store Credit Database'
        message = "A change was made to the store credit system from an unauthorized Source.\n" \
                  "TIME: {}\n" \
                  "IP ADDRESS: {}\n" \
                  "Name: {}\n" \
                  "Current Store Credit: {}\n" \
                  "Unique ID: {}\n".format(
                        time_of_change, ip, obj_name, obj_credit, obj_id,
        )
        recipient_list = list()
        mailgun.send_mail(subject=subject, recipient_list=recipient_list, message=message)


# Update TCG Player key for API access
@shared_task(name='customer.tasks.update_tcg_key')
def update_tcg_key():
    credentials.new_bearer_token()
