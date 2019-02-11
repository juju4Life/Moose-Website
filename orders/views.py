from django.shortcuts import render
from matplotlib import pylab, pyplot
from pylab import *
import numpy as np
from django.http import HttpResponse
import PIL, PIL.Image
from io import BytesIO


def graph(request):
    x = arange(0, 2*pi, 0.01)
    y = cos(x) ** 2

    plot(x, y)

    title('Graph')
    grid(True)

    xlabel('X Label')
    ylabel('Y Label')

    buffer = BytesIO()
    canvas = pylab.get_current_fig_manager().canvas
    canvas.draw()

    pilImage = PIL.Image.frombytes('RGB', canvas.get_width_height(), canvas.tostring_rgb())
    pilImage.save(buffer, 'PNG')
    pylab.close()
    return HttpResponse(buffer.getvalue(), 'image/png')

