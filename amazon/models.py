from django.db import models


class FeedSubmission(models.Model):
    success = models.BooleanField(default=False)
    feed_id = models.CharField(max_length=255, default='')
    feed_successful_on = models.DateTimeField()
    feed_created_on = models.DateTimeField(auto_now_add=True)

    def __string__(self):
        return f"{self.feed_id} - {self.feed_successful_on}"


class AmazonPriceExclusions(models.Model):
    name = models.CharField(max_length=255, default='', blank=True)
    expansion = models.CharField(max_length=255, default='', blank=True)
    condition = models.CharField(max_length=255, default='', blank=True)
    is_foil = models.BooleanField(default=False, blank=True)
    sku = models.CharField(max_length=255, default='', unique=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    min_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    max_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    price_metrics = models.CharField(max_length=255, default='', blank=True)
    exclude = models.BooleanField(default=True)
    date_time_changed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sku









