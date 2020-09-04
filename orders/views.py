
from datetime import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from orders.models import Order, OrdersLayout, PullingOrder, ReadyToShipOrder
from ppal.paypal_setup import PayPal

paypal = PayPal()


def confirm_payment(request):

    context = dict()
    template = "confirm_payment.html"

    is_paid = False

    order_number = request.GET.get("token")
    payer_id = request.GET.get("PayerID")

    if order_number and payer_id:
        paypal_payment = paypal.get_order(order_number)
        if paypal_payment == "APPROVED":
            order = Order.objects.get(order_number=order_number)
            order.order_paid = True
            order.payer_id = payer_id
            order.save()
            is_paid = True
        else:
            pass

    context["is_paid"] = is_paid
    context["order_number"] = order_number

    return render(request, template, context)


@staff_member_required
def order_view(request, order_number):
    context = dict()
    template = "order_view.html"
    ordered_items = list()

    order = Order.objects.get(order_number=order_number)
    cards = order.ordered_items.split("<card>")[:-1]

    for c in cards:
        card = c.split("<attribute>")
        ordered_items.append(
            {
                "name": card[0],
                "expansion": card[1],
                "printing": card[2],
                "condition": card[3],
                "language": card[4],
                "quantity": card[5],
                "price": card[6],
                "total": card[7],
            }
        )
    context["order"] = order
    context["cards"] = ordered_items

    return render(request, template, context)


@staff_member_required
def pull_sheet(request):
    context = dict()
    template = "pull_sheet.html"
    cards = dict()

    cards_from_active_orders = ''.join([i.ordered_items for i in PullingOrder.objects.all()])
    cards_from_active_orders = cards_from_active_orders.split("<card>")[:-1]
    for card in cards_from_active_orders:
        attributes = card.split("<attribute>")
        name = attributes[0]
        expansion = attributes[1]
        printing = attributes[2]
        condition = attributes[3]
        language = attributes[4]
        quantity = attributes[5]
        # price = attributes[6]
        # total = attributes[7]

        sku = f"{language}_{printing}_{condition}_{name}_{expansion}"
        if not cards.get(sku):
            cards[sku] = dict()

        try:
            cards[sku]["quantity"] += int(quantity)
        except KeyError:
            cards[sku]["quantity"] = 0
            cards[sku]["quantity"] += int(quantity)

        cards[sku]["name"] = name
        cards[sku]["expansion"] = expansion
        cards[sku]["language"] = language
        cards[sku]["printing"] = printing.upper()
        cards[sku]["condition"] = condition

    cards = sorted([i for i in cards.values()], key=lambda k: k["name"])
    context["cards"] = cards

    pull_order_created = datetime.now().strftime("%m/%d - %I:%M%p")
    context["time_created"] = pull_order_created

    return render(request, template, context)


@staff_member_required
def packing_slips(request, order_number):
    context = dict()
    template = "packing_slips.html"
    packing_slip_note = OrdersLayout.objects.get(name="packing_slip_note")
    all_items = list()

    orders = PullingOrder.objects.all()
    if order_number.lower() != "all":
        orders = orders.filter(order_number=order_number)

    for order in orders:
        items = order.ordered_items.split("<card>")[:-1]
        ordered_items = list()
        for item in items:
            card = item.split("<attribute>")
            name = card[0]
            expansion = card[1]
            printing = card[2]
            condition = card[3]
            language = card[4]
            quantity = card[5]
            price = card[6]
            total = card[7]

            ordered_items.append(
                {
                    "name": name,
                    "expansion": expansion,
                    "printing": printing,
                    "condition": condition,
                    "language": language,
                    "quantity": quantity,
                    "price": price,
                    "total": total,
                }
            )

        all_items.append(ordered_items)

    orders = zip(orders, all_items)

    context["orders"] = orders
    context["note"] = packing_slip_note

    return render(request, template, context)


@staff_member_required
def ready_to_ship(request):
    if request.GET:
        if request.GET.get("ready_to_ship"):
            order_numbers = [i for i in request.GET.getlist("ready_to_ship")]
            pulled_orders = PullingOrder.objects.filter(order_number__in=order_numbers)
            move_list = list()

            for order in pulled_orders:
                move_list.append(
                    ReadyToShipOrder(
                        order_number=order.order_number,
                        order_creation_date=order.order_creation_date,
                        order_status="",
                        name=order.name,
                        email=order.email,
                        shipping_method=order.shipping_method,
                        address_line_1=order.address_line_1,
                        address_line_2=order.address_line_2,
                        city=order.city,
                        state=order.state,
                        zip_code=order.zip_code,
                        phone=order.phone,
                        total_order_price=order.total_order_price,
                        store_credit_used=order.store_credit_used,
                        tax_charged=order.tax_charged,
                        shipping_charged=order.shipping_charged,
                        discounts_applied=order.discounts_applied,
                        discounts_code_used=order.discounts_code_used,
                        notes=order.notes,
                        ordered_items=order.ordered_items,
                        order_view=order.order_view,
                        send_message="",
                        tracking_number=order.tracking_number,
                        payer_id=order.payer_id,
                    )
                )

            ReadyToShipOrder.objects.bulk_create(move_list)
            pulled_orders.delete()

    return redirect("/admin/orders/readytoshiporder/")


