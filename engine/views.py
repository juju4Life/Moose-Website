import astfrom datetime import datetimefrom decimal import Decimalimport randomfrom django.shortcuts import render, redirectfrom django.http import JsonResponsefrom django.shortcuts import get_object_or_404from django.db.models import Qfrom django.core.mail import send_mailfrom buylist.models import HotListfrom engine.models import MTG, MtgCardInfofrom engine.cart import Cartfrom engine.forms import contactForm, AdvancedSearchFormfrom engine.config import paginationfrom engine.tasks import complete_orderfrom engine.tcgplayer_api import TcgPlayerApifrom layout.models import HomePageLayoutfrom ppal.paypal_api import PaypalApifrom ppal.models import PaypalOrderfrom rest_framework.views import APIViewfrom rest_framework.response import Responsetcg = TcgPlayerApi('first')paypal = PaypalApi()def home_base(request):    cart = Cart(request)    cart_length = cart.cart_length    response = render(None, 'home_base.html', {'cartLength': cart_length})    visits = int(request.COOKIES.get('visits', '0'))    if 'last_visit' in request.COOKIES:        last_visit = request.COOKIES['last_visit']        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")        if (datetime.now() - last_visit_time).days > 0:            response.set_cookie('visits', visits + 1)            response.set_cookie('last_visit', datetime.now())    else:        response.set_cookie('last_visit', datetime.now())    return responsedef home(request):    hotlist = HotList.objects.all()    home_page_objcets = HomePageLayout.objects.all()    main_slide = home_page_objcets.get(name='Main Image')    context = {        'hotlist': hotlist,        'main_slide': main_slide,    }    return render(request, 'home.html', context)class CardDatabase(APIView):    def get(self, request, format=None):        cards = MtgCardInfo.objects.all()        data = {           'names': cards.filter(card_identifier="name").values_list("name", flat=True),           'expansions': cards.filter(card_identifier="expansion").values_list("name", flat=True),           'card_types': cards.filter(card_identifier="card_type").values_list("name", flat=True),           'subtypes': cards.filter(card_identifier="subtypes").values_list("name", flat=True),           'layouts': cards.filter(card_identifier="layout").values_list("name", flat=True),           'artists': cards.filter(card_identifier="artist").values_list("name", flat=True),           'rarities': cards.filter(card_identifier="rarity").values_list("name", flat=True),           'colors': ["Black", "Blue", "Green", "Red", "White"],        }        return Response(data)def search(request):    template = 'search_result.html'    context = dict()    query = request.GET.get('q')    error = ''    print(request.POST)    form = AdvancedSearchForm(request.GET)    if request.GET.get("advanced-search-form"):        if form.is_valid():            name_query = form.cleaned_data["name_query"]            name = form.cleaned_data["name"]            expansion = form.cleaned_data["expansion"]            artist = form.cleaned_data["artist"]            oracle_text = form.cleaned_data["oracle_text"]            colors = form.cleaned_data["colors"]            color_identity = form.cleaned_data["color_identity"]            rarity = form.cleaned_data["rarity"]            card_type = form.cleaned_data["card_type"]            subtypes = form.cleaned_data["subtypes"]            power_start = form.cleaned_data["power_start"]            power_end = form.cleaned_data["power_end"]            toughness_start = form.cleaned_data["toughness_start"]            toughness_end = form.cleaned_data["toughness_end"]            cmc_start = form.cleaned_data["cmc_start"]            cmc_end = form.cleaned_data["cmc_end"]            query_list = list()            advanced_query = MTG.objects            if expansion:                advanced_query = advanced_query.filter(expansion=expansion)                query_list.append({"col": "Set", "value": expansion})            if name:                if name_query == 'contains':                    advanced_query = advanced_query.filter(name__icontains=name)                else:                    advanced_query = advanced_query.filter(name__iexact=name)                    query_list.append({"col": "Name", "value": name})            if colors:                colors = "".join(colors)                advanced_query = advanced_query.filter(colors=colors)                query_list.append({"col": "Colors", "value": colors})            if color_identity:                color_identity = "".join(color_identity)                advanced_query = advanced_query.filter(color_identity=color_identity)                query_list.append({"col": "Color Identity", "value": color_identity})            if rarity:                advanced_query = advanced_query.filter(rarity__in=rarity)                query_list.append({"col": "Rarity", "value": rarity})            if card_type:                for ct in card_type:                    advanced_query = advanced_query.filter(card_type__icontains=ct)                query_list.append({"col": "Card Types", "value": card_type})            if subtypes:                subtypes = subtypes.split(",")[0:-1]                for subtype in subtypes:                    advanced_query = advanced_query.filter(subtypes__icontains=subtype.strip())                query_list.append({"col": "Subtypes", "value": subtypes})            if artist:                artist = artist.split(",")[0:-1]                for art_person in artist:                    advanced_query = advanced_query.filter(artist__icontains=art_person.strip())                query_list.append({"col": "Artist", "value": artist})            if power_start:                advanced_query = advanced_query.filter(power__range=(power_start, power_end))                query_list.append({"col": "Power", "value": f"{power_start} to {power_end}"})            if toughness_start:                advanced_query = advanced_query.filter(toughness__range=(toughness_start, toughness_end))                query_list.append({"col": "Toughness", "value": f"{toughness_start} to {toughness_end}"})            if cmc_start:                advanced_query = advanced_query.filter(converted_mana_cost__range=(cmc_start, cmc_end))                query_list.append({"col": "Converted Mana Cost", "value": f"{cmc_start} to {cmc_end}"})            if oracle_text:                queries = oracle_text.split()                for query in queries:                    advanced_query = advanced_query.filter(oracle_text__icontains=query.strip())                query_list.append({"col": "Oracle Text Contains", "value": queries})            context["advanced_query"] = query_list            form = AdvancedSearchForm()            results = advanced_query        else:            results = []            error = "error"    else:        form = AdvancedSearchForm()        if query:            results = MTG.objects.filter(name=query)        else:            # results = MTG.objects.all(). order_by('product_name')            error = 'error'            results = []    if results:        pages = pagination(request, results, 10)        context['items'] = pages[0]        context['page_range'] = pages[1]    else:        error = "empty query"    context['error'] = error    context['query'] = query    context['form'] = form    get_copy = request.GET.copy()    parameters = get_copy.pop('page', True) and get_copy.urlencode()    context['parameters'] = parameters    return render(request, template, context)def product_detail(request, product_id):    product = MTG.objects.filter(product_id=product_id)    # versions = object.objects.filter(name=products)    return render(request, 'product_detail.html', {'product': product[0]})def orders_view(request, product_info):    results = product_info.replace('+', ' ').replace('\n', '').split('\r')    print(results)    quantity = {i[1:].lower(): {'q': i[0]} for i in results if i != ''}    print(quantity)    results = [i[1:] for i in results if i != '']    products = object.objects.filter(name__in=results).order_by('name')    q = [quantity[i.name.lower()]['q'] for i in products]    print(q)    order = zip(products, q)    return render(request, 'order_results.html', {'results': order})def get_cart(request):    cart = Cart(request)    length = cart.cart_length    sub_total = cart.total_price    return render(request, 'cart.html', {'cart': cart, 'length': length, 'sub_total': sub_total})def add_to_cart(request, product_id):    quantity = request.POST.get('quantity')    # condition = request.POST.get('condition')    # language = request.POST.get('language')    products = get_object_or_404(MTG, id=product_id)    price = products.price    total = price * Decimal(quantity)    cart = Cart(request)    cart.add(product_id, products.product_name, price, products.set_name, condition='NM', language='English', total=total, quantity=quantity)    return redirect('cart')def remove_from_cart(request, product_id):    products = []    cart = Cart(request)    cart.remove(products)    return redirect('cart')def clear(request):    cart = Cart(request)    cart.clear()    return redirect('cart')def paypal_transaction(request, name, email):    if request:        data = ast.literal_eval(request.body.decode('utf-8'))        data = data['data']        paypal_data = paypal.get_order(data['orderID'])        if paypal_data.get('error') == 'invalid_token':            paypal.get_access_token()            paypal_data = paypal.get_order(data['orderID'])        order_id = data.get('orderID', random.sample(range(10000000, 99999999), 1))        order_info = paypal_data['purchase_units'][0]        payment_status = order_info['payments']['captures'][0]['status']        if payment_status == 'COMPLETED':            cart = Cart(request)            cart_data = [i for i in cart]            complete_order.apply_async(que='low_priority', args=(cart_data, name, email, order_id, ))            cart.clear()            amount = order_info['amount']['value']            amount_currency_type = order_info['amount']['currency_code']            seller_email = order_info['payee']['email_address']            merchant_id = order_info['payee']['merchant_id']            shipping_name = order_info['shipping']['name']['full_name']            address_line_1 = order_info['shipping']['address']['address_line_1']            admin_area_2 = order_info['shipping']['address']['admin_area_2']            admin_area_1 = order_info['shipping']['address']['admin_area_1']            postal_code = order_info['shipping']['address']['postal_code']            country_code = order_info['shipping']['address']['country_code']            payment_id = order_info['payments']['captures'][0]['id']            paypal_fee = order_info['payments']['captures'][0]['seller_receivable_breakdown']['paypal_fee']['value']            net = order_info['payments']['captures'][0]['seller_receivable_breakdown']['net_amount']['value']            create_time = order_info['payments']['captures'][0]['create_time']            update_time = order_info['payments']['captures'][0]['update_time']            first_name = paypal_data['payer']['name']['given_name']            last_name = paypal_data['payer']['name']['surname']            payer_email = paypal_data['payer']['email_address']            payer_id = paypal_data['payer']['payer_id']            payer_country_code = paypal_data['payer']['address']['country_code']            paypal_record = PaypalOrder(                order_id=order_id,                amount=amount,                amount_currency_type=amount_currency_type,                my_email=seller_email,                merchant_id=merchant_id,                shipping_name=shipping_name,                address_line_1=address_line_1,                admin_area_1=admin_area_1,                admin_area_2=admin_area_2,                postal_code=postal_code,                country_code=country_code,                payment_id=payment_id,                payment_status=payment_status,                paypal_fee=paypal_fee,                net=net,                create_time=create_time,                update_time=update_time,                first_name=first_name,                last_name=last_name,                customer_payment_email=payer_email,                customer_contact_email=email,                checkout_name=name,                customer_id=payer_id,                customer_country_code=payer_country_code,            )            paypal_record.save()            grand_total = sum([float(i['total']) for i in cart_data])            new_order = [                f"{i['quantity']} {i['name']}, ({i['set_name']}) ${i['price']} | Total: ${i['total']}\n"                for i in cart_data            ]            subject = 'Order Received'            message = f"Order #{order_id}\n\n" \                f"{''.join(new_order)}\n" \                f"Grand Total: {grand_total}"            recipient_list = ['sales@mtgfirst.com']            from_mail = 'MTGFirst'            send_mail(subject=subject, message=message, recipient_list=recipient_list, from_email=from_mail)        return JsonResponse({"success": 'True'})    else:        return JsonResponse({'success': 'False'})def order_confirmation(request):    events = []    template = 'order_complete.html'    context = {'events': events}    return render(request, template, context)def payment(request):    name = request.POST.get('name')    email = request.POST.get('email')    cart = Cart(request)    total = cart.total_price    template = 'payment.html'    context = {        'total': total,        'name': name,        'email': email,    }    return render(request, template, context)def checkout(request):    cart = Cart(request)    sub_total = cart.total_price    length = len(cart)    title = ''    form = contactForm(request.POST or None)    confirm_message = None    '''paypal_dict = {        "business": "mtgfirststore-facilitator@gmail.com",        "amount": sub_total,        "item_name": 'mtg singles',        "invoice": "unique-invoice-id",        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),        "return": request.build_absolute_uri(reverse('home')),        "cancel_return": request.build_absolute_uri(reverse('home')),        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)    }    paypal_form = PayPalPaymentsForm(initial=paypal_dict)'''    if form.is_valid():        name = form.cleaned_data['name']        notes = form.cleaned_data['notes']        email = form.cleaned_data['email']        # send_order.apply_async(que='high_priority', args=(cart, name, notes, email))        title = 'Your order has been placed' \                'You will be contacted once we have checked availability and pricing for your list.' \                'Thank you for shopping with MTG First'        confirm_message = 'You will receive an email confirmation shortly'        form = None    return render(request, 'checkout.html', {'cart': cart, 'length': length,                                             'title': title, 'form': form, 'confirm_message': confirm_message, 'sub_total': sub_total})def thanks(request):    return render(request, 'thank-you.html')