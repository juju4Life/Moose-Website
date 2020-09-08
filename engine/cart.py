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

        if not hasattr(settings, 'CART_SESSION_KEY'):
            raise KeyNotSet('Session key identifier is missing in settings')

        if not hasattr(settings, 'PRODUCT_MODEL'):
            raise KeyNotSet('Product model is missing in settings')

        cart = self.session.get(settings.CART_SESSION_KEY)

        if not cart:
            is_model_set = hasattr(settings, 'USE_CART_MODELS')
            if is_model_set and settings.USE_CART_MODELS:
                pass
            else:
                cart = self.session[settings.CART_SESSION_KEY] = {}

        self.cart = cart

    def add(self, product_id, name, expansion, condition, printing, price, language, total, max_quantity, quantity=1):
        product_id = str(product_id)

        if product_id not in self.cart:

            self.cart[product_id] = {
                'product': product_id,
                'name': name,
                'expansion': expansion,
                'condition': condition,
                'printing': printing,
                'price': str(price),
                'language': language,
                'total': total,
                "max_quantity": max_quantity,
                'quantity': 0,
            }

        self.cart[product_id]['quantity'] = int(quantity)
        self.cart[product_id]['total'] = str(total)
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_KEY] = self.cart
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
        # product_ids = self.cart.keys()
        splitted = settings.PRODUCT_MODEL.split('.')
        app_label = splitted[0]
        model_name = splitted[1]

        try:
            model = apps.get_model(app_label, model_name)
        except LookupError:
            message = 'Model {} not found in app  {}'
            raise ModelDoesNotExist(message.format(model_name, app_label))

        for item in self.cart.values():
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    @property
    def total_price(self):
        subtotal = Decimal(0)
        for item in self.cart.values():
            price = Decimal(item['price'])
            quantity = item['quantity']
            subtotal += (price * quantity)

        return subtotal

    @property
    def cart_length(self):
        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        self.cart.clear()
        # self.session.cart[settings.CART_SESSION_KEY] = {}
        self.session.modified = True

