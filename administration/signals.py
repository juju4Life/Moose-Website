from decimal import Decimal
from django.db.models.signals import pre_save
from django.dispatch import receiver
from sms.twilio_ import Twilio


@receiver(pre_save, sender='administration.Safe', dispatch_uid='Safe Management')
def manage_safe(instance, **kwargs):
    from administration.models import Safe
    last = Safe.objects.last()

    if instance.withdrawal != '0':
        instance.withdrawal = Decimal(format(Decimal(instance.withdrawal[1:]), '.2f'))
        instance.balance -= instance.withdrawal
        instance.balance = last.balance - instance.withdrawal

    if instance.deposit != '0':
        instance.deposit = Decimal(format(Decimal(instance.deposit[1:]), '.2f'))
        instance.balance += instance.deposit
        instance.balance = last.balance + instance.deposit

    if instance.balance < 2000 and last.alert is False:

        message = f"Safe balance of ${instance.balance} is below the $2000 threshold. Please visit " \
                  f"https://www.tcgfirst.com/admin/administration/safe/ to view history. username is 'management'."

        sent_1 = Twilio().send_message(4435702148, message_body=message)
        Twilio().send_message(4434741655, message_body=message)

        if sent_1.status == 'queued' or sent_1.status == 'sent':
            instance.alert = True

    elif instance.balance > 2000 and instance.alert is True:
        instance.alert = False

    else:
        pass

    if instance.balance < 2000 and last.alert is True:
        instance.alert = True








