from django.db import models
from validators.model_validators import contains_minus, contains_plus


class Safe(models.Model):
    reason_choices = (
        ('', '', ),
        ('mtg_trade_in', 'mtg trade', ),
        ('pokemon_trade_in', 'pokemon trade', ),
        ('yugioh_trade_in', 'yugioh trade', ),
        ('trade_in', 'trade in', ),
        ('daily_deposit', 'daily deposit', ),
        ('drawer_balance', 'drawer balance', ),
        ('other_purchase', 'other purchase', ),
        ('safe_restock', 'safe restock', ),
        ('safe_balance', 'safe balance', ),

    )
    date_time = models.DateTimeField(auto_now_add=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    withdrawal = models.CharField(max_length=12, default='0', validators=[contains_minus])
    deposit = models.CharField(max_length=12, default='0', validators=[contains_plus])
    reason = models.CharField(max_length=255, default='', choices=reason_choices)
    manager_initials = models.CharField(max_length=255, default='')
    seller_name = models.CharField(max_length=255, default='', blank=True)
    notes = models.TextField(default='', blank=True)

    def __str__(self):
        return f"{self.date_time}"

    class Meta:
        verbose_name_plural = "Safe"



