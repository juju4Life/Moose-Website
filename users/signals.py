from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from customer.models import Customer
from datetime import datetime


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		date = datetime.strptime(f'{instance.month}-{instance.day}-{instance.year}', '%B-%d-%Y')
		Customer.objects.create(
			user=instance,
			email=instance.email,
			name=f'{instance.first_name} {instance.last_name}',
			birth_date=date,
			)


'''@receiver(post_save, sender=User)
def save_Profile(sender, instance, **kwargs):
		pass'''


