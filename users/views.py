from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			messages.success(request, f'Account Created for {username}!')
			return redirect('home')
	else:
		form = UserCreationForm()

	return render(request, 'users/register.html', {'form':form})


