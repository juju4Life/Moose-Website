from django.contrib.auth.signals import user_login_failed, user_logged_in, user_logged_out
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from customer.models import Customer
from datetime import datetime


# Connect customer profile when user is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):

	if created:
		if instance.is_staff is False:
			try:
				date = datetime.strptime(f'{instance.month}-{instance.day}-{instance.year}', '%B-%d-%Y')
			except AttributeError:
				date = "1700-01-01"

			Customer.objects.create(
				user=instance,
				email=instance.email,
				name=f'{instance.first_name} {instance.last_name}',
				birth_date=date,
				)


# Handl too many login attempts
@receiver(user_login_failed)
def login_failed(sender, credentials, **kwargs):
	email = credentials.get('email')
	if email is not None:
		try:
			user = User.objects.get(email=email)
		except ObjectDoesNotExist:
			user = None
			pass

		if user is not None:
			customer = Customer.objects.get(email=email)
			customer.login_attempt_counter += 1

			if customer.login_attempt_counter >= 5:
				user.set_unusable_password()
				customer.login_attempt_counter = 0
				user.save()

			customer.save()


@receiver(user_logged_in)
def login_success(sender, request, user, **kwargs):
	pass


@receiver(user_logged_out)
def logout_success(sender, request, user, **kwargs):
	pass

