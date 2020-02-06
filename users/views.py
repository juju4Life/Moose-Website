from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, CustomerUpdateForm
from customer.models import Customer


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, f'Account Created for {username}. You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
        for f in form:
            print(f)

    return render(request, 'users/register.html', {'form':form})


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
                    # data.save()
                    messages.success(request, 'Your account has been updated successfully')
                return redirect('profile')

            elif request.POST.get('update_page'):

                user_form = UserUpdateForm(request.POST, data.address_line_1, instance=request.user)
                return render(request, 'users/profile.html', {'data': data, 'user_form': user_form})

            elif request.POST.get('update_address'):
                address_form = CustomerUpdateForm(request.POST)
                return render(request, 'users/profile.html', {'data': data, 'address_form': address_form})

        else:
            user_form = UserUpdateForm(request.POST, data.address_line_1, instance=request.user)
            profile_form = CustomerUpdateForm(instance=request.user)

    else:
        user_form = None

    return render(request, 'users/profile.html', {'data': data})


