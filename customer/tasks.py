from __future__ import absolute_import, unicode_literals
from celery import shared_task
from customer.secrets import Secrets
from engine.models import Product
from engine.tcgplayer_api import TcgPlayerApi
from engine.tcg_credentials import Credentials
from datetime import datetime
from django.core.mail import send_mail
from customer.models import OrderRequest


tcg = TcgPlayerApi()
credentials = Credentials()


@shared_task(name='customer.tasks.send_order')
def send_order(cart, name, notes, email, phone_number, contact_type):
    text = ''
    url = 'https://www.tcgfirst.com//order_view/'
    for each in cart:
        text = text + str(each['quantity']) + each['name'].replace(' ', '+').replace("'", '%27').replace(",", '%2C') + "%0D%0A"
    versions = Product.objects.only('set_name', 'name', 'tcg_player_id').filter(name__in=[i['name'] for i in cart])
    ver = [{'name': v.name, 'set_name': v.set_name, 'qty': tcg.search_inventory(str(v.tcg_player_id))} for v in versions]
    new_list = sorted(cart, key=lambda k: k['set_name'])
    shopping_cart = ["{}x {} ({}) | {} | ${} each | {}".format(
        i['quantity'],
        i['name'],
        i['rarity'],
        i['set_name'],
        i['price'],
        ["{}: {}".format(v['set_name'], v['qty']) for v in ver if i['name'] == v['name']]) for i in new_list]

    # shopping_cart.sort(key=attrgetter('set_name'))
    no_price = ["{}({})".format(i['name'], i['set_name']) for i in new_list if i['price'] == 0.]
    final_price = (format(sum(i['quantity'] * float(i['price']) for i in new_list), '.2f'))
    email_cart = '\n\n'.join(shopping_cart)
    no_price = ','.join(no_price)
    url = url + text
    date = datetime.now()

    order_requested = OrderRequest(
        name=name, contact_type=contact_type, email=email, phone=phone_number, missing=no_price, total=final_price,
        notes=notes, order=email_cart, order_link=url, date=date

    )
    order_requested.save()
    order_id = OrderRequest.objects.get(date=date).id
    cart.clear()
    def send():
        from customer.facebook import FacebookBot
        facebook_bot = FacebookBot()
        facebook_bot.send_message(
            "TEST Order Request for {}\n"
            "Link to Order:\nhttps://www.tcgfirst.com/admin/customer/orderrequest/{}/change/".format(name, order_id)
        )

    send()
    # Link to Order:\nhttps://www.tcgfirst.com/admin/customer/orderrequest/{}/change/


@shared_task(name='customer.tasks.alert')
def alert(ip, obj_name, obj_credit, obj_id):
    time_of_change = datetime.now()
    ip_list = ['73.201.91.50', '208.54.70.156', '99.203.1.55', '2600:1:9103:7512:245a:71d4:7', '172.56.7.5', '66.87.112.131', '172.58.110.200']
    if str(ip) not in ip_list:
        subject = 'Odd Activity Detected in Store Credit Database'
        message = "A change was made to the store credit system from an unauthorized Source.\n" \
                  "TIME: {}\n" \
                  "IP ADDRESS: {}\n" \
                  "Name: {}\n" \
                  "Current Store Credit: {}\n" \
                  "Unique ID: {}\n".format(
                        time_of_change, ip, obj_name, obj_credit, obj_id,
        )

        emailFrom = 'DATABASE ALERTS'
        emailTo = ['jermol@mtgfirst.com', 'jason@mtgfirst.com']
        send_mail(subject, message, emailFrom, emailTo, fail_silently=True)


@shared_task(name='customer.tasks.update_tcg_key')
def update_tcg_key():
    credentials.new_bearer_token()


@shared_task()
def awake():
    from customer.facebook_listen import ListenBot
    client = ListenBot(Secrets.facebook_email, Secrets.facebook_password)
    while True:
        if not client.onListening():
            if not client.isLoggedIn():
                client = ListenBot(Secrets.facebook_email, Secrets.facebook_password)
            client.listen(end_time=10)


@shared_task(name='customer.tasks.add_buylist_item')
def add_buylist_item(name):
    results = Product.objects.filter(name=name.strip())
    if not results.exists():
        def send():
            from customer.facebook import FacebookBot
            facebook_bot = FacebookBot()
            facebook_bot.send_message(
                "'{}' Not added to buylist. Please Correct your spelling".format(name)

            )

        send()
    else:
        delete = False
        for results_cards in results:
            card_info = tcg.get_card_info(results_cards.tcg_player_id)['results']
            for card in card_info:
                for card_sku in card['productConditions']:
                    if card_sku['isFoil'] == False:
                        if card_sku['name'] == 'Near Mint':
                            tcg.create_buylist_item(card_sku['productConditionId'], .01, _json=True)
                            print('added')
                            delete = True
                        elif card_sku['name'] == 'Lightly Played':
                            tcg.create_buylist_item(card_sku['productConditionId'], .01, _json=True)
                            print('added')
                            delete = True
                        elif card_sku['name'] == 'Moderately Played':
                            tcg.create_buylist_item(card_sku['productConditionId'], .01, _json=True)
                            print('added')
                            delete = True
        if delete == False:
            def send():
                from customer.facebook import FacebookBot
                facebook_bot = FacebookBot()
                facebook_bot.send_message(
                    "There was an error adding {} to buylist".format(name)

                )

            send()


