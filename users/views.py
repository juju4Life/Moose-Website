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
            messages.error(request, 'Email and Password does not match.')
            return redirect('login')

    return render(request, 'users/login.html', context)


@login_required
def profile(request):
    if request.user.is_authenticated:
        data = Customer.objects.get(email=request.user.email)

        if request.method == 'POST':

            if request.POST.get('update'):
                user_form = UserUpdateForm(request.POST, data.address_line_1, instance=request.user)

                if user_form.is_valid():
                    user_form.save()
                    # email = request.user.email
                    # data.email = email
                    data.save()
                    messages.success(request, 'Your account has been updated successfully')
                return redirect('profile')

            elif request.POST.get('update_page'):

                user_form = UserUpdateForm(request.POST, data.address_line_1, instance=request.user)

                return render(request, 'users/profile.html', {'data': data, 'user_form': user_form})

            elif request.POST.get('update_address'):
                address_form = CustomerUpdateForm(request.POST, instance=request.user)
                if address_form.is_valid():
                    address_form.save()
                    name = request.POST.get('name')
                    zip_code = request.POST.get('zip_code')
                    address_line_1 = request.POST.get('address_line_1')
                    address_line_2 = request.POST.get('address_line_2')
                    city = request.POST.get('city')
                    state = request.POST.get('state')
                    data.zip_code = zip_code
                    data.name = name
                    data.address_line_1 = address_line_1
                    data.address_line_2 = address_line_2
                    data.city = city
                    data.state = state
                    data.save()
                    messages.success(request, 'Your account has been updated successfully')
                    return redirect('profile')
                else:
                    return render(request, 'users/profile.html', {'data': data, 'address_form': address_form})

            elif request.POST.get('update_second_address'):
                address_form = CustomerUpdateForm(request.POST, instance=request.user)
                if address_form.is_valid():
                    address_form.save()
                    name = request.POST.get('name')
                    zip_code = request.POST.get('zip_code')
                    address_line_1 = request.POST.get('address_line_1')
                    address_line_2 = request.POST.get('address_line_2')
                    city = request.POST.get('city')
                    state = request.POST.get('state')
                    data.second_zip_code = zip_code
                    data.second_name = name
                    data.second_address_line_1 = address_line_1
                    data.second_address_line_2 = address_line_2
                    data.second_city = city
                    data.second_state = state
                    data.save()
                    messages.success(request, 'Your account has been updated successfully')
                    return redirect('profile')
                else:
                    return render(request, 'users/profile.html', {'data': data, 'address_form': address_form})

            elif request.POST.get('update_email'):
                email_form = UpdateEmailForm(request.POST, instance=request.user)

                if email_form.is_valid():
                    email_form.save()
                    email = request.POST.get('new_email')
                    user = User.objects.get(email=request.user.email)
                    user.email = email
                    data.email = email
                    data.save()
                    user.save()
                    messages.success(request, 'Your account has been updated successfully')
                    return redirect('profile')
                else:
                    return render(request, 'users/profile.html', {'data': data, 'email_form': email_form})

            else:
                user_form = UserUpdateForm(request.POST, data.address_line_1, instance=request.user)
                profile_form = CustomerUpdateForm(instance=request.user)

        else:
            user_form = UserUpdateForm(request.POST, data.address_line_1, instance=request.user)
            profile_form = CustomerUpdateForm(instance=request.user)

        return render(request, 'users/profile.html', {'data': data})

    else:
        user_form = None


