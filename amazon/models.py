from django.db import models


class AmazonLiveInventory(models.Model):
    sku = models.CharField(max_length=255, default='')
    old_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    new_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    last_time_change = models.DateTimeField(auto_now=True)
    time_check_delta = models.DateTimeField()

    def __str__(self):
        return self.sku

