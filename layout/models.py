from django.db import models
from cloudinary.models import CloudinaryField


class HomePageLayout(models.Model):
    name = models.CharField(max_length=255, default='')
    image = CloudinaryField('image')
    text = models.TextField(blank=True)

    def __str__(self):
        return self.name


