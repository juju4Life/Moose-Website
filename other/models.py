from django.db import models


class CardKingdomAnalytics(models.Model):
    name = models.CharField(default='', max_length=255)
    expansion = models.CharField(default='', max_length=255)
    printing = models.CharField(default='', max_length=255)
    current_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    last_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    last_percent_change = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    last_update = models.DateField(auto_now=True)
    price_history = models.TextField(default='', blank=True)
    consecutive_increase = models.IntegerField(default=0)
    consecutive_decrease = models.IntegerField(default=0)
    total_days_without_decrease = models.IntegerField(default=0)

    def __str__(self):
        return self.name








