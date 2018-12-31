from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm
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

    return render(request, 'users/register.html', {'form':form})


@login_required
def profile(request):
    if request.user.is_authenticated:
        data = Customer.objects.get(email=request.user.email)

        if request.method == 'POST':
            user_form = UserUpdateForm(request.POST, isntance=request.user)

            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Your account has been updated successfully')
            return redirect('profile')

        else:
            user_form = UserUpdateForm(isntance=request.user)

    return render(request, 'users/profile.html', {'data': data, 'user_form': user_form})


