
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def incoming_mail_hook(request):
    if request.method == 'POST':
        print(request.POST)
        sender = request.POST.get('sender')
        recipient = request.POST.get('recipient')
        subject = request.POST.get('subject', '')

        body_plain = request.POST.get('body-plain', '')
        body_without_quotes = request.POST.get('stripped-text', '')
        # note: other MIME headers are also posted here...

        # attachments:
        if request.FILES:
            for key in request.FILES:
                file = request.FILES[key]

    return HttpResponse("200")



