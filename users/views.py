

from customer.models import Customer
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from mail.mailgun_api import MailGun
from users import forms
from users.forms import UserRegisterForm, UserUpdateForm, AddressForm, UpdateEmailForm, LoginForm, UpdatePasswordForm
from users.tokens import account_activation_token


mailgun = MailGun()


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            user = User.objects.get(email=email)
            user.is_active = False
            user.save()
            mail_subject = 'Activate your account.'
            current_site = get_current_site(request)
            message = render_to_string('account_activation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            to_email = form.cleaned_data.get('email')
            mailgun.send_mail(
                recipient_list=to_email,
                subject=mail_subject,
                message=message
            )

            messages.warning(request, 'Please confirm your email address to complete the registration')
            return redirect('login')
            # messages.success(request, f'Account Created for {username}. You are now able to log in.')
            # return redirect('login')
        else:
            pass  # messages.warning(request, '...')

    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been verified. You may now login')
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!')


def user_login(request):
    form = LoginForm(request.POST)
    context = {'form': form}

    if request.POST.get('user_login'):
        if form.is_valid():

            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(email=email, password=password)
            get_user = User.objects.get(email=email)
            if get_user.is_staff:
                return redirect("login")

            elif get_user.is_active is False:
                messages.warning(request, "Your account needs to be activated. Please use the account activation link in your email.")
                return redirect("login")

            else:
                if user is not None:
                    login(request, user)

                    if request.GET.get('redirect-path'):
                        return redirect(request.GET.get('redirect-path'))
                    else:
                        return redirect('profile')
                else:
                    messages.warning(request, 'Email and Password does not match.')
                    return redirect('login')

    return render(request, 'users/login.html', context)


@login_required
def restock_notification_change(request):

    if request.GET.get("restock_notice_change"):
        email = request.user.email
        product_id = request.GET.get("restock_notice_change")
        customer = Customer.objects.get(email=email)

        foil = False
        normal = False
        clean = False
        played = False
        heavily_played = False

        if request.GET.get("foil"):
            foil = True
        if request.GET.get("normal"):
            normal = True
        if request.GET.get("clean"):
            clean = True
        if request.GET.get("played"):
            played = True
        if request.GET.get("heavily_played"):
            heavily_played = True

        restock_item = customer.restock_list.get(product_id=product_id)
        restock_item.foil = foil
        restock_item.normal = normal
        restock_item.clean = clean
        restock_item.played = played
        restock_item.heavily_played = heavily_played
        restock_item.save()

        return redirect("profile")

    elif request.GET.get("delete_restock_notification"):
        email = request.user.email
        product_id = request.GET.get("delete_restock_notification")
        customer = Customer.objects.get(email=email)
        restock_item = customer.restock_list.get(product_id=product_id)
        restock_item.delete()

        return redirect("profile")

    else:
        return redirect("profile")


@login_required
def remove_wishlist_item(request):
    if request.GET.get("remove"):
        customer = Customer.objects.get(email=request.user.email)
        product = request.GET.get("remove") + ","
        customer.wishlist = customer.wishlist.replace(product, "")
        customer.save()
        return redirect("profile")


@login_required
def profile(request):
    if request.user.is_authenticated:
        context = {}
        customer = Customer.objects.get(email=request.user.email)
        wishlist_data = customer.wishlist.split(",")[:-1]
        wishlist_items = list()
        for cards in wishlist_data:
            card_data = cards.split("<>")
            wishlist_items.append(
                {"name": card_data[1], "expansion": card_data[2], "image_url": card_data[3]}
            )

        restock_list = [
            {
                "product_id": i.product_id,
                "name": i.name,
                "expansion": i.expansion,
                "foil": i.foil,
                "normal": i.normal,
                "clean": i.clean,
                "played": i.played,
                "heavily_played": i.heavily_played,
             }

            for i in customer.restock_list.all()
        ]

        if request.method == 'POST':

            if request.POST.get('update_password'):
                password_form = UpdatePasswordForm(request.user, request.POST)

                if password_form.is_valid():
                    updated_password = password_form.save()
                    update_session_auth_hash(request, updated_password)
                    messages.success(request, 'Your password has been updated successfully')
                    return redirect('profile')
                else:
                    password_form = UpdatePasswordForm(request.user, request.POST)

                context["customer"] = customer
                context["password_form"] = password_form
                context["restock_list"] = restock_list
                return render(request, 'users/profile.html', context)

            elif request.POST.get('update_page'):

                user_form = UserUpdateForm(request.POST, instance=request.user)
                context["customer"] = customer
                context["user_form"] = user_form
                context["restock_list"] = restock_list
                context["wishlist_items"] = wishlist_items

                return render(request, 'users/profile.html', context)

            elif request.POST.get('update_address'):
                address_form = AddressForm(request.POST, instance=customer)
                if address_form.is_valid():
                    address_form.save()
                    name = request.POST.get('name')
                    zip_code = request.POST.get('zip_code')
                    address_line_1 = request.POST.get('address_line_1')
                    address_line_2 = request.POST.get('address_line_2')
                    city = request.POST.get('city')
                    state = request.POST.get('state')

                    customer.zip_code = zip_code
                    customer.shipping_name = name
                    customer.address_line_1 = address_line_1
                    customer.address_line_2 = address_line_2
                    customer.city = city
                    customer.state = state
                    customer.save()
                    messages.success(request, 'Your account has been updated successfully')
                    return redirect('profile')
                else:
                    address_form = AddressForm(request.POST, instance=customer)
                    context["customer"] = customer
                    context["address_form"] = address_form
                    context["wishlist_items"] = wishlist_items
                    context["restock_list"] = restock_list
                    return render(request, 'users/profile.html', context)

            elif request.POST.get('update_second_address'):
                address_form = AddressForm(request.POST, instance=customer)
                if address_form.is_valid():
                    address_form.save()
                    name = request.POST.get('name')
                    zip_code = request.POST.get('zip_code')
                    address_line_1 = request.POST.get('address_line_1')
                    address_line_2 = request.POST.get('address_line_2')
                    city = request.POST.get('city')
                    state = request.POST.get('state')
                    customer.second_zip_code = zip_code
                    customer.second_name = name
                    customer.second_address_line_1 = address_line_1
                    customer.second_address_line_2 = address_line_2
                    customer.second_city = city
                    customer.second_state = state
                    customer.save()
                    messages.success(request, 'Your account has been updated successfully')
                    return redirect('profile')
                else:
                    address_form = AddressForm(request.POST, instance=customer)
                    context["customer"] = customer
                    context["address_form"] = address_form
                    context["wishlist_items"] = wishlist_items
                    context["restock_list"] = restock_list
                    return render(request, 'users/profile.html', context)

            elif request.POST.get('update_email'):
                email_form = UpdateEmailForm(request.POST, instance=request.user)

                if email_form.is_valid():
                    email_form.save()
                    email = request.POST.get('new_email')
                    user = User.objects.get(email=request.user.email)
                    user.email = email
                    customer.email = email
                    customer.save()
                    user.save()
                    messages.success(request, 'Your email has been updated successfully')
                    return redirect('profile')
                else:
                    email_form = UpdateEmailForm(request.POST, instance=request.user)
                    context["customer"] = customer
                    context["email_form"] = email_form
                    context["wishlist_items"] = wishlist_items
                    context["restock_list"] = restock_list
                    return render(request, 'users/profile.html', context)

            elif request.POST.get('delete_address'):
                customer.address_line_1 = ''
                customer.address_line_2 = ''
                customer.city = ''
                customer.state = ''
                customer.zip_code = ''
                customer.shipping_name = ''

                if customer.second_address_line_1:
                    customer.shipping_name = customer.second_name
                    customer.address_line_1 = customer.second_address_line_1
                    customer.address_line_2 = customer.second_address_line_2
                    customer.city = customer.second_city
                    customer.state = customer.second_state
                    customer.zip_code = customer.second_zip_code

                    customer.second_name = ''
                    customer.second_address_line_1 = ''
                    customer.second_address_line_2 = ''
                    customer.second_city = ''
                    customer.second_state = ''
                    customer.second_zip_code = ''
                customer.save()
                messages.success(request, 'Your account has been updated successfully')
                return redirect('profile')

            elif request.POST.get('delete_second_address'):
                customer.second_name = ''
                customer.second_address_line_1 = ''
                customer.second_address_line_2 = ''
                customer.second_city = ''
                customer.second_state = ''
                customer.second_zip_code = ''
                customer.save()
                messages.success(request, 'Your account has been updated successfully')
                return redirect('profile')

            # --- Handle Subscription Status ---

            elif request.POST.get('subscriptions'):

                if request.POST.get('events'):
                    customer.email_subscriber_events = True
                else:
                    customer.email_subscriber_events = False

                if request.POST.get('buylist'):
                    customer.email_subscriber_buylist = True
                else:
                    customer.email_subscriber_buylist = False

                if request.POST.get('new_products'):
                    customer.email_subscriber_new_products = True
                else:
                    customer.email_subscriber_new_products = False

                customer.save()

                return redirect('profile')

            else:
                user_form = UserUpdateForm(request.POST, customer.address_line_1, instance=request.user)
                profile_form = AddressForm(instance=request.user)

        else:
            user_form = UserUpdateForm(request.POST, instance=request.user)
            profile_form = AddressForm(instance=request.user)

        context["customer"] = customer
        context["wishlist_items"] = wishlist_items
        context["restock_list"] = restock_list

        return render(request, 'users/profile.html', context)

    else:
        user_form = None


def reset_password(request):
    context = dict()
    template_name = "users/password_reset_confirm.html"
    email_form = forms.EmailForm()
    context["email_form"] = email_form
    if request.POST.get("email"):
        email_form = forms.EmailForm(request.POST)

        if email_form.is_valid():
            email = email_form.cleaned_data["email"]

            try:
                user = User.objects.get(email=email)
                mail_subject = 'Reset your password'
                current_site = get_current_site(request)

                message = render_to_string('account_activation.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })

                success = mailgun.send_mail(
                    recipient_list=email,
                    subject=mail_subject,
                    message=message,
                )
                if success["id"]:

                    messages.success(request, f'An email with instructions on how to reset your account has been sent to "{email}"')
                else:
                    messages.warning(request, 'There was an error with your request. Please try again later.')

            except ObjectDoesNotExist:
                messages.warning(request, f'There was no account associated with "{email}" ')

    return render(request, template_name=template_name, context=context)


def reset_password_change_form(request, uidb64, token):
    context = dict()
    template_name = "users/password_reset_complete.html"
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        print(user.email)

    return render(request, template_name=template_name, context=context)



