from django.core.management.base import BaseCommand
from engine.tcgplayer_api import TcgPlayerApi
from django.core.mail import send_mail
from orders.models import GroupName
from my_customs.decorators import report_error

api = TcgPlayerApi('first')


class Command(BaseCommand):
    @report_error
    def handle(self, **options):
        category_ids = [1, 2, 3, 31, 56, 16, 32, 27, 17, 29, 35, 14, 22]
        count = 0

        while count < len(category_ids):
            group_ids = api.get_group_ids(offset=0, cat_id=category_ids[count])['results']

            # Check if group_is is present in database. IF not, request group info and add group to DB
            if group_ids:
                groups = GroupName.objects.values_list('group_id', flat=True)
                for i in group_ids:
                    if str(i['groupId']) not in groups:

                        new_id = GroupName(
                            group_id=i['groupId'],
                            group_name=i['name'],
                        )

                        new_id.save()

            # If empty, likely an api error, api change, or error with access key. If empty, send email notification.
            else:
                subject = 'Error retrieving api info'
                message = f"Error with api request for Get Category endpoint, or category_id {category_ids[count]}"
                email_from = 'tcgfirst.com'
                email_to = 'jermol.jupiter@gmail.com'
                send_mail(subject, message, email_from, email_to)

            count += 1


