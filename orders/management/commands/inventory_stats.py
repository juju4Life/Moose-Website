from django.core.management.base import BaseCommand
from engine.tcgplayer_api import TcgPlayerApi
from orders.models import InventoryAnalytics, Inventory, NewOrders
from engine.models import Upload
from datetime import date
import numpy as np

api = TcgPlayerApi()


class Command(BaseCommand):
    def handle(self, **options):

        # Function to generate total of items
        def get_total(obj):
            inventory_value = np.array(obj.values_list('price', flat=True))
            total_items_on_inventory = np.array(obj.values_list('quantity', flat=True))

            ranged_value = np.array(obj.filter(price__range=(2, 9999)).values_list('price', flat=True))
            ranged_quantity = np.array(obj.filter(price__range=(2, 9999)).values_list('quantity', flat=True))
            return {
                'sum_price_of_cards': sum(inventory_value * total_items_on_inventory),
                'total_quantity': sum(total_items_on_inventory),
                'sum_price_of_cards_2plus': sum(ranged_value * ranged_quantity),
                'total_quantity_cards_2plus': sum(ranged_quantity),
            }

        # Full online inventory
        inventory = Inventory.objects.filter(quantity__range=(1, 9999)).exclude(condition='Unopened')

        # Filter desired categories through inventory
        yugioh_singles = Inventory.objects.filter(category='Yugioh')
        pokemon_singles = Inventory.objects.filter(category='Pokemon')
        all_mtg_singles_inventory = inventory.filter(category='Magic')
        mtg_english_foils = inventory.filter(category='Magic').filter(language='English').filter(printing=True)
        mtg_foreign_foils = inventory.filter(category='Magic').exclude(language='English').filter(printing=True)
        mtg_foreign = inventory.filter(category='Magic').exclude(language='English').filter(printing=False)
        mtg_english = inventory.filter(category='Magic').filter(language='English').filter(printing=False)

        # -------------------------------

        save_all_mtg_singles_inventory = get_total(all_mtg_singles_inventory)
        save_ygo_singles = get_total(yugioh_singles)
        save_pokemon_singles = get_total(pokemon_singles)
        save_mtg_english_foils = get_total(mtg_english_foils)
        save_mtg_foreign_foils = get_total(mtg_foreign_foils)
        save_mtg_foreign = get_total(mtg_foreign)
        save_mtg_english = get_total(mtg_english)

        todays_uploaded_cards = Upload.objects.filter(upload_date=date.today())
        todays_orders = NewOrders.objects.filter(order_date=date.today())








