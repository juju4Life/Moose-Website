from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.sms_response, name='sms'),
]