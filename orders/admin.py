from django.contrib.admin import ModelAdmin, register
from django.contrib import admin

from orders.admin_actions import OrderAction
from orders.admin_functions import show_firm_url
from orders.models import GroupName, Order, ShippingMethod, Coupon, OrdersLayout, PendingPaymentOrder, CompletedOrder, PullingOrder, ReadyToShipOrder

from import_export.admin import ImportExportModelAdmin
from import_export import resources
from import_export.fields import Field

order_action = OrderAction()


@register(GroupName)
class GroupNameAdmin(ModelAdmin):
    ordering = ['category', 'group_name', ]
    search_fields = ['group_name', ]


#  ORDERS PAID ------------------------------------------------------------------------------------------ START
def cancel_orders(modeladmin, request, queryset):
    order_action.cancel_orders(
        modeladmin=modeladmin, request=request, queryset=queryset, obj=CompletedOrder, order_status="canceled", short_description="Cancel Orders",
    )


def pull_orders(modeladmin, request, queryset):
    order_action.pull_orders(
        modeladmin=modeladmin, request=request, queryset=queryset, obj=PullingOrder, order_status="", short_description="Pulling Orders",
    )


order_list_displays = ["order_number", "order_creation_date", "order_view", "name", "total_order_price", "shipping_method", ]

order_fields = (
        "order_action",
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
order_read_only_fields = ["order_view", "order_number", "payer_id", "discounts_code_used", ]


@register(Order)
class OrderAdmin(ModelAdmin):
    def get_queryset(self, request):
        return Order.objects.filter(order_paid=True)

    ordering = ["order_creation_date", ]
    search_fields = ["name", "order_number", "ordered_items", ]
    list_display = order_list_displays
    list_filter = ["shipping_method", ]
    readonly_fields = order_read_only_fields
    actions = [pull_orders, cancel_orders, ]
    fields = order_fields

#  ORDERS PAID ------------------------------------------------------------------------------------------ END


class OrderResource(resources.ModelResource):

    def before_export(self, queryset, *args, **kwargs):
        for query in queryset:
            if query.shipping_method == "Plain White Envelop":
                query.delete()

    def after_export(self, queryset, data, *args, **kwargs):
        order_action.complete_orders(
            modeladmin=None, request=None, queryset=queryset, obj=CompletedOrder, order_status="Shipped", short_description="Ship Orders",
        )

    email = Field(attribute="email", column_name="Email")
    name = Field(attribute="name", column_name="Name")
    company = Field(attribute="company", column_name="Company")
    address_line_1 = Field(attribute="address_line_1", column_name="Address Line 1")
    address_line_2 = Field(attribute="address_line_2", column_name="Address Line 2")
    city = Field(attribute="city", column_name="City")
    state = Field(attribute="state", column_name="State")
    zip_code = Field(attribute="zip_code", column_name="Zip Code")
    country = Field(attribute="country", column_name="Country")
    order_number = Field(attribute="order_number", column_name="Order ID")

    class Meta:
        model = ReadyToShipOrder
        fields = ("email", "name", "company", "address_line_1", "address_line_2", "city", "state", "zip_code", "country", "order_number", )
        import_id_fields = ("order_number", )


@register(ReadyToShipOrder)
class ReadyToShipAdmin(ImportExportModelAdmin):
    resource_class = OrderResource
    ordering = ["order_creation_date", ]
    search_fields = ["name", "order_number", ]
    list_display = order_list_displays
    list_filter = ["shipping_method", ]
    readonly_fields = order_read_only_fields
    fields = order_fields


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
    ordering = ["order_creation_date", ]
    search_fields = ["name", "order_number", ]
    list_display = order_list_displays
    list_filter = ["shipping_method", ]
    readonly_fields = order_read_only_fields
    actions = [cancel_orders, ]
    fields = order_fields


@register(CompletedOrder)
class CompletedOrdersAdmin(ModelAdmin):
    ordering = ["order_creation_date", ]
    search_fields = ["name", "order_number", ]
    list_display = order_list_displays
    list_filter = ["shipping_method", ]
    readonly_fields = order_read_only_fields
    fields = order_fields



