from decimal import Decimal
from django.db.models.signals import pre_save
from django.dispatch import receiver


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





