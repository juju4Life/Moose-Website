from django.db import models


class EbayListing(models.Model):
    title = models.CharField(max_length=80, default='')
    sku = models.CharField(max_length=25, default='')
    listing_id = models.CharField(max_length=30, default='', unique=True)
    payment_policy_id = models.CharField(max_length=30, default='')
    offer_id = models.CharField(max_length=30, default='')
    category_id = models.CharField(max_length=30, default='')
    fulfillment_policy_id = models.CharField(max_length=30, default='')
    return_policy_id = models.CharField(max_length=30, default='')
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    description = models.TextField(default='')
    format = models.CharField(max_length=20, default='')
    shipping_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.title


class EbayAccessToken(models.Model):
    name = models.CharField(max_length=255, default='', blank=True)
    access_token = models.TextField(default='')
    refresh_token = models.CharField(max_length=255, default='')
    user_token = models.CharField(max_length=255, default='')


