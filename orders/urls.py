
from django.urls import path
from orders import views


urlpatterns = [

    path('graph.png/', views.graph, name='graph'),

]

