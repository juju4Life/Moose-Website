

from buylist import views
from django.urls import path


urlpatterns = [
    path("", views.buylist_page, name="buylist"),
    path("add/<product_id>/", views.add_to_cart, name="buylist_add_to_cart"),
    path("cart/", views.get_cart, name="buylist_cart"),
    path("checkout/", views.checkout, name="buylist_checkout"),
    path("clear/", views.clear, name="clear_buylist_cart"),
    path("confirm-info/", views.confirm_info, name="buylist_confirm_info"),
    path("remove/<product_id>/", views.remove_from_cart, name="remove_from_buylist_cart"),
    path("update/<product_id>/",  views.update_cart, name="update_buylist_cart"),
]


