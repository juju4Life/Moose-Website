from django.shortcuts import render
from collections import Counter
from matplotlib import pylab
from matplotlib import pyplot as plt
from pylab import *
import numpy as np
from django.http import HttpResponse
import PIL, PIL.Image
from io import BytesIO
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Orders, ScatterEvent
from datetime import date
from .graph_functions import map_dates, orders_by_category, mtg_card_info, scatter_plot, sales_data
from .models import InventoryAnalytics, NewOrders
from datetime import date, datetime, timedelta
from engine.models import Upload
import math

def graph(request):
    x = arange(0, 2*pi, 0.01)
    y = cos(x) ** 2

    plt.plot(x, y)

    title('Graph')
    grid(True)

    xlabel('X Label')
    ylabel('Y Label')

    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')

    buffer = BytesIO()
    canvas = pylab.get_current_fig_manager().canvas
    canvas.draw()

    pilImage = PIL.Image.frombytes('RGB', canvas.get_width_height(), canvas.tostring_rgb())
    pilImage.save(buffer, 'PNG')
    pylab.close()
    return HttpResponse(buffer.getvalue(), 'image/png')


def chart_home(request):
    template = 'charts.html'
    context = {}
    return render(request, template, context)


# Charts for Analyzing Inventory ----------------------------------------------------

class ChartDataInventory(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        start = datetime.today() - timedelta(days=30)
        stop = datetime.today() - timedelta(days=1)
        inventory = InventoryAnalytics.objects.filter(check_date__range=(start, stop))
        orders = NewOrders.objects.all()
        dates = [str(i.check_date)[0:10] for i in inventory]
        date_object = [datetime.strptime(i, '%Y-%m-%d') for i in dates]

        inventory_quantity = [i.inventory_quantity_over2 for i in inventory if str(i.check_date)[0:10] in dates]
        uploads = Upload.objects.filter(upload_date__in=date_object).filter(upload_price__range=(2, 9999))

        upload_dates = {i: 0 for i in dates}
        for upload in uploads:
            upload_dates[str(upload.upload_date)] += upload.upload_quantity

        upload_dates_values = np.array([i for i in upload_dates.values()])
        upload_spread = (upload_dates_values / np.array(inventory_quantity)) * 100
        x_y = [{'x': k, 'y': round(i, 2)} for i, k in zip(upload_spread, dates)]

        def create_spread(dates, inventory_obj, order_obj, upload_obj):
            date_starter = {i: 0 for i in dates}
            date_starter.update(upload_obj)

            num_orders = Counter(date_starter)

            num_orders.update(order_obj)
            orders = np.array([i for i in num_orders.values()])

            spread = np.round((orders / inventory_obj) * 100, 2)
            spread_average = round((sum([i for i in order_obj.values()]) / len(dates)), 2)

            return spread, spread_average

        mtg_foils = inventory.values_list('total_of_english_mtg_foils_quantity_over2', flat=True)

        # English Foils
        online_foils = np.array(inventory.values_list('total_of_english_mtg_foils_quantity_over2', flat=True))
        foils_in_orders = []
        for each in orders:
            if str(each.order_date) in dates and each.printing == 'Foil' and each.language == 'English' and each.price > 2:
                for _ in range(each.quantity):
                    foils_in_orders.append(str(each.order_date))
        foils_in_orders = Counter(foils_in_orders)

        foils_in_uploads = Counter([str(i.upload_date) for i in uploads if i.category == 'Magic' and i.printing == 'True' and i.language == 'English' and str(
            i.upload_date) in dates])

        # English Non-foil
        online_english = np.array(inventory.values_list('total_of_english_mtg_quantity_over2', flat=True))
        english_in_orders = []
        for each in orders:
            if str(each.order_date) in dates and each.printing == 'Normal' and each.language == 'English' and each.price > 2:
                for _ in range(each.quantity):
                    english_in_orders.append(str(each.order_date))
        english_in_orders = Counter(english_in_orders)
        english_in_uploads = Counter([str(i.upload_date) for i in uploads if i.category == 'Magic' and i.printing == 'False' and i.language == 'English' and
                                      str(
            i.upload_date) in dates])

        # Foreign Foils
        online_foreign_foils = np.array(inventory.values_list('total_of_foreign_mtg_foils_quantity_over2', flat=True))
        foreign_foils_in_orders = []
        for each in orders:
            if str(each.order_date) in dates and each.printing == 'Foil' and each.language != 'English' and each.price > 2:
                for _ in range(each.quantity):
                    foreign_foils_in_orders.append(str(each.order_date))
        foreign_foils_in_orders = Counter(foreign_foils_in_orders)
        foreign_foils_in_uploads = Counter([str(i.upload_date) for i in uploads if i.category == 'Magic' and i.printing == 'True' and i.language != 'English'
                                           and str(
            i.upload_date) in dates])

        # Foreign Non-foil
        online_foreign = np.array(inventory.values_list('total_of_foreign_mtg_quantity', flat=True))
        foreign_in_orders = []
        for each in orders:
            if str(each.order_date) in dates and each.printing == 'Normal' and each.language != 'English':
                for _ in range(each.quantity):
                    foreign_in_orders.append(str(each.order_date))
        foreign_in_orders = Counter(foreign_in_orders)
        foreign_in_uploads = Counter([str(i.upload_date) for i in uploads if i.category == 'Magic' and i.printing == 'False' and i.language != 'English'
                                            and str(
            i.upload_date) in dates])

        # Foreign Non-foil
        online_pokemon = np.array(inventory.values_list('total_of_pokemon_quantity', flat=True))
        pokemon_in_orders = []
        for each in orders:
            if str(each.order_date) in dates and each.category == 'Pokemon':
                for _ in range(each.quantity):
                    pokemon_in_orders.append(str(each.order_date))
        pokemon_in_orders = Counter(pokemon_in_orders)
        pokemon_in_uploads = Counter([str(i.upload_date) for i in uploads if i.category == 'Pokemon' and i.printing == 'False' and i.language != 'English'
                                      and str(
            i.upload_date) in dates])

        # Create spreads
        foils_spread = create_spread(dates, online_foils, foils_in_orders, foils_in_uploads)
        foreign_foils_spread = create_spread(dates, online_foreign_foils, foreign_foils_in_orders, foreign_foils_in_uploads)
        english_spread = create_spread(dates, online_english, english_in_orders, english_in_uploads)
        foreign_spread = create_spread(dates, online_foreign, foreign_in_orders, foreign_in_uploads)
        pokemon_spread = create_spread(dates, online_pokemon, pokemon_in_orders, pokemon_in_uploads)

        data = {
            'foils_sold': mtg_foils,
            'dates': dates,
            'foil_orders': foils_spread[0],
            'foil_orders_avg': foils_spread[1],
            'english_orders': english_spread[0],
            'english_orders_avg': english_spread[1],
            'foreign_foil_orders': foreign_foils_spread[0],
            'foreign_foil_orders_avg': foreign_foils_spread[1],
            'foreign_orders': foreign_spread[0],
            'foreign_orders_avg': foreign_spread[1],
            'pokemon_orders': pokemon_spread[0],
            'pokemon_orders_avg': pokemon_spread[1],
            'upload_points': x_y,
        }

        return Response(data)


# Charts for Analyzing Orders ------------------------------------------------------
class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        # start = date(2019, 1, 1)
        # stop = date(2019, 1, 31)

        orders = Orders.objects.all()
        sorted_orders = orders.order_by('-order_date')[0:10000]

        # Generate list of orders for sorted_orders query
        orders_10k = sorted_orders.values_list('order_date', flat=True)
        # Count how many times an order occurs on a specific date, turning each date object to str.
        counted = Counter(map(str, orders_10k))

        dates = [i for i in counted.keys()][::-1]
        orders_per_day = [i for i in counted.values()][::-1]

        card_info = mtg_card_info(dates, sorted_orders)

        # Category Specific orders
        ygo = orders_by_category('Yugioh', sorted_orders)
        mtg = orders_by_category('Magic the Gathering', sorted_orders)
        pokemon = orders_by_category('Pokemon', sorted_orders)
        dbs = orders_by_category('Dragon Ball Super CCG', sorted_orders)
        fow = orders_by_category('Force of Will', sorted_orders)
        funko = orders_by_category('Funko', sorted_orders)
        card_sleeves = orders_by_category('Card Sleeves', sorted_orders)
        supplies = orders_by_category('Supplies', sorted_orders)
        deck_boxes = orders_by_category('Deck Boxes', sorted_orders)

        ygo_orders = map_dates(dates, ygo)
        mtg_orders = map_dates(dates, mtg)
        pokemon_orders = map_dates(dates, pokemon)
        dbs_orders = map_dates(dates, dbs)
        fow_orders = map_dates(dates, fow)
        funko_orders = map_dates(dates, funko)
        card_sleeves_orders = map_dates(dates, card_sleeves)
        supplies_orders = map_dates(dates, supplies)
        deck_box_orders = map_dates(dates, deck_boxes)

        number_of_days = len(dates)
        average_orders_perday = round(10000 / number_of_days, 1)
        mtg_orders_total = mtg_orders[1]
        mtg_average_orders = round(mtg_orders_total / number_of_days, 1)

        ygo_count = ygo_orders[1]
        pokemon_count = pokemon_orders[1]
        dbs_count = dbs_orders[1]
        fow_count = fow_orders[1]
        funko_count = funko_orders[1]
        sleeves_count = card_sleeves_orders[1]
        supplies_count = supplies_orders[1]
        deck_box_count = deck_box_orders[1]

        non_foil_english_count = sum(card_info['non_foil_english'])
        foil_english_count = sum(card_info['foil_english'])
        foil_foreign_count = sum(card_info['foil_foreign'])
        non_foil_foreign_count = sum(card_info['non_foil_foreign'])
        boxes_count = sum(card_info['boxes'])
        max_num = max(mtg_orders[0])

        total_english_price = card_info['sum_english']
        total_foreign_price = card_info['sum_foreign']
        total_foreign_foil_price = card_info['sum_foreign_foil']
        total_english_foil_price = card_info['sum_english_foil']
        total_boxes_price = card_info['sum_boxes']
        total_other_price = card_info['sum_other']
        refunds = card_info['refunds']

        mtg_price = sales_data(sorted_orders, 'Magic the Gathering')
        ygo_price = sales_data(sorted_orders, 'Yugioh')
        pokemon_price = sales_data(sorted_orders, 'Pokemon')
        dbs_price = sales_data(sorted_orders, 'Dragon Ball Super CCG')
        fow_price = sales_data(sorted_orders, 'Force of Will')
        deckboxes_price = sales_data(sorted_orders, 'Deckboxes')
        card_sleeves_price = sales_data(sorted_orders, 'Card Sleeves')
        supplies_price = sales_data(sorted_orders, 'Supplies')
        funko_price = sales_data(sorted_orders, 'Funko')

        gross = round(sum(sorted_orders.values_list('product_value', flat=True)))
        sum_english = round((total_english_price / mtg_price) * 100, 2)
        sum_foreign = round((total_foreign_price / mtg_price) * 100, 2)
        sum_foreign_foil = round((total_foreign_foil_price / mtg_price) * 100, 2)
        sum_english_foil = round((total_english_foil_price / mtg_price) * 100, 2)
        sum_boxes = round((total_boxes_price / mtg_price) * 100, 2)
        sum_other = round((total_other_price / mtg_price) * 100, 2)

        sum_english_price = '$' + str(round(total_english_price, 2))
        sum_foreign_price = '$' + str(round(total_foreign_price, 2))
        sum_foreign_foil_price = '$' + str(round(total_foreign_foil_price, 2))
        sum_english_foil_price = '$' + str(round(total_english_foil_price, 2))
        sum_boxes_price = '$' + str(round(total_boxes_price, 2))
        sum_other_price = '$' + str(round(total_other_price, 2))

        sum_mtg = round((mtg_price / gross) * 100, 2)
        sum_ygo = round((ygo_price / gross) * 100, 2)
        sum_pokemon = round((pokemon_price / gross) * 100, 2)
        sum_dbs = round((dbs_price / gross) * 100, 2)
        sum_fow = round((fow_price / gross) * 100, 2)
        sum_deckboxes = round((deckboxes_price / gross) * 100, 2)
        sum_card_sleeves = round((card_sleeves_price / gross) * 100, 2)
        sum_supplies = round((supplies_price / gross) * 100, 2)
        sum_funko = round((funko_price / gross) * 100, 2)

        sum_mtg_price = '$' + str(round(mtg_price, 2))
        sum_ygo_price = '$' + str(round(ygo_price, 2))
        sum_pokemon_price = '$' + str(round(pokemon_price, 2))
        sum_dbs_price = '$' + str(round(dbs_price, 2))
        sum_fow_price = '$' + str(round(fow_price, 2))
        sum_deckboxes_price = '$' + str(round(deckboxes_price, 2))
        sum_card_sleeves_price = '$' + str(round(card_sleeves_price, 2))
        sum_supplies_price = '$' + str(round(supplies_price, 2))
        sum_funko_price = '$' + str(round(funko_price, 2))

        pie_chart_1 = [
            sum_mtg,
            sum_pokemon,
            sum_ygo,
            sum_dbs,
            sum_fow,
            sum_deckboxes,
            sum_card_sleeves,
            sum_supplies,
            sum_funko,
        ]

        pie_chart_2 = [
            sum_english,
            sum_english_foil,
            sum_foreign,
            sum_foreign_foil,
            sum_boxes,
            sum_other,
        ]

        release_events = scatter_plot(ScatterEvent.objects, 'release_events', max_num)
        ban_list_update = scatter_plot(ScatterEvent.objects, 'ban_list_update', max_num)
        tcgplayer_kickback = scatter_plot(ScatterEvent.objects, 'tcgplayer_kickback', max_num)
        special = scatter_plot(ScatterEvent.objects, 'special', max_num)

        data = {
            "labels": dates,
            "all_orders": orders_per_day,
            "ygo": ygo_orders[0],
            "mtg": mtg_orders[0],
            "pokemon": pokemon_orders[0],
            "dbs": dbs_orders[0],
            "fow": fow_orders[0],
            "funko": funko_orders[0],
            "card_sleeves": card_sleeves_orders[0],
            "supplies": supplies_orders[0],
            "deck_boxes": deck_box_orders[0],
            "non_foil_english": card_info['non_foil_english'],
            "foil_english": card_info['foil_english'],
            "foil_foreign": card_info['foil_foreign'],
            "non_foil_foreign": card_info['non_foil_foreign'],
            "boxes": card_info['boxes'],
            "average": average_orders_perday,
            "number_of_days": number_of_days,
            "mtg_average": mtg_average_orders,
            "mtg_count": mtg_orders_total,
            "ygo_count": ygo_count,
            "pokemon_count": pokemon_count,
            "dbs_count": dbs_count,
            "fow_count": fow_count,
            "funko_count": funko_count,
            "sleeves_count": sleeves_count,
            "supplies_count": supplies_count,
            "non_foil_foreign_count": non_foil_foreign_count,
            "foil_foreign_count": foil_foreign_count,
            "foil_english_count": foil_english_count,
            "non_foil_english_count": non_foil_english_count,
            "boxes_count": boxes_count,
            "deck_box_count": deck_box_count,
            "release_events": release_events,
            "ban_list_update": ban_list_update,
            "tcg_player_kickback": tcgplayer_kickback,
            "special": special,
            'pie_chart': pie_chart_1,
            'pie_chart_2': pie_chart_2,
            'sum_english_price': sum_english_price,
            'sum_foreign_price': sum_foreign_price,
            'sum_foreign_foil_price': sum_foreign_foil_price,
            'sum_english_foil_price': sum_english_foil_price,
            'sum_boxes_price': sum_boxes_price,
            'sum_mtg_price': sum_mtg_price,
            'sum_ygo_price': sum_ygo_price,
            'sum_pokemon_price': sum_pokemon_price,
            'sum_dbs_price': sum_dbs_price,
            'sum_fow_price': sum_fow_price,
            'sum_deckboxes_price': sum_deckboxes_price,
            'sum_card_sleeves_price': sum_card_sleeves_price,
            'sum_supplies_price': sum_supplies_price,
            'sum_funko_price': sum_funko_price,
            'sum_other_price': sum_other_price,
            'refunds': refunds,
            'gross': gross,

        }

        return Response(data)
