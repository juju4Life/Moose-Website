from django.contrib import admin
from .models import Orders, GroupName


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    ordering = ['order_number']


admin.site.register(GroupName)

