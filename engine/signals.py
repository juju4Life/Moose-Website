from django.dispatch import receiver
# from django.db.models.signals import post_save
from import_export.signals import post_import, post_export


# @receiver(post_save, sender='engine.Upload')


@receiver(post_import, dispatch_uid='Uploading')
def upload_items(model, **kwarg):
    from orders.tasks import task_management
    # task_management(model)
    task_management.apply_async(que='low_priority')

# post_save.connect(upload_items, sender=Events)


def show_me_the_money(sender, **kwargs):
    from paypal.standard.models import ST_PP_COMPLETED
    from paypal.standard.ipn.signals import valid_ipn_received

    ipn_obj = sender
    print(ipn_obj)
    print(ipn_obj.receiver_email)
    print(kwargs)
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # WARNING !
        # Check that the receiver email is the same we previously
        # set on the `business` field. (The user could tamper with
        # that fields on the payment form before it goes to PayPal)
        if ipn_obj.receiver_email != "mtgfirststore-facilitator@gmail.com":
            # Not a valid payment
            return

        # ALSO: for the same reason, you need to check the amount
        # received, `custom` etc. are all what you expect or what
        # is allowed.

        # Undertake some action depending upon `ipn_obj`.
        if ipn_obj.custom == "premium_plan":
            price = ...
        else:
            price = ...

        if ipn_obj.mc_gross == price and ipn_obj.mc_currency == 'USD':
            ...
    else:
        ...

    valid_ipn_received.connect(show_me_the_money)



'''@receiver(post_save, sender='orders.Inventory')
def manage_inventory(instance, **kwargs):
    print(instance.update_item)
    if instance.update_item == 'remove':
        raise ValidationError(
            _('Nope, try again')
        )
    else:
        print("This works!")'''


