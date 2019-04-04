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
                # cart =
                pass
            else:
                cart = self.session[settings.CART_SESSION_KEY] = {}

        self.cart = cart

    def add(self, product, price, set_name, condition, language, total, quantity=1):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'price': str(price), 'set_name': set_name, 'condition': condition, 'language': language, 'quantity': 0, 'total': total}

        self.cart[product_id]['quantity'] = int(quantity)
        self.save()

        self.cart[product_id]['set_name'] = set_name
        self.save()

        self.cart[product_id]['condition'] = condition
        self.save()

        self.cart[product_id]['language'] = language
        self.save()

        self.cart[product_id]['total'] = str(total)
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_KEY] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def empty(self):
        for each in self.cart:
            del each
        self.save()

    def __iter__(self):
        product_ids = self.cart.keys()

        splitted = settings.PRODUCT_MODEL.split('.')
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
        #self.session.cart[settings.CART_SESSION_KEY] = {}
        self.session.modified = True

