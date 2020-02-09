from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from customer.models import Customer
from users.models import State
from captcha.fields import CaptchaField


class UserRegisterForm(UserCreationForm):
	state_list = ((i.abbreviation.lower(), i.abbreviation, ) for i in State.objects.all())
	captcha = CaptchaField()

	email = forms.EmailField()
	first_name = forms.CharField()
	last_name = forms.CharField()
	address_line_1 = forms.CharField()
	address_line_2 = forms.CharField(required=False)
	city = forms.CharField()
	state = forms.CharField(widget=forms.Select(choices=tuple(state_list)))
	zip_code = forms.CharField(max_length=5)
	birth_date = forms.DateField(widget=forms.TextInput(
		attrs={'class': 'datepicker'}
	))

	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'birth_date', 'username', 'email', 'address_line_1', 'address_line_2', 'city', 'state', 'zip_code',
				  'address_line_2', 'password1', 'password2', 'captcha', ]

	def clean(self):
		cleaned = self.cleaned_data
		zip_code = cleaned.get('zip_code')
		first_name = cleaned.get('first_name')
		last_name = cleaned.get('last_name')
		email = cleaned.get('email')
		username = cleaned.get('username')
		if not zip_code.isnumeric():
			raise forms.ValidationError(u'Zip Code must contain numeric characters only.')

		if len(zip_code) < 5:
			raise forms.ValidationError(u'Zip Code must be at least 5 digits.')

		if Customer.objects.filter(name=f'{first_name} {last_name}').exists():
			raise forms.ValidationError(u'Name Combination already exists')

		if User.objects.filter(email=email).exists():
			raise forms.ValidationError(u'An account with the email "{0}" already exists.'.format(email))

		if User.objects.filter(username=username).exists():
			raise forms.ValidationError(u'The username "{0}" already exists.'.format(username))

		return cleaned

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


class LoginForm(forms.ModelForm):
	email = forms.CharField(widget=forms.EmailInput())
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ['email', 'password', ]


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
	state_list = ((i.abbreviation, i.abbreviation,) for i in State.objects.all())
	name = forms.CharField()
	address_line_1 = forms.CharField()
	address_line_2 = forms.CharField()
	city = forms.CharField()
	state = forms.CharField(widget=forms.Select(choices=tuple(state_list)))
	zip_code = forms.CharField(max_length=5)

	class Meta:
		model = Customer
		fields = [
			'name', 'address_line_1', 'address_line_2', 'city', 'state', 'zip_code',
		]

	def clean(self):
		cleaned = self.cleaned_data
		zip_code = cleaned.get('zip_code')

		if not zip_code.isnumeric():
			raise forms.ValidationError(u'Zip Code must contain numeric characters only.')

		if len(zip_code) < 5:
			raise forms.ValidationError(u'Zip Code must be at least 5 digits.')

		return cleaned


class UpdateEmailForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	new_email = forms.EmailField()

	class Meta:
		model = User
		fields = ['new_email', 'password']

	def clean(self):

		cleaned_data = self.cleaned_data
		old_password = cleaned_data.get('password')

		if not check_password(old_password, self.instance.password):
			raise forms.ValidationError('Incorrect password. Please try again.')

		return cleaned_data


