from decimal import Decimal

from decouple import config
from django.db.models.signals import pre_save
from django.dispatch import receiver
from sms.twilio_ import Twilio


# Receive signal each time an instance of Safe is saved or created
@receiver(pre_save, sender='administration.Safe', dispatch_uid='Safe Management')
def manage_safe(instance, **kwargs):
    from administration.models import Safe

    # Most recent Safe Balance record
    last = Safe.objects.last()

    # Since this is a pre_save signal, check if the instance has already been created
    # If it is not being created, this indicates a change need to be made to an already existing instance
    # The balance cannot be changed this way so we copy the last recorded balance
    if instance.pk:
        instance.balance = last.balance

    else:
        # Create instance. Uses custom model validators to enforce + and - is used when making deposits and withdrawals to safe
        # This makes accidental withdrawals and deposits less likely
        # string instead of integer allows for this behavior, with the caveat of needing to convert to a Decimal
        if instance.withdrawal != '0':
            instance.withdrawal = Decimal(format(Decimal(instance.withdrawal[1:]), '.2f'))
            instance.balance = last.balance - instance.withdrawal

        # ---> # Can be change to elif for slight optimization but will need to handle expected errors
        if instance.deposit != '0':
            instance.deposit = Decimal(format(Decimal(instance.deposit[1:]), '.2f'))
            instance.balance = last.balance + instance.deposit

        # Send periodic message when safe reached certain threshold
        # ---> # Threshold and message should have a model to for backend to
        if instance.balance < 2000 and last.alert is False:
            message = f"Safe balance of ${instance.balance} is below the $2000 threshold. Please visit " \
                      f"https://www.tcgfirst.com/admin/administration/safe/ to view history. username is 'management'."

            # Send message when Safe threshold is reached
            # ---> # Instead of environment variable, consider a model to hold list of phone numbers so user can edit, then loop through objects and send
            sent_1 = Twilio().send_message(config('BERNIE_PHONE_NUMBER'), message_body=message)

            if sent_1.status == 'queued' or sent_1.status == 'sent':
                instance.alert = True

        elif instance.balance > 2000 and instance.alert is True:
            instance.alert = False

        else:
            pass

        if instance.balance < 2000 and last.alert is True:
            instance.alert = True

        # Message Fails silently if message fails to send. Will attempt to send again when new record is saved








