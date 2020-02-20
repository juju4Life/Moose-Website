from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from customer.models import Customer
from users.models import State
from users.validators import validate_zip_code, email_is_unique
from captcha.fields import CaptchaField


class UserRegisterForm(UserCreationForm):

	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'month', 'day', 'year', 'captcha', ]

	months = (
		('', '', ),
		('January', 'January', ),
		('February', 'February', ),
		('March', 'March', ),
		('April', 'April', ),
		('May', 'May', ),
		('June', 'June', ),
		('July', 'July', ),
		('August', 'August', ),
		('September', 'September', ),
		('October', 'October', ),
		('November', 'November', ),
		('December', 'December', ),
	)

	captcha = CaptchaField()

	email = forms.EmailField(validators=[email_is_unique])
	first_name = forms.CharField()
	last_name = forms.CharField()
	month = forms.CharField(widget=forms.Select(choices=months))
	day = forms.CharField(max_length=2)
	year = forms.CharField(max_length=4)

	def save(self, commit=True):
		user = super(UserRegisterForm, self).save(commit=False)
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.set_password(self.cleaned_data["password1"])
		user.month = self.cleaned_data['month']
		user.day = self.cleaned_data['day']
		user.year = self.cleaned_data['year']
		if commit:
			user.save()


class LoginForm(forms.ModelForm):
	email = forms.CharField(widget=forms.EmailInput())
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ['email', 'password', ]
		exclude = ['username', ]


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
	address_line_2 = forms.CharField(required=False)
	city = forms.CharField()
	state = forms.CharField(widget=forms.Select(choices=tuple(state_list)))
	zip_code = forms.CharField(max_length=5, validators=[validate_zip_code])

	class Meta:
		model = Customer
		fields = [
			'name', 'address_line_1', 'address_line_2', 'city', 'state', 'zip_code',
		]


class UpdateEmailForm(forms.ModelForm):
	confirm_password = forms.CharField(widget=forms.PasswordInput())
	new_email = forms.EmailField()

	class Meta:
		model = User
		fields = ['new_email', 'confirm_password', ]

	def clean(self):

		cleaned_data = self.cleaned_data
		confirm_password = cleaned_data.get('confirm_password')

		if not check_password(confirm_password, self.instance.password):
			raise forms.ValidationError('Incorrect password. Please try again.')

		return cleaned_data


class UpdatePasswordForm(PasswordChangeForm):
	pass


