from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm
from customer.models import Customer

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')			

			messages.success(request, f'Account Created for {username}!')
			return redirect('login')
	else:
		form = UserRegisterForm()

	return render(request, 'users/register.html', {'form':form})


@login_required
def profile(request):
	print(request)
	#data = Customer.objects.get(email=)
	return render(request, 'users/profile.html')


