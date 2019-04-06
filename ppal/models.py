from django.db import models


class PaypalOrder(models.Model):

    order_id = models.CharField(max_length=255, default='')
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amount_currency_type = models.CharField(max_length=255, default='')
    my_email = models.CharField(max_length=255, default='')
    merchant_id = models.CharField(max_length=255, default='')
    shipping_name = models.CharField(max_length=255, default='')
    adress_line_1 = models.CharField(max_length=255, default='')
    admin_area_1 = models.CharField(max_length=255, default='')
    admin_area_2 = models.CharField(max_length=255, default='')
    postal_code = models.CharField(max_length=255, default='')
    coutnry_code = models.CharField(max_length=255, default='')
    payment_id = models.CharField(max_length=255, default='')
    payment_status = models.CharField(max_length=255, default='')
    paypal_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()
    first_name = models.CharField(max_length=255, default='')
    last_name = models.CharField(max_length=255, default='')
    customer_payment_email = models.CharField(max_length=255, default='')
    customer_contact_email = models.CharField(max_length=255, default='')
    checkout_name = models.CharField(max_length=255, default='')
    customer_id = models.CharField(max_length=255, default='')
    customer_country_code = models.CharField(max_length=255, default='')

    def __str__(self):
        return f"{self.customer_payment_email} ({self.order_id})"


class PaypalAccessToken(models.Model):
    access_token = models.CharField(max_length=255, default='')
    app_id = models.CharField(max_length=255, default='')
    nonce = models.CharField(max_length=255, default='')
