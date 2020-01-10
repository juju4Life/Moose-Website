
from django.urls import path
from orders import views


urlpatterns = [

    path('graph.png/', views.graph, name='graph'),
    path('charts/', views.chart_home, name='chart_home'),
    path('api/data/', views.ChartData.as_view(), name='chart'),
    path('api/data/inventory/', views.ChartDataInventory.as_view(), name='chart_inventory'),

]

