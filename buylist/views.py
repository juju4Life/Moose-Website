
from datetime import datetime

from buylist.cart import Cart
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from engine.config import pagination
from engine.forms import AdvancedSearchForm
from engine.models import MTG
from users.forms import AddressForm, EmailForm


def buylist_home(request):
    template = 'buylist.html'
    context = {}
    response = render(None, template, context)
    visits = int(request.COOKIES.get('visits', '0'))
    if 'last_visit' in request.COOKIES:
        last_visit = request.COOKIES['last_visit']
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
        if (datetime.now() - last_visit_time).days > 0:
            response.set_cookie('visits', visits + 1)
            response.set_cookie('last_visit', datetime.now())
        response.set_cookie('last_visit', datetime.now())
    return response


def buylist_page(request):
    context = dict()
    template_name = 'buylist.html'
    query = request.GET.get('q')
    form = AdvancedSearchForm()
    if query:
        results = MTG.objects.filter(name=query)
        pages = pagination(request, results, 20)
        context['items'] = pages[0]
        context['page_range'] = pages[1]
    else:
        results = MTG.objects.filter(buylist=True)
        pages = pagination(request, results, 20)
        context["items"] = pages[0]
        context["page_range"] = pages[1]
    context['form'] = form
    return render(request, template_name=template_name, context=context)


def search(request):
    template = 'search_result_buylist.html'
    query = request.GET.get('q')
    if query:
        results = object.objects.filter(Q(name__icontains=query))
        pages = pagination(request, results, 20)
        context = {'items': pages[0], 'page_range': pages[1]}
        return render(request, template, context)
    else:
        return redirect('buylist_home')


def add_to_cart(request, product_id):
    quantity = request.POST.get('quantity')
    product = get_object_or_404(MTG, product_id=product_id)
    cart = Cart(request)
    cart.add(product, product.buylist_price, product.expansion, quantity)
    return redirect('buylist_cart')


def update_cart(request, product_id):
    if request.POST:
        cart = Cart(request)
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        cart.update(product_id=product_id, price=price, new_value=quantity)

    return redirect("buylist_cart")


def get_cart(request):
    cart = Cart(request)
    for c in cart:
        print(c)
    length = cart.cart_length
    sub_total = cart.total_price
    return render(request, 'buylist_cart.html', {'cart': cart, 'length': length, 'sub_total': sub_total})


def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect('buylist_cart')


def clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('buylist_cart')


def confirm_info(request):
    context = dict()
    template_name = "buylist_confirm_info.html"

    address_form = AddressForm()
    email_form = EmailForm()
    context["address_form"] = address_form
    context["email_form"] = email_form

    return render(request, template_name=template_name, context=context)


def checkout(request):
    context = dict()
    template_name = "buylist_checkout.html"
    if request.user.is_authenticated is False:
        messages.warning(request, "You must be logged in to submit a buylist order")
        return redirect("login")
    else:
        cart = Cart(request)
        context["cart"] = cart
    return render(request, template_name=template_name, context=context)

