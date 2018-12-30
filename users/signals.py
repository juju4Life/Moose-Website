from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from customer.models import Customer


@receiver(post_save, sender=User)
def create_Profile(sender, instance, created, **kwargs):
	if created:
		Customer.objects.create(
			email=instance.email,
			name = f'{instance.first_name} {instance.last_name}'

			)