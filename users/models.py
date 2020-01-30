from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=255, default='', blank=True)
    address_line_2 = models.CharField(max_length=255, default='', blank=True)
    state = models.CharField(max_length=20, default='', blank=True)
    city = models.CharField(max_length=20, default='', blank=True)
    zip_code = models.CharField(max_length=25, default='', blank=True)
    birth_date = models.DateField(null=True, blank=True)









