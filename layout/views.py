from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
import requests


@require_http_methods(["GET", "POST", ])
def daily_mtg_hook(request):
    template = "layout/templates/daily_mtg.html"
    context = dict()

    print(request.GET)
    challenge = request.GET.get("hub.topic")
    topic = request.GET.get("hub.challenge")
    print(topic)
    print(challenge)

    return HttpResponse(challenge)


