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
        start = date(2019, 1, 1)
        stop = date(2019, 1, 31)
        orders = Orders.objects.filter(order_date__range=(start, stop)).values_list('order_date', flat=True)
        orders = Counter(map(str, orders))
        data = {
            "orders": orders,
            "sales": 100,
            "customers": 10,
        }
        return Response(data)
