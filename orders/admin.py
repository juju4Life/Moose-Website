from django.contrib import admin
from orders.models import GroupName, Order, ShippingMethod, Coupon


@admin.register(GroupName)
class GroupNameAdmin(admin.ModelAdmin):
    ordering = ['category', 'group_name', ]
    search_fields = ['group_name', ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["order_number", "order_creation_date", "order_view", "name", "total_order_price", ]


@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    pass


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    pass
