from engine.tcgplayer_api import TcgPlayerApi


api = TcgPlayerApi("moose")


def update_tcg():
    total_items = api.get_store_inventory(offset=0)["totalItems"]
    excludes = ["Alpha Edition", "Beta Edition", "Unlimited Edition", ]
    offset = 0
    while offset < total_items:
        skus = dict()
        items = api.get_store_inventory(offset=offset)["results"]

        for item in items:
            if item["group"] not in excludes:
                for sku in item["skus"]:
                    sku_id = sku["skuId"]
                    language = sku["language"]["name"]
                    price = sku["price"]
                    if language == "English":
                        skus[sku_id] = price

        sku_ids = ','.join([str(i) for i in skus])
        prices = api.market_prices_by_sku(sku_ids)
        upload_list = list()
        for each in prices["results"]:
            sku = each["skuId"]
            low_price = each["lowestListingPrice"]
            market_price = each["marketPrice"]

            if low_price is not None and market_price is not None:
                upload_price = market_price
                if low_price > market_price:
                    upload_price = low_price

                if upload_price < .49:
                    upload_price = .49

                upload_list.append(
                    {
                        "skuId": sku,
                        "price": upload_price,
                    }
                )

        api.batch_update_price(payload=upload_list)
        offset += 100


