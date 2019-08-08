from django.shortcuts import render, render_to_response
from django.shortcuts import get_object_or_404
from .cart import Cart
from django.shortcuts import redirect
from datetime import datetime
from engine.config import pagination
from django.db.models import Q
from .forms import buylistForm
from django.conf import settings
from django.core.mail import send_mail


def buylist_home(request):
    print(request.path, request.get_full_path)
    template = 'buylist.html'
    context = {}
    cart = Cart(request)
    response = render_to_response(template, context)
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
    buylist = ""
    pages = pagination(request, buylist, 21)
    return render(request, 'buylist-page.html', {'items': pages[0], 'page_range': pages[1]})


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
    products = get_object_or_404(object, id=product_id)
    cart = Cart(request)
    cart.add(products, products.price, products.set_name, quantity)
    return redirect('buylist_cart')


def get_cart(request):
    cart = Cart(request)
    length = cart.cart_length
    sub_total = cart.total_price
    total = [i['quantity'] * i['price'] for i in cart]
    cart_data = zip(cart, total)
    return render(request, 'buylist-cart.html', {'cart':cart_data, 'length':length, 'sub_total':sub_total})


def remove_from_cart(request, product_id):
    products = ''
    cart = Cart(request)
    cart.remove(products)
    return redirect('buylist_cart')


def clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('buylist_cart')


def checkout(request):
    if request.POST:
        cart = Cart(request)
        sorted_list = sorted(cart, key=lambda k: k['set_name'])
        shopping_cart = ["{}x {} | {} for | ${} each".format(i['quantity'], i['product'], i['set_name'], i['price']) for i in sorted_list]
        total = [i['quantity'] * i['price'] for i in sorted_list]
        final_price = (format(sum(i['quantity'] * i['price'] for i in cart), '.2f'))
        sub_total = cart.total_price
        email_cart = '\n'.join(shopping_cart)
        cart_data = zip(cart,total)
        length = len(sorted_list)

        title = ''
        form = buylistForm(request.POST or None)
        confirm_message = None

        if form.is_valid():
            name = form.cleaned_data['name']
            notes = form.cleaned_data['notes']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            extension = form.cleaned_data['extension']
            address = form.cleaned_data['address']
            address_2 = form.cleaned_data['address_2']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zip_code = form.cleaned_data['zip_code']
            payment = form.cleaned_data['payment']
            order_number = 'Q43yd765mtg'


            subject = 'Buylist Order'
            message = 'Name: {0} \nOrder Number: {1}\nEmail: {2}\nPhone Number: {3}, ext:{4}\nPayment Type: {5}\n Address info:\n{6} |' \
                      '{7}\n{8},{9} {10}\n\nCustomer Note:\n{11}\n\nOrder:\n{12}\n Total Payment: {13} '.format(name, order_number, email,
                                                                                          phone_number, extension,
                                                                                          payment, address, address_2,
                                                                                          city, state, zip_code, notes,
                                                                                          email_cart, final_price)
            emailFrom = form.cleaned_data['email']
            emailTo = [settings.EMAIL_HOST_USER]
            send_mail(subject, message, emailFrom, emailTo, fail_silently=True)
            title = 'Your order has been placed\n' \
                    'Please ensure that your order is sorted exactly as it appears in you confirmation email.\n' \
                    'MTG First Game Center\n' \
                    'ATTN: Buyer\n' \
                    '7602 Baltimore Annapolis Blvd.\n' \
                    'Glen Burnie, MD 21060' \
                    'Thank you for shopping with MTG First'
            confirm_message = 'You will receive an email confirmation shortly'
            form = None
            cart.clear()
        return render(request, 'buylist-checkout.html', {'cart': cart_data, 'length': length,
                                                 'title': title, 'form': form, 'confirm_message': confirm_message, 'sub_total':sub_total})

