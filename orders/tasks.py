from __future__ import absolute_import, unicode_literals

from time import localtime, strftime

from celery import shared_task
from customer.models import Customer
from django.db import transaction
from engine.tcgplayer_api import TcgPlayerApi
from engine.models import MTG
from engine.update_moose_tcg import moose_price
from mail.mailgun_api import MailGun
from orders.models import Order


api = TcgPlayerApi('moose')
mailgun = MailGun()

@shared_task(name='orders.tasks.update_moose_tcg')
def update_moose_tcg():
    moose_price()


# @shared_task(name='orders.tasks.process_order')
def process_order(request, cart, order_number, store_credit, discounts, ):

    product_list = list()
    ordered_items = ""
    missing_cards = list()

    # Handle cases where an item's quantity is changed before a customer checks out. Already saved items are reversed
    def stock_availability_error(name, expansion, printing, condition, language, quantity, price, total_price, product_id):
        missing_cards.append(
            f"{name}<attribute>{expansion}<attribute>"
            f"{printing}<attribute>{condition}<attribute>{language}<attribute>{quantity}<attribute>"
            f"{price}<attribute>{total_price}<attribute>{product_id}"
        )

    # create string reference of cart item to keep track of all items in a given order
    def save_item(name, expansion, printing, condition, language, quantity, price, total_price, ordered_items, product_id):
        cart_item = f"{name}<attribute>{expansion}<attribute>" \
                    f"{printing}<attribute>{condition}<attribute>{language}<attribute>{quantity}<attribute>" \
                    f"{price}<attribute>{total_price}<attribute>{product_id}<card>"

        return ordered_items + cart_item

    with transaction.atomic():
        # Create list of product ids without prepended sku identifier. maintained order and length are import to iterate using zip() later
        product_id_list = [i["product"][2:] for i in cart]

        # Create a query using the list of product ids. we use set in order to avoid redundant filters
        mtg_cards = MTG.objects.filter(product_id__in=list(set(product_id_list)))

        # iterate over each (cart item, product id) and remove them from inventory or call stock_availability_error(). Return to cart if error
        for item, product in zip(cart, product_id_list):
            product = mtg_cards.get(product_id=product)
            item_id = item["product"]
            condition = item["condition"]
            printing = item["printing"]
            quantity = item["quantity"]

            if printing == "Normal":
                if condition == "clean":
                    price = product.normal_clean_price
                    db_stock = product.normal_clean_stock
                    product.normal_clean_stock -= quantity
                    product_list.append([product, printing, condition, item["language"], quantity])
                    ordered_items = save_item(
                        name=item["name"],
                        expansion=item["expansion"],
                        printing=printing,
                        condition=condition,
                        language=item["language"],
                        quantity=quantity,
                        price=price,
                        total_price=item["total"],
                        ordered_items=ordered_items,
                        product_id=product.product_id,
                    )
                    product.save()

                    if db_stock < quantity:
                        stock_availability_error(
                            name=item["name"],
                            expansion=item["expansion"],
                            printing=item["printing"],
                            condition=item["condition"],
                            language=item["language"],
                            quantity=item["quantity"],
                            price=item["price"],
                            total_price=item["total"],
                            product_id=product,
                        )

                elif condition == "played":
                    price = product.normal_played_price
                    db_stock = product.normal_played_stock

                    product.normal_played_stock -= quantity
                    product_list.append([product, printing, condition, item["language"], quantity])
                    ordered_items = save_item(
                        name=item["name"],
                        expansion=item["expansion"],
                        printing=printing,
                        condition=condition,
                        language=item["language"],
                        quantity=quantity,
                        price=price,
                        total_price=item["total"],
                        ordered_items=ordered_items,
                        product_id=product.product_id,
                    )
                    product.save()

                    if db_stock < quantity:
                        stock_availability_error(
                            name=item["name"],
                            expansion=item["expansion"],
                            printing=item["printing"],
                            condition=item["condition"],
                            language=item["language"],
                            quantity=item["quantity"],
                            price=item["price"],
                            total_price=item["total"],
                            product_id=product,
                        )

                else:
                    price = product.normal_heavily_played_price
                    db_stock = product.normal_heavily_played_stock

                    product.normal_heavily_played_stock -= quantity
                    product_list.append([product, printing, condition, item["language"], quantity])
                    ordered_items = save_item(
                        name=item["name"],
                        expansion=item["expansion"],
                        printing=printing,
                        condition=condition,
                        language=item["language"],
                        quantity=quantity,
                        price=price,
                        total_price=item["total"],
                        ordered_items=ordered_items,
                        product_id=product.product_id,
                    )
                    product.save()

                    if db_stock < quantity:
                        stock_availability_error(
                            name=item["name"],
                            expansion=item["expansion"],
                            printing=item["printing"],
                            condition=item["condition"],
                            language=item["language"],
                            quantity=item["quantity"],
                            price=item["price"],
                            total_price=item["total"],
                            product_id=product,
                        )

            elif printing == "Foil":
                if condition == "clean":
                    price = product.foil_clean_price
                    db_stock = product.foil_clean_stock
                    product.foil_clean_stock -= quantity
                    product_list.append([product, printing, condition, item["language"], quantity])
                    ordered_items = save_item(
                        name=item["name"],
                        expansion=item["expansion"],
                        printing=printing,
                        condition=condition,
                        language=item["language"],
                        quantity=quantity,
                        price=price,
                        total_price=item["total"],
                        ordered_items=ordered_items,
                        product_id=product.product_id,
                    )
                    product.save()

                    if db_stock < quantity:
                        stock_availability_error(
                            name=item["name"],
                            expansion=item["expansion"],
                            printing=item["printing"],
                            condition=item["condition"],
                            language=item["language"],
                            quantity=item["quantity"],
                            price=item["price"],
                            total_price=item["total"],
                            product_id=product,
                        )

                elif condition == "played":
                    price = product.foil_played_price
                    db_stock = product.foil_played_stock
                    product.foil_played_stock -= quantity
                    product_list.append([product, printing, condition, item["language"], quantity])
                    ordered_items = save_item(
                        name=item["name"],
                        expansion=item["expansion"],
                        printing=printing,
                        condition=condition,
                        language=item["language"],
                        quantity=quantity,
                        price=price,
                        total_price=item["total"],
                        ordered_items=ordered_items,
                        product_id=product.product_id,
                    )
                    product.save()

                    if db_stock < quantity:
                        stock_availability_error(
                            name=item["name"],
                            expansion=item["expansion"],
                            printing=item["printing"],
                            condition=item["condition"],
                            language=item["language"],
                            quantity=item["quantity"],
                            price=item["price"],
                            total_price=item["total"],
                            product_id=product,
                        )

                else:
                    price = product.foil_heavily_played_price
                    db_stock = product.foil_heavily_played_stock
                    product.foil_heavily_played_stock -= quantity
                    product_list.append([product, printing, condition, item["language"], quantity])
                    ordered_items = save_item(
                        name=item["name"],
                        expansion=item["expansion"],
                        printing=printing,
                        condition=condition,
                        language=item["language"],
                        quantity=quantity,
                        price=price,
                        total_price=item["total"],
                        ordered_items=ordered_items,
                        product_id=product.product_id,
                    )
                    product.save()
                    if db_stock < quantity:
                        stock_availability_error(
                            name=item["name"],
                            expansion=item["expansion"],
                            printing=item["printing"],
                            condition=item["condition"],
                            language=item["language"],
                            quantity=item["quantity"],
                            price=item["price"],
                            total_price=item["total"],
                            product_id=product,
                        )

    new_order = Order(
        order_number=order_number,
        name=request.POST.get("name"),
        email=request.POST.get("email"),
        shipping_method=request.POST.get("shipping_method"),
        address_line_1=request.POST.get("address_line_1"),
        address_line_2=request.POST.get("address_line_2"),
        city=request.POST.get("city"),
        state=request.POST.get("state"),
        zip_code=request.POST.get("zip_code"),
        phone=request.POST.get("phone_number"),
        total_order_price=request.POST.get("final_total"),
        store_credit_used=store_credit,
        tax_charged=request.POST.get("tax"),
        shipping_charged=request.POST.get("shipping_charged"),
        discounts_applied=discounts,
        discounts_code_used=request.POST.get("discount_name"),
        notes=request.POST.get("notes"),
        order_view=f"{request.META['HTTP_HOST']}/orders/admin/{order_number}",
        ordered_items=ordered_items,
        missing_cards=missing_cards,
        payer_id='',

    )

    try:
        # If customer has an account, retrieve it and append the ordered items + order details
        date_time_processed = strftime("%Y-%m-%d at %I:%M%p", localtime())
        customer = Customer.objects.get(email=request.POST.get("email"))
        customer.orders = customer.orders + ordered_items + f"{date_time_processed}<card>{order_number}<card>" \
                                                            f"{request.POST.get('final_total')}<card><status_start>Pulling<status_end><order>"
        customer.save()

    except Customer.DoesNotExist:
        pass

    new_order.save()

    product_string = '\n'.join([f"{i['language']} | {i['name']} | {i['expansion']} | {i['printing']} | "
                                f"{i['condition']} | qty: {i['quantity']} | price: ${i['price']} | total: ${i['total']}" for i in cart])

    message = f"Your order has be received. We are in the process of pulling your items and once they are packaged, you " \
              f"will receive an email with the shipping status of your order along with tracking (if applicable). For reference here are your order " \
              f"details:\n\nOrder Number: {order_number}\n" \
              f"Ship to:\n{request.POST.get('name')}\n{request.POST.get('address_line_1')} {request.POST.get('address_line_2')}\n" \
              f"{request.POST.get('city')}, {request.POST.get('state')} {request.POST.get('zip_code')}\n{request.POST.get('shipping_method')}\n\n" \
              f"{product_string}\nShipping: {request.POST.get('shipping_charged')}\n Tax: {request.POST.get('tax')}\n" \
              f"Final Total: ${request.POST.get('final_total')}"

    mailgun.send_mail(
        recipient_list=request.POST.get('email'),
        subject=f"Order confirmation #{order_number}",
        message=message,
    )





