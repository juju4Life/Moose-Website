from django.db import models


class Orders(models.Model):
    order_number = models.CharField(max_length=100, default='', unique=True)
    order_channel_type = models.CharField(max_length=100, default='')
    order_status_type = models.CharField(max_length=100, default='')
    order_delivery_type = models.CharField(max_length=100, default='')
    is_direct = models.BooleanField()
    international = models.BooleanField()
    presale_status_type = models.CharField(max_length=100, default='')
    order_date = models.DateField()
    modified_on_date = models.DateField()
    customer_token = models.CharField(max_length=100, default='')
    first_name = models.CharField(max_length=100, default=None)
    last_name = models.CharField(max_length=100, default=None)
    email = models.CharField(max_length=100, default=None)
    shipping_first_name = models.CharField(max_length=100, default=None)
    shipping_last_name = models.CharField(max_length=100, default=None)
    address_1 = models.CharField(max_length=100, default=None)
    address_2 = models.CharField(max_length=100, default=None)
    city = models.CharField(max_length=100, default=None)
    state = models.CharField(max_length=100, default=None)
    postal_code = models.CharField(max_length=100, default=None)
    country = models.CharField(max_length=100, default=None)
    product_value = models.DecimalField(max_digits=12, decimal_places=2, default=0., blank=True)
    shipping = models.DecimalField(max_digits=12, decimal_places=2, default=0., blank=True)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0., blank=True)
    gross = models.DecimalField(max_digits=12, decimal_places=2, default=0., blank=True)
    fees = models.DecimalField(max_digits=12, decimal_places=2, default=0., blank=True)
    net = models.DecimalField(max_digits=12, decimal_places=2, default=0., blank=True)
    ordered_items = models.TextField()

    def __str__(self):
        return self.order_number

