from django.core.management.base import BaseCommand
from engine.tcgplayer_api import TcgPlayerApi
from django.core.mail import send_mail

api = TcgPlayerApi()


class Command(BaseCommand):
    def handle(self, **options):
        category_ids = [1, 2, 3, 31, 56, 16, 32, 27, 17, 29, 35, 14, 22]
        count = 0

        while count < len(category_ids):
            group_ids = api.get_group_ids(offset=0, cat_id=category_ids[count])['results']

            # If empty, likely an api error, api change, or error with access key. If empty, send email notification.
            if group_ids:
                pass

            else:
                subject = 'Error retrieving api info'
                message = f"Error with api request for Get Category endpoint, or category_id {category_ids[count]}"
                email_from = 'tcgfirst.com'
                email_to = 'jermol.jupiter@gmail.com'
                send_mail(subject, message, email_from, email_to)

            count += 1


