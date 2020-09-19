
from datetime import datetime
from decimal import Decimal

from buylist.cart import Cart
from buylist.forms import BuylistPaymentType
from buylist.grade_price_buylist_card import grade
from buylist.models import BuylistSubmission
from customer.models import Customer
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from engine.config import pagination
from engine.forms import AdvancedSearchForm
from engine.models import MTG, MTGUpload
from mail.mail_templates import customer_info_template, ordered_items_template, company_buylist_shipping_info
from mail.mailgun_api import MailGun
from my_customs.functions import format_cart_for_text_field_storage, create_random_id, split_text_field_string_for_orders, change_order_status
from users.forms import AddressForm
mailgun = MailGun()


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
        results = MTG.objects.filter(normal_buylist=True, foil_buylist=True)
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
    name = request.POST.get('name')
    expansion = request.POST.get('expansion')
    language = request.POST.get('language')
    quantity = request.POST.get('quantity')
    printing = request.POST.get('printing')
    max_quantity = request.POST.get('max_quantity')
    price = request.POST.get('price')
    total = Decimal(price) * int(quantity)
    cart = Cart(request)
    cart.add(
        product_id=product_id,
        name=name,
        expansion=expansion,
        condition="clean",
        printing=printing,
        price=price,
        language=language,
        total=total,
        max_quantity=max_quantity,
        quantity=quantity,
    )

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


def confirm_info(request):
    context = dict()
    template_name = "buylist_confirm_info.html"
    if request.user.is_authenticated is False:
        messages.warning(request, "You must be logged in to submit a buylist order")
        return redirect("login")
    else:
        cart = Cart(request)

        if request.POST.get("submit_order"):
            address_form = AddressForm(request.POST)
            payment_form = BuylistPaymentType(request.POST)

            if address_form.is_valid() and payment_form.is_valid():
                notes = request.POST.get('notes')
                email = request.user.email
                customer = Customer.objects.get(email=email)
                name = address_form.cleaned_data["name"]
                address_line_1 = address_form.cleaned_data["address_line_1"]
                address_line_2 = address_form.cleaned_data["address_line_2"]
                city = address_form.cleaned_data["city"]
                state = address_form.cleaned_data["state"]
                zip_code = address_form.cleaned_data["zip_code"]
                payment_type = payment_form.cleaned_data["payment_type"]
                paypal_email = payment_form.cleaned_data["paypal_email"]
                buylist_number = create_random_id(8)

                if payment_type == "store_credit":
                    total = round(cart.total_price * Decimal(1.3), 2)
                else:
                    total = cart.total_price

                order_string = format_cart_for_text_field_storage(cart=cart, order_number=buylist_number, payment_type=payment_type,
                                                                  paypal_email=paypal_email, total_price=cart.total_price, store_credit_total=total)

                seller_review_grading = True if request.POST.get('seller_verify') else False

                new_buylist_sub = BuylistSubmission(
                    buylist_order=order_string,
                    buylist_number=buylist_number,
                    buylist_status="Not Received",
                    payment_type=payment_type,
                    paypal_email=paypal_email,
                    name=name,
                    email=email,
                    address_line_1=address_line_1,
                    address_line_2=address_line_2,
                    city=city,
                    state=state,
                    zip_code=zip_code,
                    total=total,
                    notes=notes,
                    order_url=f"{request.get_host()}/buylist/admin/order/{buylist_number}/",
                    seller_review_grading=seller_review_grading,


                )
                new_buylist_sub.save()

                customer.buylist_submissions = customer.buylist_submissions + order_string
                customer.save()
                customer_order_info_template = customer_info_template(
                    order_type="Buylist ",
                    order_number=buylist_number,
                    name=name,
                    address_line_1=address_line_1,
                    address_line_2=address_line_2,
                    city=city,
                    state=state,
                    zip_code=zip_code,
                    payment_type=payment_type,
                    paypal_email=paypal_email,
                )

                mailgun.send_mail(
                    subject=f"We have received your buylist submission",
                    recipient_list=email,
                    message=f"Your buylist submission has been received. It must be post-marked within 2 business days in order to guarantee "
                            f"your current quote. Please ensure that your cards are sorted exactly as they appear in this email, and that all sleeves are"
                            f" removed. Please ship items to the following address:\n\n"
                            f"{company_buylist_shipping_info(buylist_number)}\n\n"
                            f"Here are your order details:\n"
                            f"{customer_order_info_template}\n\n"
                            f"{ordered_items_template(cart, total=total)}\n"
                            f"Your Notes:\n"
                            f"{notes}"
                )
                cart.empty()
                context["submit"] = True

        else:
            address_form = AddressForm()
            payment_form = BuylistPaymentType()
            context["address_form"] = address_form
            context["payment_form"] = payment_form
            context["cart"] = cart

        return render(request, template_name=template_name, context=context)


def check_buylist_order(request, buylist_number):
    context = dict()
    template_name = "check_buylist_order.html"
    order = BuylistSubmission.objects.get(buylist_number=buylist_number)

    def make_status_change(status):
        new_status = change_order_status(order.buylist_order, order_status=status)
        order.buylist_order = new_status
        order.buylist_status = status
        order.save()

    def create_new_cart_item(card_condition, quantity):

        condition = card_condition
        graded_price = grade(condition=condition, printing=printing, price=price)
        total = graded_price * quantity
        resubmitted_list.append(
            {
                'product_id': product_id,
                'name': name,
                'expansion': expansion,
                'printing': printing,
                'condition': condition,
                'language': language,
                'quantity': quantity,
                'price': graded_price,
                'total': total,
            }
        )

    if request.POST.get("mark_as_received"):
        make_status_change("Received and Verifying Content")

    elif request.POST.get("cancel_buylist"):
        make_status_change("canceled")

    elif request.POST.get('await_customer_reply'):
        post_data = request.POST
        resubmitted_list = list()
        for i in range(len(post_data.getlist('name'))):
            name = post_data.getlist('name')[i]
            expansion = post_data.getlist('expansion')[i]
            price = float(post_data.getlist('price')[i])
            product_id = post_data.getlist('product_id')[i]
            language = post_data.getlist('language')[i]
            printing = post_data.getlist('printing')[i]
            clean = int(post_data.getlist('clean')[i])
            played = int(post_data.getlist('played')[i])
            heavily_played = int(post_data.getlist('heavily_played')[i])

            if clean > 0:
                create_new_cart_item("clean", clean)

            if played > 0:
                create_new_cart_item("played", played)

            if heavily_played > 0:
                create_new_cart_item("heavily_played", heavily_played)

        total_price = sum([i['total'] for i in resubmitted_list])
        total_price = total_price * 1.3 if order.payment_type == 'store_credit' else total_price
        total_price = round(total_price, 2)

        formatted_ordered_items = ordered_items_template(cart=resubmitted_list, total=total_price)
        mailgun.send_mail(
            subject=f'Update for Buylist {buylist_number}',
            recipient_list=order.email,
            message='Your buylist submission has been graded. Please approve or deny any changes. Once we receive your '
                    f'reply your buylist will be processed.\n\n{formatted_ordered_items}'
        )
        make_status_change("Awaiting Email Reply")

    elif request.POST.get("submit_buylist"):
        upload_list = list()
        post_data = request.POST
        resubmitted_list = list()

        for i in range(len(post_data.getlist('name'))):
            name = post_data.getlist('name')[i]
            expansion = post_data.getlist('expansion')[i]
            price = float(post_data.getlist('price')[i])
            product_id = post_data.getlist('product_id')[i]
            language = post_data.getlist('language')[i]
            printing = post_data.getlist('printing')[i]
            clean = int(post_data.getlist('clean')[i])
            played = int(post_data.getlist('played')[i])
            heavily_played = int(post_data.getlist('heavily_played')[i])

            if clean > 0:
                create_new_cart_item("clean", clean)

            if played > 0:
                create_new_cart_item("played", played)

            if heavily_played > 0:
                create_new_cart_item("heavily_played", heavily_played)

            if printing == "Foil":
                foil_clean_stock = clean
                foil_played_stock = played
                foil_heavily_played_stock = heavily_played
                normal_clean_stock = 0
                normal_played_stock = 0
                normal_heavily_played_stock = 0

            else:
                foil_clean_stock = 0
                foil_played_stock = 0
                foil_heavily_played_stock = 0
                normal_clean_stock = clean
                normal_played_stock = played
                normal_heavily_played_stock = heavily_played

            upload_list.append(
                MTGUpload(
                    product_id=product_id,
                    name=name,
                    expansion=expansion,
                    normal_clean_stock=normal_clean_stock,
                    normal_played_stock=normal_played_stock,
                    normal_heavily_played_stock=normal_heavily_played_stock,
                    foil_clean_stock=foil_clean_stock,
                    foil_played_stock=foil_played_stock,
                    foil_heavily_played_stock=foil_heavily_played_stock,
                    upload_status=False,
                )
            )

        payment_type = order.payment_type
        paypal_email = order.paypal_email
        total_price = sum([i['total']for i in resubmitted_list])
        total_price = total_price * 1.3 if payment_type == 'store_credit' else total_price
        total_price = round(total_price, 2)

        string = format_cart_for_text_field_storage(
            cart=resubmitted_list, order_number=buylist_number, payment_type=payment_type, paypal_email=paypal_email, total_price=total_price,
        )
        order.buylist_order = string
        order.save()
        # MTGUpload.objects.bulk_create(upload_list)
        message = ''
        if payment_type == 'store_credit':
            message = f'{total_price} has been credited to your account.'
            customer = Customer.objects.get(email=order.email)
            customer.credit += total_price
            customer.save()
        elif payment_type == 'check':
            message = f'Your check will be mailed to you within 1-3 business days.'
        elif payment_type == 'paypal':
            message = f'{total_price} will be sent to {paypal_email} within 1-3 business days.'

        mailgun.send_mail(
            subject=f'Update for Buylist {buylist_number}',
            recipient_list=order.email,
            message=f'Your buylist submission has been completed. {message}'
        )
        make_status_change("completed")
        messages.SUCCESS(request, f'Your buylist submission has been processed. {payment_type} ${total_price}.')
    else:
        pass

    context['order'] = order
    items = split_text_field_string_for_orders(string=order.buylist_order)
    context['items'] = items[0]['items']

    return render(request, template_name=template_name, context=context)

