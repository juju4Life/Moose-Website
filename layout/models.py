from django.db import models
from cloudinary.models import CloudinaryField


class HomePageImage(models.Model):
    image = CloudinaryField('image')
    text = models.TextField(blank=True)


