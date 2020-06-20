from django.db import models


class Coupon(models.Model):
    name = models.CharField(max_length=255, default='')
    code = models.CharField(max_length=255, default='')
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ShippingMethod(models.Model):
    full_name = models.CharField(max_length=255, default='')
    clean_name = models.CharField(max_length=255, default='')
    cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ["cost", "full_name", ]


class GroupName(models.Model):
    added = models.BooleanField(default=False)
    category = models.CharField(max_length=255, default='Unknown')
    group_name = models.CharField(max_length=255, default=None)
    group_id = models.CharField(max_length=255, default=None, unique=True)

    def __str__(self):
        return self.group_name


class Order(models.Model):

    shipping_choices = (

        ("free", "free", ),
        ("standard", "standard", ),
        ("priority", "priority", ),
        ("in-store", "in-store", ),
    )

    order_number = models.CharField(max_length=255, default='')
    order_creation_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255, default='')
    email = models.CharField(max_length=255, default='')
    shipping_method = models.CharField(max_length=255, default='free')
    address_line_1 = models.CharField(max_length=255, default='')
    address_line_2 = models.CharField(max_length=255, default='')
    city = models.CharField(max_length=255, default='')
    state = models.CharField(max_length=255, default='')
    zip_code = models.CharField(max_length=255, default='')
    phone = models.CharField(max_length=255, default='', null=True)
    total_order_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    store_credit_used = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_charged = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    shipping_charged = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discounts_applied = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discounts_code_used = models.CharField(max_length=255, default='')
    notes = models.TextField(default='')
    ordered_items = models.TextField(default='')
    order_view = models.URLField(default='')
    send_message = models.TextField(default='', blank=True)
    tracking_number = models.CharField(max_length=255, default='', blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.order_number


class OrdersLayout(models.Model):
    label = models.CharField(max_length=255, default='')
    name = models.CharField(max_length=255, default='')
    data = models.TextField(default='')

    def __str__(self):
        return self.label


