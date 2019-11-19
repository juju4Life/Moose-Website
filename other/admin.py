from django.contrib import admin
from .models import CardKingdomAnalytics


@admin.register(CardKingdomAnalytics)
class CardKingdomAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'expansion', 'printing', 'current_price', 'last_price', 'consecutive_increase', 'consecutive_decrease',
                    'last_percent_change', 'total_days_without_decrease', 'last_update']
