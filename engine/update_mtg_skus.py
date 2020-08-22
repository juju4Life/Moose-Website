
from engine.models import MTGDatabase
from engine.tcgplayer_api import TcgPlayerApi
from engine.tcg_manifest import Manifest
from orders.models import GroupName

api = TcgPlayerApi("moose")
manifest = Manifest()


def update_skus(category_id=1):
    total_items = api.get_all_products_for_category(offset=0, category_id=category_id)["totalItems"]
    offset = 48300

    def append_skus(sku_data, product_id, name, expansion):
        if sku_data:
            if MTGDatabase.objects.filter(sku=sku_data["skuId"]).exists() is False:
                upload_list.append(
                    MTGDatabase(
                        name=name,
                        expansion=expansion,
                        sku=sku_data["skuId"],
                        product_id=product_id,
                        language=manifest.language(sku_data["languageId"]),
                        condition=manifest.moose_condition_map(sku_data["conditionId"]),
                        printing=manifest.printing(sku_data["printingId"]),
                    )
                )

    while offset < total_items:
        upload_list = list()
        products = api.get_all_products_for_category(offset=offset, category_id=category_id)["results"]

        for product in products:
            product_id = product["productId"]
            name = product["name"]
            try:
                expansion = GroupName.objects.get(group_id=product["groupId"]).group_name
            except Exception as e:
                print(e)

            sku_list = product["skus"]
            normal_clean = next((i for i in sku_list if i["languageId"] == 1 and i["conditionId"] == 2 and i["printingId"] == 1), None)
            normal_played = next((i for i in sku_list if i["languageId"] == 1 and i["conditionId"] == 3 and i["printingId"] == 1), None)
            normal_heavily_played = next((i for i in sku_list if i["languageId"] == 1 and i["conditionId"] == 4 and i["printingId"] == 1), None)
            foil_clean = next((i for i in sku_list if i["languageId"] == 1 and i["conditionId"] == 2 and i["printingId"] == 2), None)
            foil_played = next((i for i in sku_list if i["languageId"] == 1 and i["conditionId"] == 3 and i["printingId"] == 2), None)
            foil_heavily_played = next((i for i in sku_list if i["languageId"] == 1 and i["conditionId"] == 4 and i["printingId"] == 2), None)
            sealed = next((i for i in sku_list if i["conditionId"] == 6), None)

            append_skus(sku_data=normal_clean, product_id=product_id, name=name, expansion=expansion)
            append_skus(sku_data=normal_played, product_id=product_id, name=name, expansion=expansion)
            append_skus(sku_data=normal_heavily_played, product_id=product_id, name=name, expansion=expansion)
            append_skus(sku_data=foil_clean, product_id=product_id, name=name, expansion=expansion)
            append_skus(sku_data=foil_played, product_id=product_id, name=name, expansion=expansion)
            append_skus(sku_data=foil_heavily_played, product_id=product_id, name=name, expansion=expansion)
            append_skus(sku_data=sealed, product_id=product_id, name=name, expansion=expansion)

        MTGDatabase.objects.bulk_create(upload_list)
        offset += 100
        print(offset)










