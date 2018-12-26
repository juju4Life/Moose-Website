from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required
from ipware import get_client_ip
from django.http import HttpResponse

"""def preorder_list(request):
    return render_to_response(
        "preorder-list.html",
        {'preorder_list' : Preorder.objects.all()},
        RequestContext(request, {}),
    )
report = staff_member_required(preorder_list)"""


def get_ip(request):
    ip, is_routable = get_client_ip(request)
    if ip is None:
        return
    else:
        print(ip)
        if is_routable:
            return "public IP"
        else:
            return "Private IP Address"


def alert_change(sender, instance, created, request, **kwarg):
    if created:
        print("Account created for {}.".format(instance.name))

    else:
        print("change for {}. Credit: {}".format(instance.name, instance.credit))
