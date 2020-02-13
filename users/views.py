from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import UserRegisterForm, UserUpdateForm, CustomerUpdateForm, UpdateEmailForm, LoginForm
from customer.models import Customer


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, f'Account Created for {username}. You are now able to log in.')
            return redirect('login')
        else:
            pass  # messages.warning(request, '...')

    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    form = LoginForm(request.POST)
    context = {'form': form}

    if request.POST.get('user_login'):

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

            if request.POST.get('update'):
                user_form = UserUpdateForm(request.POST, instance=request.user)

                if user_form.is_valid():
                    user_form.save()
                    customer.save()
                    messages.success(request, 'Your account has been updated successfully')
                return redirect('profile')

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
                    messages.success(request, 'Your account has been updated successfully')
                    return redirect('profile')
                else:
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

            else:
                user_form = UserUpdateForm(request.POST, customer.address_line_1, instance=request.user)
                profile_form = CustomerUpdateForm(instance=request.user)

        else:
            user_form = UserUpdateForm(request.POST, instance=request.user)
            profile_form = CustomerUpdateForm(instance=request.user)

        return render(request, 'users/profile.html', {'customer': customer})

    else:
        user_form = None


