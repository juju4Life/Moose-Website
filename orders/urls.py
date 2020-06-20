
from django.urls import path
from orders import views


urlpatterns = [
    path('admin/<order_number>/', views.order_view, name="order"),
    path('admin/active/pull-sheet', views.pull_sheet, name="orders_pull_sheet"),
]

