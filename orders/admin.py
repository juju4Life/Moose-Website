from django.contrib import admin
from orders.models import GroupName, Order, ShippingMethod, Coupon


@admin.register(GroupName)
class GroupNameAdmin(admin.ModelAdmin):
    ordering = ['category', 'group_name']
    search_fields = ['group_name']


@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    pass


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    pass
