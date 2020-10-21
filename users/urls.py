from django.urls import path
from users import views


urlpatterns = [
    path("activation-email/", views.activation_email, name='activation_email'),
    path("remove/", views.remove_wishlist_item, name="remove_wishlist_item"),
    path('resend-activation-email/', views.resend_activation_email, name='resend_activation_email'),
    path("restock/", views.restock_notification_change, name="restock_edit"),
]

