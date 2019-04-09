from __future__ import absolute_import, unicode_literals
from celery import shared_task
from decimal import Decimal
from customer.models import Customer, ItemizedPreorder, Preorder, PreordersReady
from my_customs.decorators import report_error
from django.core.mail import send_mail
from decouple import config


@shared_task(name='engine.tasks.complete_order')
@report_error
def complete_order(cart, name, email, order_number):
    print(cart, name, email, order_number)
    db = ItemizedPreorder.objects
    ordered_items = ''
    grand_total = sum([float(i['total']) for i in cart])
    for each in cart:
        quantity = int(each['quantity'])
        total_price = Decimal(each['price']) * quantity
        preorder = f"{each['name']} ({each['set_name']})"
        customer = Customer.objects.get_or_create(name=name)[0]
        if customer.email == '':
            customer.email = email
            customer.save()

        product = Preorder.objects.get_or_create(product=preorder)[0]

        new_preorder = PreordersReady(
            customer_name=customer,
            email=email,
            product=product,
            price=total_price,
            paid=total_price,
            quantity=each['quantity'],
            preorder_type='Single',
            employee_initials='Web',
        )
        new_preorder.save()

        card = db.get(id=each['product'])
        card.quantity -= quantity
        card.total_sold += quantity
        if card.quantity < 1:
            card.available = False
        card.save()

        ordered_items = ordered_items + f"{each['quantity']} {each['condition']} {each['name']} ({each['set_name']} - ${each['price']} - Total: ${each['total']})\n"

    message = [
        f'Hello {name},\n\n'
        'We have received your order. They will be available for pickup on Friday, May 3rd. Your order details are below\n'
        f'Order Number: {order_number}\n'
        f'{ordered_items}\n'
        f'Grand Total: {grand_total}'
    ]
    subject = f'Order #{order_number} from TCGFirst.com has been received'
    from_mail = 'TCGFirst.com'
    recipient_list = [email, ]

    send_mail(subject=subject, message=message, from_email=from_mail, recipient_list=recipient_list)



