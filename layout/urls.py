from django.urls import path
from layout import views

urlpatterns = [
    path("hook", views.daily_mtg_hook, name="daily_mtg_hook"),
]









