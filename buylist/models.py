from customer.models import CustomerInfo, BasicProductInfo
from django.db import models
from engine.models import MTG


class BuylistFields(models.Model):
    name = models.CharField(max_length=255, default='')
    expansion = models.CharField(max_length=255, default='')
    printing = models.CharField(max_length=255, default='', blank=True)
    price_nm = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    price_ex = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    price_vg = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        abstract = True


class HotList(BasicProductInfo):

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "HotList"


class HotListCards(MTG):
    pass


class CardKingdomBuylist(BuylistFields):

    def __str__(self):
        return self.name


class StarcityBuylist(BuylistFields):

    def __str__(self):
        return self.name


class BuylistSubmission(CustomerInfo):
    status_choice = (
        ("not_received", "Not Received", ),
        ("verifying", "Verifying Contents", ),
        ("canceled", "canceled", ),
        ("processed", "Processed", ),
    )

    change_order_status = models.CharField(max_length=255, default='', choices=status_choice)
    buylist_order = models.TextField(default='')
    buylist_number = models.CharField(max_length=255, default='')
    buylist_status = models.CharField(max_length=255, default="Not Received")
    payment_type = models.CharField(max_length=255, default="")
    paypal_email = models.EmailField(default='', blank=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    order_url = models.URLField(blank=True)
    seller_review_grading = models.BooleanField(default=False)

    def __str__(self):
        return self.buylist_number


