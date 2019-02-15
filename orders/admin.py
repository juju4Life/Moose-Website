from django.contrib import admin
from .models import Orders, GroupName


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    ordering = ['-order_date']
    list_filter = ['order_delivery_type', 'category']
    search_fields = ['order_number']
    list_display = ['order_number', 'order_date', 'category', 'order_delivery_type', 'product_value', 'net', 'is_direct']
    change_list_template = 'admin/orders_change_list.html'


admin.site.register(GroupName)

