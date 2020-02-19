from uuid import uuid1
from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactForm
from .models import CustomerEmail


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

            message = f'You have submitted the message below\n\n{comment}\n\n A team member will review your message shortly. The expected reply window is 24 hours'
            emailTo = [email, ]
            send_mail(subject, message, from_email=settings.EMAIL_HOST_USER, recipient_list=emailTo, fail_silently=True)
            context['confirm_message'] = 'confirmed'
            context['form'] = None
        else:
            context['confirm_message'] = 'unconfirmed'
            messages.warning(request, 'There was an error while try to submit your message. Please try again later')
            return render(request, template, context)

    else:
        return render(request, template, context)


def policy(request):
    return render(request, 'privacy-policy.html')



