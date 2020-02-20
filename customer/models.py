from django.db import models
from simple_history.models import HistoricalRecords
from datetime import datetime
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from validators.model_validators import validate_name


class ItemizedPreorder(models.Model):
    name = models.CharField(max_length=255, default='')
    quantity = models.IntegerField(default=0)
    expansion = models.CharField(max_length=255, default='')
    item_type = models.CharField(max_length=255, default='')
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    custom_price = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    image_url = models.CharField(max_length=255, default='')
    product_id = models.CharField(max_length=50, default='')
    total_sold = models.IntegerField(default=0)
    color = models.CharField(max_length=255, default='None')
    rarity = models.CharField(max_length=255, default='Unknown')
    card_text = models.TextField(default='')
    card_type = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.name


class Preorder(models.Model):
    product = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.product

    class Meta:
        verbose_name_plural = "Create Preorder Product"


class Customer(models.Model):

    letters_only = RegexValidator(r'^[a-zA-Z ]*$', _('Only letters are allowed.'))
    name = models.CharField(validators=[letters_only], max_length=100, default='')
    credit = models.DecimalField(max_digits=12, decimal_places=2, default=0., blank=True, verbose_name='Credit')
    last_credit = models.DecimalField(max_digits=12, decimal_places=2, default=0., blank=True, verbose_name='last_credit')
    email = models.EmailField(max_length=200, default='')
    notes = models.TextField(default='', blank=True, null=True)
    employee_initial = models.CharField(max_length=5, default='')
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    address_line_1 = models.CharField(max_length=255, default='', blank=True)
    address_line_2 = models.CharField(max_length=255, default='', blank=True)
    state = models.CharField(max_length=20, default='', blank=True)
    city = models.CharField(max_length=20, default='', blank=True)
    zip_code = models.CharField(max_length=25, default='', blank=True)
    second_name = models.CharField(max_length=255, default='', blank=True)
    second_address_line_1 = models.CharField(max_length=255, default='', blank=True)
    second_address_line_2 = models.CharField(max_length=255, default='', blank=True)
    second_state = models.CharField(max_length=20, default='', blank=True)
    second_city = models.CharField(max_length=20, default='', blank=True)
    second_zip_code = models.CharField(max_length=25, default='', blank=True)
    birth_date = models.DateField(null=True, blank=True)
    shipping_name = models.CharField(max_length=255, default='', blank=True)
    login_attempt_counter = models.IntegerField(default=0)
    email_subscriber_all = models.BooleanField(default=False)
    email_subscriber_events = models.BooleanField(default=False)
    email_subscriber_buylist = models.BooleanField(default=False)
    email_subscriber_new_products = models.BooleanField(default=False)

    history = HistoricalRecords(
        history_change_reason_field=models.TextField(null=True)
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Customer Store Credit"


class PreordersReady(models.Model):

    type_choice = (
        ('sealed_product', 'Sealed Product', ),
        ('single', 'Single', ),
        ('other', 'Other', ),
    )

    customer_name = models.ForeignKey(Customer, on_delete=models.CASCADE, default=None, verbose_name='Customer Name')
    email = models.EmailField(max_length=255, default='', blank=True)
    product = models.ForeignKey(Preorder, on_delete=models.CASCADE, default=None)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=None, null=True)
    paid = models.DecimalField(max_digits=8, decimal_places=2, default=None, null=True)
    quantity = models.IntegerField(default=1)
    preorder_type = models.CharField(max_length=255, default='Sealed Product', choices=type_choice)
    employee_initials = models.CharField(max_length=5, default='')
    history = HistoricalRecords()

    def __str__(self):
        return "{}".format(self.product)

    def name(self):
        return "{}".format(self.customer_name)

    class Meta:
        verbose_name_plural = "Manage Preorders"


class OrderRequest(models.Model):
    name = models.CharField(max_length=60)
    date = models.DateTimeField(default=datetime.now(), verbose_name='Order Placed')
    contact_type = models.CharField(max_length=50, default='', verbose_name="Contact by")
    email = models.CharField(max_length=255, default='')
    phone = models.CharField(max_length=50, default='', verbose_name='Phone Number')
    missing = models.CharField(max_length=255, blank=True, null=True, verbose_name='No Price Available')
    total = models.DecimalField(max_digits=12, decimal_places=2, default=None, null=True, blank=True, verbose_name='Grand Total')
    notes = models.TextField(default='')
    order_link = models.URLField(max_length=5000, default='', blank=True)
    order = models.TextField(default='')

    def __str__(self):
        return self.name


class ReleasedProducts(models.Model):
    product = models.CharField(max_length=60, default='Name Unknown')
    release_date = models.CharField(max_length=25, default='Unknown', verbose_name='Release Date')
    price = models.CharField(max_length=20, default='None', verbose_name='MSRP')
    link = models.URLField(max_length=5000, default='', blank=True)
    month = models.CharField(max_length=20, default='')
    year = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.product

    class Meta:
        verbose_name_plural = "Released Products"
