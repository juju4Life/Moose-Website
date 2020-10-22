from ipware import get_client_ip


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
