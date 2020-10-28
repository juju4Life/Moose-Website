from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from twilio.twiml.messaging_response import MessagingResponse


@csrf_exempt
def sms_response(request):
    # Start our TwiML response
    resp = MessagingResponse()

    # Add a text message
    msg = resp.message("Karakas\n"
                       "Eternal Masters\n"
                       "$35\n"
                       "____________________\n"
                       "Bitterblossom\n"
                       "Morningtide\n"
                       "$25\n"
                       "____________________\n"
                       "Karakas\n"
                       "Eternal Masters\n"
                       "$35\n"
                       "____________________\n"
                       "Bitterblossom\n"
                       "Morningtide\n"
                       "$25\n"
                       "____________________\n"
                       "Karakas\n"
                       "Eternal Masters\n"
                       "$35\n"
                       "____________________\n"
                       "Bitterblossom\n"
                       "Morningtide\n"
                       "$25\n"
                       "____________________\n"
                       "Karakas\n"
                       "Eternal Masters\n"
                       "$35\n"
                       "____________________\n"
                       "Bitterblossom\n"
                       "Morningtide\n"
                       "$25\n"
                       "____________________\n"
                       "Karakas\n"
                       "Eternal Masters\n"
                       "$35\n"
                       "____________________\n"
                       "Bitterblossom\n"
                       "Morningtide\n"
                       "$25\n"
                       "____________________\n"
                       "Karakas\n"
                       "Eternal Masters\n"
                       "$35\n"
                       "____________________\n"
                       "Bitterblossom\n"
                       "Morningtide\n"
                       "$25\n"
                       "____________________\n"
                       "Karakas\n"
                       "Eternal Masters\n"
                       "$35\n"
                       "____________________\n"
                       "Bitterblossom\n"
                       "Morningtide\n"
                       "$25\n"
                       "____________________\n"
                       "Karakas\n"
                       "Eternal Masters\n"
                       "$35\n"
                       "____________________\n"
                       "Bitterblossom\n"
                       "Morningtide\n"
                       "$25\n"
                       "____________________\n"
                       "Karakas\n"
                       "Eternal Masters\n"
                       "$35\n"
                       "____________________\n"
                       "Bitterblossom\n"
                       "Morningtide\n"
                       "$25\n"
                       "____________________\n"
                       "Karakas\n"
                       "Eternal Masters\n"
                       "$35\n"
                       "____________________\n"
                       "Bitterblossom\n"
                       "Morningtide\n"
                       "$25\n"
                       "____________________\n"
                       )

    # Add a picture message
    #msg.media("https://demo.twilio.com/owl.png")

    return HttpResponse(str(resp))

