from django.db import models


class HotList(models.Model):
    name = models.CharField(max_length=255, default='')
    expansion = models.CharField(max_length=255, default='')
    price = models.DecimalField(max_digits=12, decimal_places=2, default=None, null=True, blank= True)
    image = models.CharField(max_length=255, default='no_image.png')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "HotList"


