from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
from validators.model_validators import cannot_be_empty


class BasicProductInfo(models.Model):
    product_id = models.CharField(max_length=255, default='')
    name = models.CharField(max_length=255, default='')
    expansion = models.CharField(max_length=255, default='')
    printing = models.CharField(max_length=255, default='')
    price = models.DecimalField(max_digits=12, decimal_places=2, default=None, null=True, blank=True)
    image = models.CharField(max_length=255, default='no_image.png')

    class Meta:
        abstract = True


class CustomerInfo(models.Model):
    name = models.CharField(max_length=255, default='')
    email = models.EmailField(max_length=200, default='')
    company = models.CharField(max_length=255, default='', blank=True)
    country = models.CharField(max_length=255, default='US', blank=True)
    address_line_1 = models.CharField(max_length=255, default='', blank=True)
    address_line_2 = models.CharField(max_length=255, default='', blank=True)
    state = models.CharField(max_length=20, default='', blank=True)
    city = models.CharField(max_length=20, default='', blank=True)
    zip_code = models.CharField(max_length=25, default='', blank=True)
    phone = models.CharField(max_length=25, default='', blank=True)
    notes = models.TextField(default='', blank=True)

    class Meta:
        abstract = True


class Customer(models.Model):
    transaction_choices = (
        ('', '', ),
        ('other', 'other', ),
        ('mtg', 'mtg', ),
        ('pokemon', 'pokemon', ),
        ('supplies', 'supplies', ),
        ('yugioh', 'yugioh', ),
    )

    letters_only = RegexValidator(r'^[a-zA-Z ]*$', _('Only letters are allowed.'))
    name = models.CharField(validators=[letters_only], max_length=100, default='')
    credit = models.DecimalField(max_digits=12, decimal_places=2, default=0., blank=True, verbose_name='Credit')
    last_credit = models.DecimalField(max_digits=12, decimal_places=2, default=0., blank=True, verbose_name='last_credit')
    email = models.EmailField(max_length=200, default='')
    notes = models.TextField(default='', blank=True, null=True)
    employee_initial = models.CharField(max_length=5, default='')
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    company = models.CharField(max_length=255, default='', blank=True)
    country = models.CharField(max_length=255, default='US', blank=True)
    address_line_1 = models.CharField(max_length=255, default='', blank=True)
    address_line_2 = models.CharField(max_length=255, default='', blank=True)
    state = models.CharField(max_length=20, default='', blank=True)
    city = models.CharField(max_length=20, default='', blank=True)
    zip_code = models.CharField(max_length=25, default='', blank=True)
    second_name = models.CharField(max_length=255, default='', blank=True)
    second_company = models.CharField(max_length=255, default='', blank=True)
    second_country = models.CharField(max_length=255, default='US', blank=True)
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
    wishlist = models.TextField(default='', blank=True)
    restock_list = models.ManyToManyField("customer.CustomerRestockNotice")
    orders = models.TextField(default='', blank=True)
    buylist_submissions = models.TextField(default='', blank=True)
    clear_credit = models.BooleanField(default=False)
    transaction = models.CharField(max_length=255, default='', choices=transaction_choices, validators=[cannot_be_empty])

    history = HistoricalRecords(
        history_change_reason_field=models.TextField(null=True)
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Customer Store Credit"


class CustomerRestockNotice(models.Model):
    email = models.CharField(max_length=255, default='')
    product_id = models.CharField(max_length=255, default='')
    name = models.CharField(max_length=255, default='')
    expansion = models.CharField(max_length=255, default='')
    foil = models.BooleanField(default=False)
    normal = models.BooleanField(default=False)
    clean = models.BooleanField(default=False)
    played = models.BooleanField(default=False)
    heavily_played = models.BooleanField(default=False)

    def __str__(self):
        return self.email


class StoreCredit(models.Model):
    name = models.CharField(max_length=255, default='', blank=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    entries = models.IntegerField(default=0)
    store_credit = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Credit Added')
    used_credit = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Credit Used')
    date_time = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(max_length=255, default='')

    def __str__(self):
        return f"{self.store_credit}"

    class Meta:
        verbose_name_plural = 'Store Credit History'

