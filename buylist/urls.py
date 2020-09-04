

from buylist import views
from django.urls import path


urlpatterns = [
    path("", views.buylist_page, name="buylist"),
]


