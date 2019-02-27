from django.db import models
from datetime import date
from validators.model_validators import *
from django.utils import timezone


class Orders(models.Model):
    category = models.CharField(max_length=255, default='unknown')
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
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    email = models.CharField(max_length=100, default='')
    shipping_first_name = models.CharField(max_length=100, default='')
    shipping_last_name = models.CharField(max_length=100, default='')
    address_1 = models.CharField(max_length=100, default='')
    address_2 = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    state = models.CharField(max_length=100, default='')
    postal_code = models.CharField(max_length=100, default='')
    country = models.CharField(max_length=100, default='')
    product_value = models.DecimalField(max_digits=12, decimal_places=2, default=0., blank=True)
    shipping = models.DecimalField(max_digits=12, decimal_places=2, default=0., blank=True)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0., blank=True)
    gross = models.DecimalField(max_digits=12, decimal_places=2, default=0., blank=True)
    fees = models.DecimalField(max_digits=12, decimal_places=2, default=0., blank=True)
    net = models.DecimalField(max_digits=12, decimal_places=2, default=0., blank=True)
    ordered_items = models.TextField()

    def __str__(self):
        return self.order_number

    class Meta:
        verbose_name_plural = 'Orders'


class GroupName(models.Model):
    group_name = models.CharField(max_length=255, default=None)
    group_id = models.CharField(max_length=255, default=None, unique=True)

    def __str__(self):
        return self.group_name


class ScatterEvent(models.Model):
    choices = (
        ('none', 'None',),
        ('release_events', 'Release Events',),
        ('tcgplayer_kickback', 'TCGplayer Kickback',),
        ('ban_list_update', 'Ban-list Update',),
        ('special', 'Special',),
    )

    name = models.CharField(max_length=255, default='')
    event = models.CharField(max_length=255, default='None', choices=choices)
    date = models.DateField()

    def __str__(self):
        return self.name


class Inventory(models.Model):

    update_inventory_quantity = models.IntegerField(default=0)
    sku = models.CharField(max_length=255, default='', unique=True)
    quantity = models.IntegerField(default=0)
    expansion = models.CharField(max_length=255, default='')
    name = models.CharField(max_length=255, default='')
    condition = models.CharField(max_length=255, default='')
    printing = models.CharField(max_length=255, default='', verbose_name='Foil')
    language = models.CharField(max_length=255, default='')
    category = models.CharField(max_length=255, default='')
    rarity = models.CharField(max_length=255, default='')
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0., blank=True)
    last_upload_date = models.DateField(blank=True)
    last_upload_quantity = models.IntegerField(default=0)
    last_sold_date = models.DateField(blank=True)
    last_sold_quantity = models.IntegerField(default=0)
    last_sold_price = models.DecimalField(max_digits=12, default=0, decimal_places=2)
    total_quantity_sold = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def __init__(self, *args, **kwargs):
        super(Inventory, self).__init__(*args, **kwargs)
        self.upload_q = self.update_inventory_quantity

    def clean(self):
        from engine.tcgplayer_api import TcgPlayerApi
        api = TcgPlayerApi()

        if self.update_inventory_quantity < 0:
            current_quantity = api.get_sku_quantity(self.sku)
            if current_quantity['errors']:
                raise ValidationError(
                    {'update_inventory_quantity': current_quantity['errors'][0]}
                )
            else:
                if current_quantity['results'][0]['quantity'] + self.update_inventory_quantity < 0:

                    raise ValidationError(
                        {'update_inventory_quantity': f"Cannot remove more than {current_quantity}"}
                    )
                else:
                    res = api.increment_sku_quantity(self.sku, self.update_inventory_quantity)

                    if res['errors']:
                        raise ValidationError(
                            {'update_inventory_quantity': res['errors'][0]}
                        )
                    elif res['success']:
                        self.quantity += self.update_inventory_quantity
                        self.update_inventory_quantity = 0
                    else:
                        raise ValidationError(
                            {'update_inventory_quantity': 'Unknown Error. Card may not be uploaded.'}
                        )

        elif self.update_inventory_quantity > 0:
            res = api.increment_sku_quantity(self.sku, self.update_inventory_quantity)

            if res['errors']:
                raise ValidationError(
                    {'update_inventory_quantity': res['errors'][0]}
                )
            elif res['success']:
                self.quantity += self.update_inventory_quantity
            else:
                raise ValidationError(
                    {'update_inventory_quantity': 'Unkown erorr. Card may not have been uploaded.'}
                )
        else:
            pass

    class Meta:
        verbose_name_plural = "Inventory"


class NewOrders(models.Model):
    customer_name = models.CharField(max_length=255, default='Unknown')
    order_delivery_type = models.CharField(max_length=255, default='Unknown')
    order_date = models.DateField()
    order_number = models.CharField(max_length=255, default='')
    sku = models.CharField(max_length=255, default='')
    name = models.CharField(max_length=255, default='')
    expansion = models.CharField(max_length=255, default='')
    category = models.CharField(max_length=255, default='')
    condition = models.CharField(max_length=255, default='')
    printing = models.CharField(max_length=255, default='')
    language = models.CharField(max_length=255, default='')
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.order_number

    class Meta:
        verbose_name_plural = "Ordered Singles"







