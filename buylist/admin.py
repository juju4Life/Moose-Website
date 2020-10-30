from django.contrib import admin
from .models import HotList, CardKingdomBuylist, StarcityBuylist, BuylistSubmission


@admin.register(BuylistSubmission)
class BuylistSubmissionAdmin(admin.ModelAdmin):
    search_fields = ['name', ]
    list_display = ["buylist_number", "date_created", "order_url", "payment_type", "paypal_email", "total", "name", ]


@admin.register(CardKingdomBuylist)
class CkAdmin(admin.ModelAdmin):
    pass


@admin.register(StarcityBuylist)
class ScgAdmin(admin.ModelAdmin):
    pass


