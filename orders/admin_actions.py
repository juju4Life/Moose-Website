from django.shortcuts import redirect
from engine.models import MTG
from tcg.tcg_functions import adjust_product_quantity


class OrderAction:

    @staticmethod
    def process_action(modeladmin, request, queryset, obj, order_status, short_description):
        save_list = list()
        for each in queryset:
            save_list.append(
                obj(
                    order_number=each.order_number,
                    order_creation_date=each.order_creation_date,
                    order_status=order_status,
                    name=each.name,
                    email=each.email,
                    shipping_method=each.shipping_method,
                    address_line_1=each.address_line_1,
                    address_line_2=each.address_line_2,
                    city=each.city,
                    state=each.state,
                    zip_code=each.zip_code,
                    phone=each.phone,
                    total_order_price=each.total_order_price,
                    store_credit_used=each.store_credit_used,
                    tax_charged=each.tax_charged,
                    shipping_charged=each.shipping_charged,
                    discounts_applied=each.discounts_applied,
                    discounts_code_used=each.discounts_code_used,
                    notes=each.notes,
                    ordered_items=each.ordered_items,
                    order_view=each.order_view,
                    tracking_number=each.tracking_number,
                    payer_id=each.payer_id,
                )
            )

        obj.objects.bulk_create(save_list)
        obj.short_description = short_description

    def pull_orders(self, modeladmin, request, queryset, obj, order_status, short_description):
        self.process_action(modeladmin=modeladmin, request=request, queryset=queryset, obj=obj, order_status=order_status, short_description=short_description)
        queryset.delete()
        return redirect("admin/orders")

    def complete_orders(self, modeladmin, request, queryset, obj, order_status, short_description):
        self.process_action(modeladmin=modeladmin, request=request, queryset=queryset, obj=obj, order_status=order_status, short_description=short_description)
        queryset.delete()
        return redirect("admin/orders")

    def cancel_orders(self, modeladmin, request, queryset, obj, order_status, short_description):
        self.process_action(modeladmin=modeladmin, request=request, queryset=queryset, obj=obj, order_status=order_status, short_description=short_description)

        for order in queryset:
            items = order.ordered_items.split("<card>")[:-1]
            for item in items:
                card = item.split("<attribute>")
                printing = card[2]
                condition = card[3]
                quantity = card[5]
                product_id = card[8]
                adjust_product_quantity(
                    obj=MTG,
                    printing=printing,
                    condition=condition,
                    quantity=quantity,
                    product_id=product_id
                )
        queryset.delete()


