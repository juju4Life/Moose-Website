from django.contrib import admin
from .models import Orders, GroupName, ScatterEvent, NewOrders, Inventory
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .forms import InventoryForm


class InventoryResource(resources.ModelResource):
    class Meta:
        model = Inventory
        fields = ('sku', 'name',)


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    ordering = ['-order_date']
    list_filter = ['is_direct', 'order_delivery_type', 'category']
    search_fields = ['order_number']
    list_display = ['order_number', 'order_date', 'category', 'order_delivery_type', 'product_value', 'net', 'is_direct']
    change_list_template = 'admin/orders_change_list.html'


@admin.register(ScatterEvent)
class ScatterEventAdmin(admin.ModelAdmin):
    list_display = ['name', 'event', 'date']


@admin.register(NewOrders)
class NewOrdersAdmin(admin.ModelAdmin):
    ordering = ['-order_date']
    search_fields = ['name']
    list_filter = ['is_direct', 'order_delivery_type', 'order_date', 'printing', 'language']
    list_display = ['order_date', 'customer_name', 'name', 'expansion', 'printing', 'condition', 'language', 'order_number', 'price', 'quantity', 'is_direct']


@admin.register(Inventory)
class InventoryAdmin(ImportExportModelAdmin):
    resource_class = InventoryResource
    save_on_top = True
    search_fields = ['name']
    list_filter = ['category', 'printing', 'language', 'condition', 'expansion']
    ordering = ['-last_sold_date', '-total_quantity_sold', ]
    list_display = ['name', 'expansion', 'quantity', 'price',  'category', 'printing', 'condition', 'last_upload_date',
                    'last_sold_date', 'total_quantity_sold']
    fieldsets = (
        (None, {
            'fields': (
                ('update_inventory_quantity', 'update_inventory_price',),
                ('printing',),
                ('price', 'quantity'),
                ('name', 'expansion',),
                ('language', 'condition',),
                ('last_upload_date', 'last_upload_quantity',),
                ('last_sold_date', 'last_sold_quantity',),
                ('last_sold_price',),
                ('total_quantity_sold',),
            )
        }),

        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('sku',),
        }),
    )

    readonly_fields = ('printing', 'price', 'quantity', 'name', 'expansion', 'language', 'condition',
                       'last_upload_date', 'last_upload_quantity', 'last_sold_date', 'last_sold_quantity',
                       'last_sold_price', 'total_quantity_sold', 'sku',)


@admin.register(GroupName)
class GroupNameAdmin(admin.ModelAdmin):
    ordering = ['category', 'group_name']
    search_fields = ['group_name']
