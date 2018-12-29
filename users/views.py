from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UseRegisterForm

def register(request):
	if request.method == 'POST':
		form = UseRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')			

			messages.success(request, f'Account Created for {username}!')
			return redirect('home')
	else:
		form = UseRegisterForm()

	return render(request, 'users/register.html', {'form':form})


