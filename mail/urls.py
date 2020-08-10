from django.urls import path
from mail import views


urlpatterns = [
    path("incoming/", views.incoming_mail_hook, name="incoming_mail"),
]

