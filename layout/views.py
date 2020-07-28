from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import xmltodict


@csrf_exempt
@require_http_methods(["GET", "POST", ])
def daily_mtg_hook(request):
    print(type(request.body))
    print(request.body)

    challenge = request.GET.get("hub.challenge")
    topic = request.GET.get("hub.topic")

    d = xmltodict.parse(request.body)
    print(json.dumps(d, indent=4))
    return HttpResponse(challenge)



