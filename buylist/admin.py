from django.contrib import admin
from .models import HotList, CardKingdomBuylist, StarcityBuylist, StoreCredit


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
    pass


admin.site.register(HotList, HotListAdmin)

