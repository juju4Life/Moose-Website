import csvfrom datetime import datetimefrom decimal import Decimalimport iofrom buylist.models import HotListfrom customer.models import Customer, CustomerRestockNoticefrom django.db import transactionfrom django.contrib import messagesfrom django.contrib.admin import AdminSitefrom django.contrib.admin.views.decorators import staff_member_requiredfrom django.db.models import Qfrom django.http import JsonResponse, HttpResponsefrom django.shortcuts import render, redirectfrom engine.cart import Cartfrom engine.config import paginationfrom engine.data_query import process_filterfrom engine.forms import AdvancedSearchForm, SuppliesAdvancedQueryFormfrom engine.models import DailyMtgNews, MTG, MtgCardInfo, MTGUpload, StateInfo, MTGDatabase, SickDealfrom engine.tasks import upload_mtg_cardsfrom engine.tcgplayer_api import TcgPlayerApifrom layout.models import HomePageLayout, Text, PreorderItem, CompanyAddressfrom orders.models import ShippingMethod, Couponfrom orders.tasks import process_orderfrom ppal.paypal_setup import PayPalfrom pytz import timezonefrom rest_framework.views import APIViewfrom rest_framework.response import Responsefrom users.forms import GuestCheckoutFormtcg = TcgPlayerApi('first')paypal = PayPal()def add_to_cart(request, product_id):    quantity = request.POST.get('quantity')    if not quantity.isnumeric():        quantity = 1    condition = request.POST.get('condition')    printing = request.POST.get('printing')    price = request.POST.get('price')    name = request.POST.get('name')    expansion = request.POST.get('expansion')    language = request.POST.get('language')    max_quantity = request.POST.get('max_quantity')    total = Decimal(price) * int(quantity)    # Create unique sku based on printing and condition in order to add variation of the same product to cart    sku = ''    if printing == "Normal":        sku += "a"    else:        sku += "b"    if condition == "clean":        sku += "c"    elif condition == "played":        sku += "p"    elif condition == "heavily_played":        sku += "h"    else:        pass    identifier = f"add-to-cart-{printing}-{condition}-{product_id}"    message = "cart updated"    product_id = sku + product_id    cart = Cart(request)    cart.add(        product_id=product_id,        name=name,        expansion=expansion,        condition=condition,        printing=printing,        price=price,        language=language,        total=total,        quantity=quantity,        max_quantity=max_quantity,    )    return JsonResponse({"success": "true", "id": identifier, "message": message})# Ajax call data to use for autucomplete fieldsclass CardDatabase(APIView):    @staticmethod    def get(request, format=None):        cards = MtgCardInfo.objects.all()        data = {           'names': cards.filter(card_identifier="name").values_list("name", flat=True),           'expansions': cards.filter(card_identifier="expansion").values_list("name", flat=True),           'card_types': cards.filter(card_identifier="card_type").values_list("name", flat=True),           'subtypes': cards.filter(card_identifier="subtypes").values_list("name", flat=True),           'layouts': cards.filter(card_identifier="layout").values_list("name", flat=True),           'artists': cards.filter(card_identifier="artist").values_list("name", flat=True),           'rarities': cards.filter(card_identifier="rarity").values_list("name", flat=True),           'colors': ["Black", "Blue", "Green", "Red", "White"],        }        return Response(data)# Empty cartdef clear(request):    cart = Cart(request)    cart.clear()    return redirect('cart')def checkout(request):    context = dict()    template = "checkout.html"    if request.user.is_authenticated and request.POST.get("change_address"):        email = request.user.email        customer = Customer.objects.get(email=email)        shipping_name = request.POST.get("name")        address_line_1 = request.POST.get("address_line_1")        address_line_2 = request.POST.get("address_line_2")        city = request.POST.get("city")        state = request.POST.get("state")        zip_code = request.POST.get("zip_code")        customer.shipping_name = shipping_name        customer.address_line_1 = address_line_1        customer.address_line_2 = address_line_2        customer.city = city        customer.state = state        customer.zip_code = zip_code        customer.save()        return redirect("checkout")    elif request.user.is_authenticated or request.GET.get("guest"):        address_form = GuestCheckoutForm()        cart = Cart(request)        if cart.total_price > 49.99:            shipping_methods = ShippingMethod.objects.all().exclude(clean_name="standard")        else:            shipping_methods = ShippingMethod.objects.all().exclude(clean_name="free_shipping")        context["cart"] = cart        context["guest_address_form"] = address_form        context["shipping_methods"] = shipping_methods    else:        if request.GET.get("login"):            return redirect("login")        context["checkout_options"] = True    return render(request, template, context)# After cart checkout confirm aditional infodef confirm_info(request):    context = dict()    discount = 0    discount_name = None    if request.POST.get("address_line_1") is False:        messages.WARNING(request, "Address missing")        return redirect("checkout")    if request.POST.get("coupon_code"):        coupons = Coupon.objects.filter(active=True)        if coupons.filter(code=request.POST.get("coupon_code")).exists():            c = coupons.get(code=request.POST.get("coupon_code"))            discount = c.discount            discount_name = c.name        else:            messages.warning(request, message="Coupon code invalid")            return redirect("checkout")    if request.POST.get:        template = "confirm_order_details.html"        shipping_method = ShippingMethod.objects.get(clean_name=request.POST.get("shipping_method"))        cart = Cart(request)        final_total = cart.total_price        if discount:            final_total = final_total - discount        if request.POST.get("store_credit"):            final_total = cart.total_price - Decimal(request.POST.get("store_credit"))        state_tax = StateInfo.objects.get(abbreviation=request.POST.get("state")).state_tax_rate        tax = sum([(round(Decimal(i["price"]) * state_tax, 2)) * i["quantity"] for i in cart])        # tax = round(sum([Decimal(i["total"]) * state_tax for i in cart]), 2)        final_total = round((final_total + tax) + shipping_method.cost, 2)        data = {            "name": request.POST.get("name"),            "email": request.POST.get("email"),            "address_line_1": request.POST.get("address_line_1"),            "address_line_2": request.POST.get("address_line_2"),            "city": request.POST.get("city"),            "state": request.POST.get("state"),            "zip_code": request.POST.get("zip_code"),            "shipping_method": shipping_method.full_name,            "shipping_charged": shipping_method.cost,            "payment_method": request.POST.get("payment_method"),            "store_credit": request.POST.get("store_credit", 0),            "final_total": final_total,            "tax": tax,            "tax_percentage": state_tax,            "discount_amount": discount,            "discount_name": discount_name,        }        context["customer"] = data        context["cart"] = cart        return render(request, template, context)# Get main Cart objectdef get_cart(request):    remove_list = list()    cart = Cart(request)    for item in cart:        if item["quantity"] <= 0:            remove_list.append(item["product"])    if remove_list:        for item in remove_list:            cart.remove(item)    length = cart.cart_length    return render(request, 'cart.html', {'cart': cart, 'length': length, 'sub_total': cart.total_price})def home(request):    context = dict()    template_name = 'home.html'    daily_mtg = DailyMtgNews.objects.all().order_by("published_date")[0:6]    context['daily_mtg_articles'] = daily_mtg    home_page_objects = HomePageLayout.objects.get(name='Main Image')    context['main_slide'] = home_page_objects    hotlist = HotList.objects.all()    context['hotlist'] = hotlist    preorders = PreorderItem.objects.all()    context['preorders'] = preorders    sick_deals = SickDeal.objects.all()    context['sick_deals'] = sick_deals    announcement_title = Text.objects.get(clean_name='announcement_title')    context['announcement_title'] = announcement_title.text    announcement_text = Text.objects.get(clean_name='announcement_text')    context['announcement_text'] = announcement_text.text    company_address = CompanyAddress.objects.first()    context['address'] = company_address    map_description = Text.objects.get(clean_name='map_description')    context['map_description'] = map_description.text    return render(request, template_name=template_name, context=context)def home_base(request):    cart = Cart(request)    cart_length = cart.cart_length    response = render(None, 'home_base.html', {'cartLength': cart_length})    visits = int(request.COOKIES.get('visits', '0'))    if 'last_visit' in request.COOKIES:        last_visit = request.COOKIES['last_visit']        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")        if (datetime.now() - last_visit_time).days > 0:            response.set_cookie('visits', visits + 1)            response.set_cookie('last_visit', datetime.now())    else:        response.set_cookie('last_visit', datetime.now())    return responsedef order_confirmation(request):    events = []    template = 'order_complete.html'    context = {'events': events}    return render(request, template, context)def orders_view(request, product_info):    results = product_info.replace('+', ' ').replace('\n', '').split('\r')    quantity = {i[1:].lower(): {'q': i[0]} for i in results if i != ''}    results = [i[1:] for i in results if i != '']    products = object.objects.filter(name__in=results).order_by('name')    q = [quantity[i.name.lower()]['q'] for i in products]    order = zip(products, q)    return render(request, 'order_results.html', {'results': order})def payment(request):    name = request.POST.get('name')    email = request.POST.get('email')    cart = Cart(request)    total = cart.total_price    template = 'payment.html'    context = {        'total': total,        'name': name,        'email': email,    }    return render(request, template, context)def preorders(request):    context = dict()    template_name = 'preorders.html'    preorders = [i.expansion for i in PreorderItem.objects.all()]    if request.GET.get('q'):        expansion = request.GET.get('q')        preorder_products = MTG.objects.filter(expansion=expansion)        context['current'] = expansion    else:        preorder_products = MTG.objects.filter(expansion=preorders[0].group_name)        context['current'] = preorders[0].group_name    pages = pagination(request, data=preorder_products, num=10)    context['items'] = pages[0]    context['page_range'] = pages[1]    context['expansions'] = preorders    context['release_date'] = preorders[0].release_date    return render(request, template_name=template_name, context=context)def product_detail(request, product_id):    product = MTG.objects.filter(product_id=product_id)    # versions = object.objects.filter(name=products)    return render(request, 'product_detail.html', {'product': product})def query_expansion(request):    expansion = request.GET.get("expansion")    if expansion:        context = dict()        template = "singles_by_expansion.html"        results = MTG.objects.filter(expansion=expansion).exclude(layout="Sealed")        pages = pagination(request, results, 10)        context["items"] = pages[0]        context["page_range"] = pages[1]        return render(request, template_name=template, context=context)    else:        return redirect("home")def query_sealed_product(request):    context = dict()    template_name = "sealed_product.html"    results = MTG.objects.filter(layout="sealed")    pages = pagination(request, results, 10)    context["items"] = pages[0]    context["page_range"] = pages[1]    return render(request, template_name=template_name, context=context)def query_supplies(request):    context = dict()    template_name = "supplies.html"    supply_form = SuppliesAdvancedQueryForm()    if request.method == "GET":        search_query = request.GET.get("query")        with transaction.atomic():            def query(q):                if q == "all":                    results = MTG.objects.filter(layout='supplies')                else:                    item_type_options = ["Card Sleeves", "Deckboxes", ]                    if q in item_type_options:                        results = MTG.objects.filter(card_type=q)                        # filters = list(set(results.order_by('expansion').values_list("expansion", flat=True)))                    else:                        results = MTG.objects.filter(expansion=q)                return results        supplies = query(search_query)        pages = pagination(request, supplies, 10)        context["items"] = pages[0]        context["page_range"] = pages[1]    context["supply_form"] = supply_form    return render(request, template_name=template_name, context=context)def restock(request):    if request.GET:        user = request.user        if user.is_authenticated is True:            product_id = request.GET.get("product_id")            name = request.GET.get("name")            expansion = request.GET.get("expansion")            card = MTG.objects.get(product_id=product_id)            customer = Customer.objects.get(email=user.email)            normal = False            foil = False            clean = False            played = False            heavily_played = False            if request.GET.get("normal"):                normal = True            if request.GET.get("foil"):                foil = True            if request.GET.get("clean"):                clean = True            if request.GET.get("played"):                played = True            if request.GET.get("heavily_played"):                heavily_played = True            restock_notice, created = CustomerRestockNotice.objects.get_or_create(                email=user.email,                product_id=product_id,            )            restock_notice.name = name            restock_notice.expansion = expansion            restock_notice.normal = normal            restock_notice.foil = foil            restock_notice.clean = clean            restock_notice.played = played            restock_notice.heavily_played = heavily_played            restock_notice.save()            card.restock_notice.add(restock_notice)            customer.restock_list.add(restock_notice)            identifier = f"restock-button-{product_id}"            message = "Item added to Restock Notice list"            return JsonResponse({"success": "true", "id": identifier, "message": message})        else:            return redirect("login")    else:        return JsonResponse({"success": "false"})def remove_from_cart(request, product_id):    cart = Cart(request)    cart.remove(product_id)    return redirect('cart')def search(request):    template = 'search_result.html'    context = dict()    query = request.GET.get('q')    error = ''    def handle_query(request_variable, filtering, cards_per_page=10, check_stock=False):        query = request.GET.get(request_variable)        if query:            with transaction.atomic():                results = MTG.objects.filter(name=query).order_by(filtering)                error = ""                if not results:                    results = MTG.objects.filter(name__icontains=query).order_by(filtering)                    error = ""                    if not results:                        error = "empty query"        else:            error = "error"            results = list()        if check_stock:            results = results.filter(                Q(normal_clean_stock__gte=1) | Q(normal_played_stock__gte=1) | Q(normal_heavily_played_stock__gte=1) |                Q(foil_clean_stock__gte=1) | Q(foil_played_stock__gte=1) | Q(foil_heavily_played_stock__gte=1)            )        return results, error, cards_per_page, query    form = AdvancedSearchForm(request.GET)    if request.GET.get("advanced-search-form"):        if form.is_valid():            name_query = form.cleaned_data["name_query"]            name = form.cleaned_data["name"]            expansion = form.cleaned_data["expansion"]            artist = form.cleaned_data["artist"]            oracle_text = form.cleaned_data["oracle_text"]            colors = form.cleaned_data["colors"]            color_identity = form.cleaned_data["color_identity"]            rarity = form.cleaned_data["rarity"]            card_type = form.cleaned_data["card_type"]            subtypes = form.cleaned_data["subtypes"]            power_start = form.cleaned_data["power_start"]            power_end = form.cleaned_data["power_end"]            toughness_start = form.cleaned_data["toughness_start"]            toughness_end = form.cleaned_data["toughness_end"]            cmc_start = form.cleaned_data["cmc_start"]            cmc_end = form.cleaned_data["cmc_end"]            query_list = list()            advanced_query = MTG.objects            if expansion:                expansions = expansion.split(",")[0:-1]                for exp in expansions:                    advanced_query = advanced_query.filter(expansion__icontains=exp.strip())                query_list.append({"col": "Subtypes", "value": subtypes})            if name:                if name_query == 'contains':                    advanced_query = advanced_query.filter(name__icontains=name)                    query_list.append({"col": "Name", "value": name})                elif name_query == 'equals':                    advanced_query = advanced_query.filter(name__iexact=name)                    query_list.append({"col": "Name", "value": name})                else:                    pass            if colors:                color_list = "".join(colors)                advanced_query = advanced_query.filter(colors=color_list)                query_list.append({"col": "Colors", "value": colors})            if color_identity:                color_identity = "".join(color_identity)                advanced_query = advanced_query.filter(color_identity=color_identity)                query_list.append({"col": "Color Identity", "value": color_identity})            if rarity:                advanced_query = advanced_query.filter(rarity__in=rarity)                query_list.append({"col": "Rarity", "value": rarity})            if card_type:                for ct in card_type:                    advanced_query = advanced_query.filter(card_type__icontains=ct)                query_list.append({"col": "Card Types", "value": card_type})            if subtypes:                subtypes = subtypes.split(",")[0:-1]                for subtype in subtypes:                    advanced_query = advanced_query.filter(subtypes__icontains=subtype.strip())                query_list.append({"col": "Subtypes", "value": subtypes})            if artist:                artist = artist.split(",")[0:-1]                for art_person in artist:                    advanced_query = advanced_query.filter(artist__icontains=art_person.strip())                query_list.append({"col": "Artist", "value": artist})            if power_start:                advanced_query = advanced_query.filter(power__range=(power_start, power_end))                query_list.append({"col": "Power", "value": f"{power_start} to {power_end}"})            if toughness_start:                advanced_query = advanced_query.filter(toughness__range=(toughness_start, toughness_end))                query_list.append({"col": "Toughness", "value": f"{toughness_start} to {toughness_end}"})            if cmc_start:                advanced_query = advanced_query.filter(converted_mana_cost__range=(cmc_start, cmc_end))                query_list.append({"col": "Converted Mana Cost", "value": f"{cmc_start} to {cmc_end}"})            if oracle_text:                queries = oracle_text.split(',')                for query in queries:                    advanced_query = advanced_query.filter(oracle_text__icontains=query.strip())                query_list.append({"col": "Oracle Text Contains", "value": queries})            context["advanced_query"] = query_list            form = AdvancedSearchForm()            results = advanced_query        else:            results = list()            error = "error"    elif request.GET.get('all'):        results, error, cards_per_page, query = handle_query("all", "name")    elif request.GET.get('in_stock'):        results, error, cards_per_page, query = handle_query("in_stock", "name", check_stock=True)    elif request.GET.get('sort_by_set_reverse'):        results, error, cards_per_page, query = handle_query("sort_by_set_reverse", "-expansion")    elif request.GET.get('sort_by_set'):        results, error, cards_per_page, query = handle_query("sort_by_set_reverse", "expansion")    elif request.GET.get('per_page_10'):        results, error, cards_per_page, query = handle_query("per_page_10", "name")    elif request.GET.get('per_page_20'):        results, error, cards_per_page, query = handle_query("per_page_20", "name", cards_per_page=20)    elif request.GET.get('per_page_50'):        results, error, cards_per_page, query = handle_query("per_page_50", "name", cards_per_page=50)    elif request.GET.get('preorder'):        query = request.GET.get('preorder')        cards_per_page = 10        results = MTG.objects.filter(expansion=query)    else:        cards_per_page = 10        form = AdvancedSearchForm()        with transaction.atomic():            if query:                results = MTG.objects.filter(name=query)                if not results:                    results = MTG.objects.filter(name__icontains=query)                    if not results:                        error = "empty query"            else:                error = "error"                results = list()    if results:        pages = pagination(request, results, cards_per_page)        context['items'] = pages[0]        context['page_range'] = pages[1]    else:        error = "empty query"    context['error'] = error    context['query'] = query    context['form'] = form    context['results_object'] = results    get_copy = request.GET.copy()    parameters = get_copy.pop('page', True) and get_copy.urlencode()    context['parameters'] = parameters    return render(request, template, context)def sick_deals(request):    context = dict()    template_name = 'sick_deals.html'    if request.GET:        results, error, cards_per_page = process_filter(request, page="sick_deals")    else:        results = MTG.objects.filter(sick_deal=True)        cards_per_page = 10    pages = pagination(request, data=results, num=cards_per_page)    context['items'] = pages[0]    context['page_range'] = pages[1]    return render(request, template_name=template_name, context=context)def sku_search(request):    template_name = 'sku_search_result.html'    context = dict()    query = request.GET.get('q')    with transaction.atomic():        results = MTGDatabase.objects.filter(name=query)        if not results:            results = MTGDatabase.objects.filter(name__icontains=query)    pages = pagination(request, data=results, num=10)    context["items"] = pages[0]    context["page_range"] = pages[1]    return render(request, template_name=template_name, context=context)def submit_order(request):    if request.POST.get("submit_order"):        cart = Cart(request)        store_credit = request.POST.get("store_credit") if not None else 0        discounts = request.POST.get("discount_amount") if not None else 0        # Create Paypal formatting to submit paypal order        cards_in_cart = [            {                "name": i["name"],                "description": f"{i['language']}<>{i['printing']}<>{i['condition']}",                "sku": i["product"],                "unit_amount": {                    "currency_code": "USD",                    "value": i["price"],                },                "tax": {                    "currency_code": "USD",                    "value": str(round(Decimal(i["price"]) * Decimal(request.POST.get("tax_percentage")), 2))                },                "quantity": i["quantity"],                "category": "PHYSICAL_GOODS",            }            for i in cart        ]        # Creates Paypal Order and return an order ID        order_number = paypal.create_order(            product_list=cards_in_cart,            grand_total=request.POST.get("final_total"),            subtotal=str(cart.total_price),            shipping_cost=request.POST.get("shipping_charged"),            shipping_discount=0,            tax=request.POST.get("tax"),            shipping_method=request.POST.get("shipping_method"),            shipping_name=request.POST.get("name"),            address_line_1=request.POST.get("address_line_1"),            address_line_2=request.POST.get("address_line_2"),            city=request.POST.get("city"),            state=request.POST.get("state"),            zip_code=request.POST.get("zip_code"),        )        if order_number:            # Add processing of order to celery que in order to avoid a timeout for large orders            # process_order.apply_async(que='low_priority', args=[request, cart, order_number, store_credit, discounts, ])            process_order(request, cart, order_number, store_credit, discounts)            cart.clear()            return redirect(f"https://www.sandbox.paypal.com/checkoutnow?token={order_number}")        else:            messages.WARNING(request, "There was an error processing your request. Please try again. If this issue continues, please contact us.")            return redirect("cart")    elif request.POST.get("edit_order"):        return redirect("cart")    else:        return redirect("cart")def update_cart(request, product_id):    cart = Cart(request)    if request.POST:        quantity = request.POST.get("quantity")        unit_price = request.POST.get("price")        cart.update(product_id, quantity, unit_price)    return redirect("cart")@staff_member_requireddef upload_cards(request):    context = dict()    template_name = "upload_cards.html"    if request.POST:        csv_file = request.FILES.get("file")        if csv_file:            try:                if not csv_file.name.endswith('.csv'):                    messages.warning(request, 'THIS IS NOT A CSV FILE')                data_set = csv_file.read().decode('UTF-8')                io_string = io.StringIO(data_set)                next(io_string)                upload_list = list()                def change_str_to_zero(value):                    if value == '':                        return 0                    else:                        return value                for column in csv.reader(io_string, delimiter=','):                    normal_clean_stock = column[3]                    normal_played_stock = column[4]                    normal_heavily_played_stock = column[5]                    foil_clean_stock = column[6]                    foil_played_stock = column[7]                    foil_heavily_played_stock = column[8]                    if normal_clean_stock != '' or normal_played_stock != '' or normal_heavily_played_stock or foil_clean_stock != '' \                            or foil_played_stock != '' or foil_heavily_played_stock != '':                        product_id = column[0]                        name = column[1]                        expansion = column[2]                        upload_list.append(                            MTGUpload(                                product_id=product_id,                                name=name,                                expansion=expansion,                                normal_clean_stock=change_str_to_zero(normal_clean_stock),                                normal_played_stock=change_str_to_zero(normal_played_stock),                                normal_heavily_played_stock=change_str_to_zero(normal_heavily_played_stock),                                foil_clean_stock=change_str_to_zero(foil_clean_stock),                                foil_played_stock=change_str_to_zero(foil_played_stock),                                foil_heavily_played_stock=change_str_to_zero(foil_heavily_played_stock),                                upload_status=False,                            )                        )                MTGUpload.objects.bulk_create(upload_list)                upload_mtg_cards.apply_async(que='low_priority')                messages.success(request, "Upload Successful!")                return redirect("https://www.tcgfirst.com/admin/engine/mtgupload")            except Exception as e:                messages.warning(request, f"error Uploading CSV file: {e}")        else:            messages.warning(request, "Error processing request")    return render(request, template_name=template_name, context=context)def wishlist(request):    if request.GET:        user = request.user        if user.is_authenticated is True:            product_id = request.GET.get('product_id')            name = request.GET.get('name')            expansion = request.GET.get('expansion')            image_url = request.GET.get('image_url')            customer = Customer.objects.get(email=user.email)            if product_id not in customer.wishlist:                customer.wishlist = customer.wishlist + f"{product_id}<>{name}<>{expansion}<>{image_url},"                customer.save()            identifier = f"wishlist-icon-{product_id}"            message = "Added to wishlist!"            return JsonResponse({"success": "true", "id": identifier, "message": message})    else:        return JsonResponse({"success": "false"})