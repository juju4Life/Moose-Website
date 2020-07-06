from django.contrib.admin import ModelAdmin, register
from django.contrib import admin

from orders.admin_actions import OrdersAction
from orders.models import GroupName, Order, ShippingMethod, Coupon, OrdersLayout, PendingPaymentOrder, CompletedOrder, PullingOrder, ReadyToShipOrder

orders_action = OrdersAction()


@register(GroupName)
class GroupNameAdmin(ModelAdmin):
    ordering = ['category', 'group_name', ]
    search_fields = ['group_name', ]


#  ORDERS PAID ------------------------------------------------------------------------------------------ START
def cancel_orders(modeladmin, request, queryset):
    orders_action.cancel_orders(
        modeladmin=modeladmin, request=request, queryset=queryset, obj=CompletedOrder, order_status="canceled", short_description="Cancel Orders",
    )


def pull_orders(modeladmin, request, queryset):
    orders_action.pull_orders(
        modeladmin=modeladmin, request=request, queryset=queryset, obj=PullingOrder, order_status="", short_description="Pulling Orders",
    )


@register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ["order_number", "order_creation_date", "order_view", "name", "total_order_price", ]
    readonly_fields = ["order_view", "order_number", "payer_id", "discounts_code_used", ]
    actions = [pull_orders, cancel_orders, ]
    fields = (
        "order_view",
        ("order_number", "payer_id", ),
        ("name", "email", ),
        "shipping_method",
        ("address_line_1", "address_line_2", ),
        ("city", "state", ),
        "zip_code",
        "phone",
        "total_order_price",
        "tax_charged",
        "shipping_charged",
        "store_credit_used",
        ("discounts_applied", "discounts_code_used", ),
        "notes",
        "send_message",
        "tracking_number",
    )

#  ORDERS PAID ------------------------------------------------------------------------------------------ END


@register(ReadyToShipOrder)
class ReadyToShipAdmin(ModelAdmin):
    pass


@register(ShippingMethod)
class ShippingMethodAdmin(ModelAdmin):
    pass


@register(Coupon)
class CouponAdmin(ModelAdmin):
    pass


@register(OrdersLayout)
class OrdersLayoutAdmin(ModelAdmin):
    pass


@register(PullingOrder)
class PullingOrdersAdmin(ModelAdmin):
    pass


@register(CompletedOrder)
class CompletedOrdersAdmin(ModelAdmin):
    pass


