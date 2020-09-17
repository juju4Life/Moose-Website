

def ordered_items_template(cart, total):
    items = [
        f"{i['printing']} | {i['language']} | {i['name']} | {i['expansion']} | Qty. {i['quantity']} | Price: ${i['price']} | Total: ${i['total']}"
        for i in cart
    ]
    items.append(f"Grand Total: ${total}\n")

    return '\n'.join(items)


def customer_info_template(order_type, order_number, name, address_line_1, address_line_2, city, state, zip_code, payment_type=None,
                           paypal_email=None):

    info = f"{order_type} {order_number}\n{name}\n{address_line_1} {address_line_2}\n{city}, {state} {zip_code}"

    if payment_type:
        info = info + f"\nPayment Type: {payment_type}"
        if payment_type == "paypal":
            info = info + f" Paypal email: {paypal_email}"

    return info


def company_buylist_shipping_info(buylist_number):
    value = f"MooseLoot\nattn buylist {buylist_number}\n5356 Chase Lions Way\nColumbia, MD 21044"
    return value


