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
from .models import Orders
from datetime import date
from .graph_functions import map_dates, orders_by_category, mtg_card_info


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

        ygo_orders = map_dates(dates, ygo)
        mtg_orders = map_dates(dates, mtg)
        pokemon_orders = map_dates(dates, pokemon)
        dbs_orders = map_dates(dates, dbs)
        fow_orders = map_dates(dates, fow)
        funko_orders = map_dates(dates, funko)
        card_sleeves_orders = map_dates(dates, card_sleeves)
        supplies_orders = map_dates(dates, supplies)

        number_of_days = len(dates)
        average_orders_perday = int(10000 / number_of_days)
        mtg_orders_total = mtg_orders[1]
        mtg_average_orders = int(mtg_orders_total / number_of_days)

        ygo_count = ygo_orders[1]
        pokemon_count = pokemon_orders[1]
        dbs_count = dbs_orders[1]
        fow_count = fow_orders[1]
        funko_count = funko_orders[1]
        sleeves_count = card_sleeves_orders[1]
        supplies_count = supplies_orders[1]

        non_foil_english_count = sum(card_info['non_foil_english'])
        foil_english_count = sum(card_info['foil_english'])
        foil_foreign_count = sum(card_info['foil_foreign'])
        non_foil_foreign_count = sum(card_info['non_foil_foreign'])
        boxes_count = sum(card_info['boxes'])

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

        }

        return Response(data)
