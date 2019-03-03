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
            return (
                sum(inventory_value * total_items_on_inventory),
                sum(total_items_on_inventory),
                sum(ranged_value * ranged_quantity),
                sum(ranged_quantity),
            )


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
        other_singles = inventory.exclude(category='Magic').exclude(category='Yugioh').exclude(category='Pokemon').exclude(category='Magic the Gathering')

        # -------------------------------

        save_all_mtg_singles_inventory = get_total(all_mtg_singles_inventory)
        save_ygo_singles = get_total(yugioh_singles)
        save_pokemon_singles = get_total(pokemon_singles)
        save_mtg_english_foils = get_total(mtg_english_foils)
        save_mtg_foreign_foils = get_total(mtg_foreign_foils)
        save_mtg_foreign = get_total(mtg_foreign)
        save_mtg_english = get_total(mtg_english)
        save_others = get_total(other_singles)

        # todays_uploaded_cards = Upload.objects.filter(upload_date=date.today())
        # todays_orders = NewOrders.objects.filter(order_date=date.today())

        new_stats = InventoryAnalytics(

            inventory_total=save_all_mtg_singles_inventory[0],
            inventory_quantity=save_all_mtg_singles_inventory[1],
            inventory_total_over2=save_all_mtg_singles_inventory[2],
            inventory_quantity_over2=save_all_mtg_singles_inventory[3],

            total_of_english_mtg_foils=save_mtg_english_foils[0],
            total_of_english_mtg_foils_quantity=save_mtg_english_foils[1],
            total_of_english_mtg_foils_over2=save_mtg_english_foils[2],
            total_of_english_mtg_foils_quantity_over2=save_mtg_english_foils[3],

            total_of_foreign_mtg_foils=save_mtg_foreign_foils[0],
            total_of_foreign_mtg_foils_quantity=save_mtg_foreign_foils[1],
            total_of_foreign_mtg_foils_over2=save_mtg_foreign_foils[2],
            total_of_foreign_mtg_foils_quantity_over2=save_mtg_foreign_foils[3],

            total_of_foreign_mtg=save_mtg_foreign[0],
            total_of_foreign_mtg_quantity=save_mtg_foreign[1],
            total_of_foreign_mtg_over2=save_mtg_foreign[2],
            total_of_foreign_mtg_quantity_over2=save_mtg_foreign[3],

            total_of_english_mtg=save_mtg_english[0],
            total_of_english_mtg_quantity=save_mtg_english[1],
            total_of_english_mtg_over2=save_mtg_english[2],
            total_of_english_mtg_quantity_over2=save_mtg_english[3],

            total_of_yugioh=save_ygo_singles[0],
            total_of_yugioh_quantity=save_ygo_singles[1],
            total_of_yugioh_over2=save_ygo_singles[2],
            total_of_yugioh_quantity_over2=save_ygo_singles[3],

            total_of_pokemon=save_ygo_singles[0],
            total_of_pokemon_quantity=save_pokemon_singles[1],
            total_of_pokemon_over2=save_pokemon_singles[2],
            total_of_pokemon_quantity_over2=save_pokemon_singles[3],

            total_of_others=save_others[0],
            total_of_others_quantity=save_others[1],
            total_of_others_over2=save_others[2],
            total_of_others_quantity_over2=save_others[3],
        )

        new_stats.save()








