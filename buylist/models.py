from django.db import models

class Buying(models.Model):
    name = models.CharField(max_length=255, default='', blank=True, null=True)
    set_name = models.CharField(max_length=255, default='', blank=True, null=True)
    sku = models.CharField(max_length=255, default='None')
    price = models.DecimalField(max_digits=12, decimal_places=2, default=None, null=True, blank= True)
    quantity = models.IntegerField(null=True, blank=True, default=20)
    image = models.CharField(max_length=250, default='', blank=True, null=True)
    product_id = models.CharField(max_length=250, default='', blank=True)
    condition = models.CharField(max_length=250, default='Unknown')
    percentage = models.IntegerField(default=60)

    class meta:
        ordering = ['set_name', 'name']

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Manage Buylist"


class SkuLight(models.Model):
    sku = models.CharField(max_length=255, default='', blank=True, null=True, db_index=True)
    name = models.CharField(max_length=255, default='', blank=True, null=True)
    expansion = models.CharField(max_length=255, default='', blank=True, null=True)
    condition = models.CharField(max_length=255, default='', blank=True, null=True)

    def __str__(self):
        return self.name



class HotList(models.Model):
    name = models.CharField(max_length=255, default='')
    expansion = models.CharField(max_length=255, default='')
    price = models.DecimalField(max_digits=12, decimal_places=2, default=None, null=True, blank= True)
    image = models.CharField(max_length=255, default='no_image.png')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "HotList"


