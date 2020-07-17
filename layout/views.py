from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
import requests


@require_http_methods(["GET", "POST", ])
def daily_mtg_hook(request):
    template = "layout/templates/daily_mtg.html"
    context = dict()

    print(request.GET)
    print(request.POST)

    return HttpResponse("200")


