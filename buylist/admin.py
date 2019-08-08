from django.contrib import admin
from .models import HotList
from customer.tasks import add_buylist_item


class HotListAdmin(admin.ModelAdmin):
    list_display = ['name', 'expansion', 'price']
    ordering = ['name']
    search_fields = ['name']


admin.site.register(HotList, HotListAdmin)

