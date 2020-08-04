from django.db import models


class HotList(models.Model):
    name = models.CharField(max_length=255, default='')
    expansion = models.CharField(max_length=255, default='')
    price = models.DecimalField(max_digits=12, decimal_places=2, default=None, null=True, blank=True)
    image = models.CharField(max_length=255, default='no_image.png')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "HotList"


class CardKingdomBuylist(models.Model):
    name = models.CharField(max_length=255, default='')
    expansion = models.CharField(max_length=255, default='')
    printing = models.CharField(max_length=255, default='', blank=True)
    price_nm = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    price_ex = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    price_vg = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class StarcityBuylist(models.Model):
    name = models.CharField(max_length=255, default='')
    expansion = models.CharField(max_length=255, default='')
    printing = models.CharField(max_length=255, default='', blank=True)
    price_nm = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    price_played = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    price_hp = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class StoreCredit(models.Model):
    name = models.CharField(max_length=255, default='', blank=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    entries = models.IntegerField(default=0)
    store_credit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.store_credit

    verbose_name_plural = 'Total'




