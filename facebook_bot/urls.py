from django.urls import path, include
from .views import botView


urlpatterns = [
    path('8c4e201a68cc0741436ac8617c81439512f88ffaa6deec565f/', botView.as_view())

]
