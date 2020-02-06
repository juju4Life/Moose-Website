from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from customer.models import Customer


class UserRegisterForm(UserCreationForm):
	states = (
		(),
	)
	email = forms.EmailField()
	first_name = forms.CharField()
	last_name = forms.CharField()
	address_line_1 = forms.CharField()
	address_line_2 = forms.CharField(required=False)
	city = forms.CharField()
	state = forms.CharField(widget=forms.Select())
	zip_code = forms.CharField()
	birth_date = forms.DateField(widget=forms.TextInput(
		attrs={'class': 'datepicker'}
	))

	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'birth_date', 'username', 'email', 'address_line_1', 'address_line_2', 'city', 'state', 'zip_code', 'address_line_2', 'password1', 'password2', ]

	def save(self, commit=True):
		user = super(UserRegisterForm, self).save(commit=False)
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.email = self.cleaned_data['email']
		user.set_password(self.cleaned_data["password1"])
		user.address_line_1 = self.cleaned_data['address_line_1']
		user.address_line_2 = self.cleaned_data['address_line_2']
		user.city = self.cleaned_data['city']
		user.state = self.cleaned_data['state']
		user.zip_code = self.cleaned_data['zip_code']
		user.birth_date = self.cleaned_data['birth_date']
		if commit:
			user.save()


class LoginForm(AuthenticationForm):
	class Meta:
		pass


class UserUpdateForm(forms.ModelForm):
	username = forms.CharField(max_length=15)

	class Meta:
		model = User
		fields = ['username']

	def __init__(self, *args, **kwargs):
		super(UserUpdateForm, self).__init__(*args, **kwargs)
		# address = args[1]
		# self.fields['address_line_1'].widget.attrs['placeholder'] = address


class CustomerUpdateForm(forms.ModelForm):
	name = forms.CharField()
	address_line_1 = forms.CharField()
	address_line_2 = forms.CharField()
	city = forms.CharField()
	state = forms.CharField()
	zip_code = forms.CharField()

	class Meta:
		model = Customer
		fields = [
			'name', 'address_line_1', 'address_line_2', 'city', 'state', 'zip_code'
		]


