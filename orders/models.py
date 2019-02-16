from django.db import models
from validators.model_validators import validate_event_choice


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
        ('tcgplayer_kickback', 'TCGplayer Lickback',),
        ('ban_list_update', 'Ban-list Update',),
        ('special', 'Special',),
    )

    event = models.CharField(max_length=255, default='None', choices=choices, validators=[validate_event_choice])
    date = models.DateField()

    def __str__(self):
        return self.event











