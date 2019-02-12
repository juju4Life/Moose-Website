from django.shortcuts import render
from matplotlib import pylab
from matplotlib import pyplot as plt
from pylab import *
import numpy as np
from django.http import HttpResponse
import PIL, PIL.Image
from io import BytesIO


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

