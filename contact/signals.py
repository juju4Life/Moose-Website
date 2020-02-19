from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail


@receiver(pre_save, sender='contact.CustomerEmail')
def customer_email_reply(sender, instance, **kwargs):

    from_mail = settings.EMAIL_HOST_USER
    recipient_list = [instance.email]
    subject = 'Email response to Contact Us Form'
    message = f'Hello {instance.name}\n\n This email is in response to the following message you sent to us\n\n "{instance.message}"\n\nFrom the ' \
        f'MooseLoot '\
        f'Team:\n {instance.reply}\n\nLet us know if you have any other questions.\n\nThank you,\nMooseLoot Team'

    send_mail(
        subject=subject,
        recipient_list=recipient_list,
        from_email=from_mail,
        message=message
    )




