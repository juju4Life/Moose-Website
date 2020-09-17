from django.contrib import admin
from .models import HotList, CardKingdomBuylist, StarcityBuylist, StoreCredit, BuylistSubmission


class HotListAdmin(admin.ModelAdmin):
    list_display = ['name', 'expansion', 'price']
    ordering = ['name']
    search_fields = ['name']


@admin.register(CardKingdomBuylist)
class CkAdmin(admin.ModelAdmin):
    pass


@admin.register(StarcityBuylist)
class ScgAdmin(admin.ModelAdmin):
    pass


@admin.register(StoreCredit)
class StoreCreditAdmin(admin.ModelAdmin):
    list_display = ['name', 'store_credit', 'date_time', 'total', ]


@admin.register(BuylistSubmission)
class BuylistSubmissionAdmin(admin.ModelAdmin):
    search_fields = ['name', ]
    list_display = ["buylist_number", "date_created", "order_url", "payment_type", "paypal_email", "total", "name", ]


admin.site.register(HotList, HotListAdmin)

