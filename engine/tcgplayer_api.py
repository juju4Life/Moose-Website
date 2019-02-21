from.tcg_credentials import Credentials


credentials = Credentials()
store_key = credentials.store_key
headers = Credentials.headers


class TcgPlayerApi(object):
    def __init__(self):
        self.credentials = Credentials()
        self.store_key = self.credentials.store_key
        self.headers = self.credentials.headers

    def card_info_by_sku(self, sku_id):
        return self.credentials.get_request('catalog/skus/{}'.format(sku_id))

    def get_card_info(self, product_id):
        return self.credentials.get_request('catalog/products/{}'.format(product_id))

    def search_inventory(self, product_id):
        return self.credentials.get_request('stores/{}/inventory/products/{}/quantity'.format(store_key, product_id))

    def get_prices(self, *product_id):
        if type(product_id[0][0]) == list:
            product_ids = ','.join(product_id[0][0])
        else:
            product_ids = product_id[0]
        return self.credentials.get_request('pricing/product/{}'.format(product_ids))

    def create_buylist_item(self, sku_id, price, _data=False, _json=False):
        json_params = {
            "skuId": sku_id,
            "price": price,
            "quantity": 20
        }
        self.credentials.put_request('stores/{}/buylist/skus/{}'.format(self.store_key, sku_id), _data, _json, json=json_params)

    def update_buylist_item_price(self, sku_id, price, _data=False, _json=False):
        data = price
        self.credentials.put_request("stores/{}/buylist/skus/{}/price".format(store_key, sku_id), _data, _json, data=data)

    def update_buylist_item_quantity(self, sku_id, quantity, _data=False, _json=False):
        data = quantity
        self.credentials.put_request("stores/{}/buylist/skus/{}/quantity".format(store_key, sku_id), _data, _json, data=data)

    def get_orders(self, order_status, limit, offset):
        params = {
            "orderStatusIds": order_status,
            "limit": limit,
            "offset": offset,
        }
        return self.credentials.get_request_with_params("stores/{}/orders".format(store_key), params=params)

    def get_order_details(self, order_numbers):
        return self.credentials.get_request(f"stores/{store_key}/orders/{','.join(order_numbers)}")

    def get_order_items(self, order_number):
        return self.credentials.get_request(f"stores/{store_key}/orders/{order_number}/items")

    def get_buylist_cards(self, limit, offset):
        params = {
            "limit": limit,
            "offset": offset
        }
        return self.credentials.get_request("stores/{}/buylist/skuprices".format(store_key), params=params)

    def get_set_data(self, group_id, limit=100, offset=0, _bool_=False):
        params = {
            "groupId": group_id,
            "limit": limit,
            "offset": offset,
            "getExtendedFields": _bool_,
        }
        return self.credentials.get_request("catalog/products".format(store_key), params=params)

    def update_sku_price(self, sku_id, price, _data=False, _json=False):
        json_params = {
            "skuId": sku_id,
            "price": price,
        }
        self.credentials.put_request('stores/{}/inventory/skus/{}/price'.format(self.store_key, sku_id), _data, _json, json=json_params)

    def get_tcg_public_buylist(self, sku):
        return self.credentials.get_request("pricing/buy/sku/{}".format(sku))

    def get_group_ids(self, offset, cat_id):
        params = {
            "offset": offset,
            "limit": 100,
        }
        return self.credentials.get_request(f'catalog/categories/{cat_id}/groups', params=params)

    def get_recent_orders(self, offset):
        params = {
            "offset": offset,
            "limit": 100,
            "sort": "OrderDate Desc"
        }
        return self.credentials.get_request(f'stores/{store_key}/orders', params=params)

    def get_inventory(self, category):
        return self.credentials.get_request(f'stores/{store_key}/categories/{category}/skus')

    def get_sku_quantity(self, sku):
        return self.credentials.get_request(f'stores/{store_key}/inventory/skus/{sku}/quantity')

    def upload(self, sku, price, quantity, _data=False, _json=True):
        params = {
            "price": price,
            "quantity": quantity,
        }
        return self.credentials.put_request(f'stores/{store_key}/inventory/skus/{sku}', json=params, _data=_data, _json=_json)

    def market_prices_by_sku(self, sku):
        return self.credentials.get_request(f'pricing/sku/{",".join(sku)}')







