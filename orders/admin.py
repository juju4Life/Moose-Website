from django.contrib import admin
from .models import Orders, GroupName, ScatterEvent, NewOrders, Inventory
from import_export.admin import ImportExportModelAdmin
from import_export import resources


class InventoryResource(resources.ModelResource):
    class Meta:
        model = Inventory
        fields = ('sku', 'name',)


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    ordering = ['-order_date']
    list_filter = ['order_delivery_type', 'category']
    search_fields = ['order_number']
    list_display = ['order_number', 'order_date', 'category', 'order_delivery_type', 'product_value', 'net', 'is_direct']
    change_list_template = 'admin/orders_change_list.html'


@admin.register(ScatterEvent)
class ScatterEventAdmin(admin.ModelAdmin):
    list_display = ['name', 'event', 'date']


@admin.register(NewOrders)
class NewOrdersAdmin(admin.ModelAdmin):
    ordering = ['-order_date']


@admin.register(Inventory)
class InventoryAdmin(ImportExportModelAdmin):
    resource_class = InventoryResource
    search_fields = ['name']
    list_filter = ['category', 'printing', 'language', 'expansion']
    ordering = ['-last_upload_date', 'expansion']
    list_display = ['quantity', 'price',  'category', 'printing', 'name', 'expansion', 'condition', 'last_upload_date',
                    'last_sold_date', 'total_quantity_sold']


admin.site.register(GroupName)
