
from django.urls import path
from orders import views


urlpatterns = [
    path('admin/<order_number>/', views.order_view, name="order"),
    path('admin/active/pull-sheet', views.pull_sheet, name="orders_pull_sheet"),
    path('admin/active/packing-slips/<order_number>', views.packing_slips, name="packing_slips"),
]

