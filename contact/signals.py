from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver
from mail.mailgun_api import MailGun

mailgun = MailGun()


# Automatically send email on instance.reply save
@receiver(pre_save, sender='contact.CustomerEmail')
def customer_email_reply(sender, instance, **kwargs):
    if instance.reply:
        from_mail = settings.EMAIL_HOST_USER
        recipient_list = [instance.email]

        # --> # message / subject Template should be in backend for user edit
        subject = 'Email response to Contact Us Form'
        message = f'Hello {instance.name}\n\n This email is in response to the following inquiry you sent to us\n\n "{instance.message}"\n\nFrom the ' \
            f'MooseLoot '\
            f'Team:\n {instance.reply}\n\nLet us know if you have any other questions.\n\nThank you,\nMooseLoot Team'

        mailgun.send_mail(
            subject=subject,
            recipient_list=recipient_list,
            message=message,
        )




