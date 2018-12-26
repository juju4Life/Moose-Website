from django.contrib import admin
from .models import Buying, HotList
from customer.tasks import add_buylist_item


class BuylistAdmin(admin.ModelAdmin):
    model = Buying
    ordering = ['set_name', 'name']
    list_display = ('name', 'set_name', 'price', 'percentage', 'condition',)
    search_fields = ['name']

    def save_model(self, request, obj, form, change):
        add_buylist_item.apply_async(que='low_priority', args=(obj.name,))

class HotListAdmin(admin.ModelAdmin):
    list_display = ['name', 'expansion', 'price']
    ordering = ['name']
    search_fields = ['name']



admin.site.register(Buying, BuylistAdmin)
admin.site.register(HotList, HotListAdmin)