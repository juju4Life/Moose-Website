from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from .forms import UserRegisterForm, UserUpdateForm, CustomerUpdateForm, UpdateEmailForm, LoginForm, UpdatePasswordForm
from .tokens import account_activation_token
from customer.models import Customer


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
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
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

            if user is not None:
                login(request, user)

                return redirect('profile')
            else:
                messages.warning(request, 'Email and Password does not match.')
                return redirect('login')

    return render(request, 'users/login.html', context)


@login_required
def profile(request):
    if request.user.is_authenticated:
        customer = Customer.objects.get(email=request.user.email)

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

                return render(request, 'users/profile.html', {'customer': customer, 'password_form': password_form})

            elif request.POST.get('update_page'):

                user_form = UserUpdateForm(request.POST, instance=request.user)

                return render(request, 'users/profile.html', {'customer': customer, 'user_form': user_form})

            elif request.POST.get('update_address'):
                address_form = CustomerUpdateForm(request.POST, instance=customer)

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
                    address_form = CustomerUpdateForm(request.POST, instance=customer)
                    return render(request, 'users/profile.html', {'customer': customer, 'address_form': address_form})

            elif request.POST.get('update_second_address'):
                address_form = CustomerUpdateForm(request.POST, instance=customer)
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
                    address_form = CustomerUpdateForm(request.POST, instance=customer)
                    return render(request, 'users/profile.html', {'customer': customer, 'address_form': address_form})

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
                    return render(request, 'users/profile.html', {'customer': customer, 'email_form': email_form})

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
                profile_form = CustomerUpdateForm(instance=request.user)

        else:
            user_form = UserUpdateForm(request.POST, instance=request.user)
            profile_form = CustomerUpdateForm(instance=request.user)

        return render(request, 'users/profile.html', {'customer': customer})

    else:
        user_form = None


class PasswordResetConfirm(PasswordResetConfirmView):

    def get(self, request, *args, **kwargs):
        print(request.user)
        print(args)
        print(kwargs)



