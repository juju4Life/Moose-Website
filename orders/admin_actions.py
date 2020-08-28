
from customer.models import Customer
from django.shortcuts import redirect
from engine.models import MTG
from my_customs.functions import text_between_two_words
from tcg.tcg_functions import adjust_product_quantity


class OrderAction:

    @staticmethod
    def process_instance(instance, obj, order_status):

        new = obj(
            order_number=instance.order_number,
            order_creation_date=instance.order_creation_date,
            order_status=order_status,
            name=instance.name,
            email=instance.email,
            shipping_method=instance.shipping_method,
            address_line_1=instance.address_line_1,
            address_line_2=instance.address_line_2,
            city=instance.city,
            state=instance.state,
            zip_code=instance.zip_code,
            phone=instance.phone,
            total_order_price=instance.total_order_price,
            store_credit_used=instance.store_credit_used,
            tax_charged=instance.tax_charged,
            shipping_charged=instance.shipping_charged,
            discounts_applied=instance.discounts_applied,
            discounts_code_used=instance.discounts_code_used,
            notes=instance.notes,
            ordered_items=instance.ordered_items,
            order_view=instance.order_view,
            tracking_number=instance.tracking_number,
            payer_id=instance.payer_id,

        )
        new.save()

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

        for order in queryset:
            self.change_order_status(email=order.email, order_number=order.order_number, order_status=order_status)
        queryset.delete()
        return redirect("admin/orders")

    def cancel_orders(self, modeladmin, request, queryset, obj, order_status, short_description):
        self.process_action(modeladmin=modeladmin, request=request, queryset=queryset, obj=obj, order_status=order_status, short_description=short_description)

        for order in queryset:
            self.change_order_status(email=order.email, order_number=order.order_number, order_status=order_status)
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
                    product_id=product_id,
                )

        queryset.delete()

    @staticmethod
    def change_order_status(email, order_number, order_status):

        if Customer.objects.filter(email=email).exists():
            customer = Customer.objects.get(email=email)
            orders = customer.orders
            split_orders = orders.split("<order>")[:-1]
            for each_order in split_orders[::-1]:
                if order_number in each_order:
                    old_status = text_between_two_words("<status_start>", "<status_end>", each_order)
                    new_status = f"<status_start>{order_status}<status_end>"
                    updated_order = each_order.replace(f"<status_start>{old_status}<status_end>", new_status)
                    customer.orders = customer.orders.replace(each_order, updated_order)
                    customer.save()
                    break



