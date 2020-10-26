from django.db import models


class Safe(models.Model):
    reason_choices = (
        ('', '', ),
        ('trade_in', 'trade in', ),
        ('restock', 'safe restock', ),
        ('daily_deposit', 'daily deposit', ),
        ('balance', 'safe balance', ),
        ('cash_withdrawal', 'cash withdrawal', ),
    )
    date_time = models.DateTimeField(auto_now_add=True)
    current_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    withdrawal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    deposit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    reason = models.CharField(max_length=255, default='', choices=reason_choices)
    notes = models.TextField(default='', blank=True)



