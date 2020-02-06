from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from customer.models import Customer


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		Customer.objects.create(
			user=instance,
			email=instance.email,
			name=f'{instance.first_name} {instance.last_name}',
			address_line_1=instance.address_line_1,
			address_line_2=instance.address_line_2,
			state=instance.state,
			city=instance.city,
			zip_code=instance.zip_code,
			birth_date=instance.birth_date,
			)


'''@receiver(post_save, sender=User)
def save_Profile(sender, instance, **kwargs):
		pass'''


