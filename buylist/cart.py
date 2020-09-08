from decimal import Decimal
from django.conf import settings
from django.apps import apps


class ItemAlreadyExists(Exception):
    pass


class ItemDoesNotExist(Exception):
    pass


class ModelDoesNotExist(Exception):
    pass


class KeyNotSet(Exception):
    pass


class Cart(object):

    def __init__(self, request):
        self.session = request.session

        if not hasattr(settings, 'BUYLIST_CART_SESSION_KEY'):
            raise KeyNotSet('Session key identifier is missing in settings')

        if not hasattr(settings, 'BUYLIST_MODEL'):
            raise KeyNotSet('Buying model is missing in settings')

        cart = self.session.get(settings.BUYLIST_CART_SESSION_KEY)

        if not cart:
            is_model_set = hasattr(settings, 'USE_CART_MODELS')
            if is_model_set and settings.USE_CART_MODELS:
                pass
            else:
                cart = self.session[settings.BUYLIST_CART_SESSION_KEY] = {}

        self.cart = cart

    def add(self, product, price, expansion, quantity=1):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'price': str(price), 'expansion': expansion, 'quantity': 0}

        self.cart[product_id]['quantity'] = int(quantity)
        self.cart[product_id]['expansion'] = expansion
        self.cart[product_id]['total'] = str(Decimal(price) * Decimal(quantity))
        self.save()

    def save(self):
        self.session[settings.BUYLIST_CART_SESSION_KEY] = self.cart
        self.session.modified = True

    def remove(self, product_id):
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def update(self, product_id, new_value, price, max_quantity=None):
        if product_id in self.cart:
            if max_quantity:
                self.cart[product_id]["max_quantity"] = max_quantity
            quantity = int(new_value)
            price = Decimal(price)
            self.cart[product_id]["quantity"] = quantity
            self.cart[product_id]["total"] = str(quantity * price)
            self.save()

    def empty(self):
        for each in self.cart:
            del each
        self.save()

    def __iter__(self):
        product_ids = self.cart.keys()

        splitted = settings.BUYLIST_MODEL.split('.')
        app_label = splitted[0]
        model_name = splitted[1]

        try:
            model = apps.get_model(app_label, model_name)
        except LookupError:
            message = 'Model {} not found in app  {}'
            raise ModelDoesNotExist(message.format(model_name, app_label))

        products = model.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    @property
    def total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    @property
    def cart_length(self):
        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        self.cart.clear()
        # self.session.cart[settings.CART_SESSION_KEY] = {}
        self.session.modified = True



