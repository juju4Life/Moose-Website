from django.urls import path
from layout import views

urlpatterns = [
    path("about-us/", views.about_us, name="about_us"),
    path("hook/", views.daily_mtg_hook, name="daily_mtg_hook"),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path("terms-of-service/", views.terms_of_service, name="terms_of_service"),
]









