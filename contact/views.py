
from uuid import uuid1

from contact.forms import ContactForm
from contact.models import CustomerEmail
from django.shortcuts import render
from django.contrib import messages
from mail.mailgun_api import MailGun


mailgun = MailGun()


def contact(request):
    form = ContactForm(request.POST or None)
    confirm_message = None
    context = {'form': form, 'confirm_message': confirm_message}
    template = 'contact.html'

    if form.is_valid():
        name = form.cleaned_data['name']
        comment = form.cleaned_data['comment']
        subject = form.cleaned_data['subject']
        order_number = form.cleaned_data['order_number']
        email = form.cleaned_data['email']
        uuid = str(uuid1())

        new_email = CustomerEmail(
            name=name,
            message=comment,
            subject=subject,
            order_number=order_number,
            email=email,
            uuid=uuid,
        )

        new_email.save()

        if CustomerEmail.objects.filter(uuid=uuid).exists():

            # --> # Message to be placed in model for backend user customization
            message = f'You have submitted the following message to MooseLoot.com\n\n"{comment}"\n\n We look forward to helping you with any problems or ' \
                f'questions that you may have. A team member will review you order shortly. Expect to hear back from us within 24 hours.\n\nThank you for \
contacting MooseLoot.com,\nMooseLoot Team'

            email_to = [email, ]

            mailgun.send_mail(
                recipient_list=email_to, subject=subject, message=message,
            )

            context['confirm_message'] = 'confirmed'
            context['form'] = None
            return render(request, template, context)
        else:
            context['confirm_message'] = 'unconfirmed'
            messages.warning(request, 'There was an error while try to submit your message. Please try again later')
            return render(request, template, context)

    else:
        return render(request, template, context)


