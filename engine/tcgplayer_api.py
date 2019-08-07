from.tcg_credentials import Credentials


credentials = Credentials()


class TcgPlayerApi:
    def __init__(self, store):
        self.credentials = Credentials()
        self.store_key = self.credentials.store_keys[store]

    def card_info_by_sku(self, sku_id, store):
        return self.credentials.get_request('catalog/skus/{}'.format(sku_id), store=store)

    def get_card_info(self, product_id, store):
        params = {
            'getExtendedFields': True,
        }
        return self.credentials.get_request('catalog/products/{}'.format(product_id), params=params, store=store)

    def search_inventory(self, product_id, store):
        return self.credentials.get_request('stores/{}/inventory/products/{}/quantity'.format(self.store_key, product_id), store=store)

    def get_market_price(self, product_id, store):
        return self.credentials.get_request(f'pricing/product/{product_id}', store=store)

    def create_buylist_item(self, sku_id, price, store, _data=False, _json=False):
        json_params = {
            "skuId": sku_id,
            "price": price,
            "quantity": 20
        }
        self.credentials.put_request('stores/{}/buylist/skus/{}'.format(self.store_key, sku_id), _data, _json, json=json_params, store=store)

    def update_buylist_item_price(self, sku_id, price, store, _data=False, _json=False):
        data = price
        self.credentials.put_request("stores/{}/buylist/skus/{}/price".format(self.store_key, sku_id), _data, _json, data=data, store=store)

    def update_buylist_item_quantity(self, sku_id, quantity, store, _data=False, _json=False):
        data = quantity
        self.credentials.put_request("stores/{}/buylist/skus/{}/quantity".format(self.store_key, sku_id), _data, _json, data=data)

    def get_orders(self, order_status, limit, offset):
        params = {
            "orderStatusIds": order_status,
            "limit": limit,
            "offset": offset,
        }
        return self.credentials.get_request_with_params("stores/{}/orders".format(self.store_key), params=params)

    def get_order_details(self, order_numbers):
        return self.credentials.get_request(f"stores/{self.store_key}/orders/{','.join(order_numbers)}")

    def get_order_items(self, order_number):
        params = {
            'limit': 100,
        }
        return self.credentials.get_request(f"stores/{self.store_key}/orders/{order_number}/items", params=params)

    def get_buylist_cards(self, limit, offset):
        params = {
            "limit": limit,
            "offset": offset
        }
        return self.credentials.get_request("stores/{}/buylist/skuprices".format(self.store_key), params=params)

    def get_set_data(self, group_id, limit=100, offset=0):
        params = {
            "groupId": group_id,
            "limit": limit,
            "offset": offset,
            "getExtendedFields": True,
        }
        return self.credentials.get_request("catalog/products".format(self.store_key), params=params)

    def update_sku_price(self, sku_id, price, store, _data=False, _json=False):
        json_params = {
            "skuId": sku_id,
            "price": price,
        }
        self.credentials.put_request('stores/{}/inventory/skus/{}/price'.format(self.self.store_key, sku_id), _data=_data, _json=_json, json=json_params,
                                     store=store)

    def get_tcg_public_buylist(self, sku):
        return self.credentials.get_request("pricing/buy/sku/{}".format(sku))

    def get_group_ids(self, offset, cat_id, store):
        params = {
            "offset": offset,
            "limit": 100,
        }
        return self.credentials.get_request(f'catalog/categories/{cat_id}/groups', params=params, store=store)

    def get_recent_orders(self, offset):
        params = {
            "offset": offset,
            "limit": 100,
            "sort": "OrderDate Desc"
        }
        return self.credentials.get_request(f'stores/{self.store_key}/orders', params=params)

    def get_inventory(self, category, store):
        return self.credentials.get_request(f'stores/{self.store_key}/categories/{category}/skus', store=store)

    def get_sku_quantity(self, sku, store):
        return self.credentials.get_request(f'stores/{self.store_key}/inventory/skus/{sku}/quantity', store=store)

    def upload(self, sku, price, quantity, store, _data=False, _json=True):
        params = {
            "price": price,
            "quantity": quantity,
        }
        return self.credentials.put_request(f'stores/{self.store_key}/inventory/skus/{sku}', json=params, _data=_data, _json=_json, store=store)

    def market_prices_by_sku(self, sku, store):
        return self.credentials.get_request(f'pricing/sku/{",".join(sku)}', store=store)

    def increment_sku_quantity(self, sku, quantity, store):
        data = {
            "quantity": quantity,
        }
        return self.credentials.post_request(f'stores/{self.store_key}/inventory/skus/{sku}/quantity', data=data, store=store)

    def get_group_id_info(self, group_id, store):
        return self.credentials.get_request(f"catalog/groups/{group_id}", store=store)

    def price_by_group_id(self, group_id, store):
        return self.credentials.get_request(f'pricing/group/{group_id}', store=store)

    def get_category_skus(self, category, store):

        # api call dict = {totalItems: 0, success: True, errors: [], results: []}
        # skuId // sellerId // productId // channel Id // productName // categoryId // categoryName // groupId // groupName // conditionId // conditionName //
        # rarityId // rarityName // rarityDbValue // languageId // languageName // printingId // printingName // currentPrice // marketPrice //
        # directLowPrice // lowPrice // lowestListing // shippingPrice // isCustom

        category_map = {
            "magic": 1,
            "pokemon": 2,
            "yugioh": 3,
        }

        return self.credentials.get_request(f"stores/{self.store_key}/categories/{category_map[category]}/skus", store=store)

    def get_product_sku_list(self, product_id, store):

        return self.credentials.get_request(f"catalog/products/{product_id}/skus", store=store)





