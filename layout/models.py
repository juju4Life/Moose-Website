from django.db import models
from cloudinary.models import CloudinaryField


class HomePageLayout(models.Model):
    name = models.CharField(max_length=255, default='')
    image = CloudinaryField('image')
    text = models.TextField(blank=True)

    def __str__(self):
        return self.name


class SinglePrintingSet(models.Model):
    expansion = models.CharField(max_length=255, default='')
    normal_only = models.BooleanField(default=False)
    foil_only = models.BooleanField(default=False)

    def __str__(self):
        return self.expansion



