from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from layout.models import PrivacyPolicy, PrivacyPolicyBlock, TermsOfService, TermsOfServiceBlock, Text
import xmltodict


def about_us(request):
    context = dict()
    template_name = 'about_us.html'
    about_us_data = Text.objects.get(clean_name='about_us')
    context['about_us'] = about_us_data

    return render(request, template_name=template_name, context=context)

# Webhook for daily mtg feed
# --> # Not currently functioning
@csrf_exempt
@require_http_methods(["GET", "POST", ])
def daily_mtg_hook(request):
    challenge = request.GET.get("hub.challenge")
    topic = request.GET.get("hub.topic")
    d = xmltodict.parse(request.body)
    return HttpResponse(challenge)


def privacy_policy(request):
    context = dict()
    template_name = 'privacy_policy.html'
    privacy_policy_info = PrivacyPolicy.objects.first()
    context['policy'] = privacy_policy_info

    privacy_policy_blocks = PrivacyPolicyBlock.objects.all()
    context['policy_blocks'] = privacy_policy_blocks

    return render(request, template_name=template_name, context=context)


def terms_of_service(request):
    context = dict()
    template_name = 'terms_of_service.html'
    terms_of_service_info = TermsOfService.objects.first()
    context['policy'] = terms_of_service_info

    terms_of_service_blocks = TermsOfServiceBlock.objects.all()
    context['policy_blocks'] = terms_of_service_blocks

    return render(request, template_name=template_name, context=context)



