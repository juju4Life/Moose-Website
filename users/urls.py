from django.urls import path
from users import views


urlpatterns = [
    path("remove/", views.remove_wishlist_item, name="remove_wishlist_item"),
]

