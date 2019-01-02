from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from customer.models import Customer



class UserRegisterForm(UserCreationForm):
	email = forms.EmailField(unique=True)
	first_name = forms.CharField()
	last_name = forms.CharField()
 
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
	class Meta:
		pass


class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField(unique=True)

	class Meta:
		model = User
		fields = ['username', 'email']


'''class CustomerUpdateForm(forms.ModelForm):
	class Meta:
	model = Customer
	field = ['email']'''