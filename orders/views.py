from datetime import datetime


from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from orders.models import Order, OrdersLayout


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

    cards_from_active_orders = ''.join([i.ordered_items for i in Order.objects.all()])
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

    orders = Order.objects.filter(active=True)
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
