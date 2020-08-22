from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from contact import views as contact_views
from engine import views as home_views
from buylist import views as buylist_views
from customer import views as customer_views
from users import views as user_views


urlpatterns = [
    # path('profile/update', user_views.login_required, name='update'),
    path('captcha/', include('captcha.urls')),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('user/', include('users.urls')),
    path('at/', include('admin_tools.urls')),
    path('sms/', include('sms.urls')),
    path('mail/', include('mail.urls')),
    path('layout/', include('layout.urls')),
    path('admin/', admin.site.urls),
    path('activate/<str:uidb64>/<str:token>', user_views.activate, name='activate'),
    path('', home_views.home_base, name='base'),
    path('home/', home_views.home, name='home'),
    path('singles/', home_views.query_expansion, name='expansions'),
    path('upload/admin', home_views.upload_cards, name='upload_cards'),
    path('sealed/', home_views.query_sealed_product, name='sealed'),
    path('supplies/', home_views.query_supplies, name='supplies'),
    path('checkout/confirm-details', home_views.confirm_info, name='confirm_order_details'),
    path('orders/', include('orders.urls')),
    path('api/card-info', home_views.CardDatabase.as_view(), name='card_info'),
    path('payment/', home_views.payment, name='payment'),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', user_views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('reset-password/', user_views.reset_password, name="reset_password"),
    path('make-password-change/', user_views.make_password_change, name="make_password_change"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', user_views.reset_password_change_form, name="password_reset_confirm"),
    path('password-reset-complete', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
        name='password_reset_complete'),
    path('contact-us/', contact_views.contact, name='contact'),
    path('ip/', customer_views.get_ip, name='ip'),
    path('buylist/', buylist_views.buylist_home, name='buylist'),
    path('buylist/buylist-page/', buylist_views.buylist_page, name='buylist_page'),
    path('privacy-policy/', contact_views.policy, name='policy'),
    path('accounts/', include('allauth.account.urls')),
    path('facebook_bot/', include('facebook_bot.urls')),
    path('results/', home_views.search, name='search'),
    path('sku-results/', home_views.sku_search, name='sku_search'),
    path('results/wishlist', home_views.wishlist, name='wishlist'),
    path('results/restock', home_views.restock, name='restock_notice'),
    path('buylist/results/', buylist_views.search, name='search_buylist'),
    # path('order_view/<product_info>', home_views.orders_view, name='orders'),
    # path('search-result/', home_views.search_result, name='search-result'),
    path('cart/', home_views.get_cart, name='cart'),
    path('buylist/cart/', buylist_views.get_cart, name='buylist_cart'),
    path('checkout/', home_views.checkout, name='checkout'),
    path('buylist/checkout/', buylist_views.checkout,  name='buylist_checkout'),
    path('results/cart/add/<product_id>', home_views.add_to_cart, name='add_to_cart'),
    path('cart/add-buylist-item/<product_id>', buylist_views.add_to_cart, name='add_to_cart_buylist'),
    path('cart/update/<product_id>', home_views.update_cart, name='update_cart'),
    path('cart/remove/<product_id>', home_views.remove_from_cart, name='remove_from_cart'),
    path('cart/remove-buylist-item/<product_id>', buylist_views.remove_from_cart, name='remove_from_cart_buylist'),
    path('cart/clear/', home_views.clear, name='empty_cart'),
    path('cart/clear-buylist-item/', buylist_views.clear, name='empty_cart_buylist'),
    path('product/<product_id>', home_views.product_detail, name='product_detail'),
    path('submit-order', home_views.submit_order, name='submit_order'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT,)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)),)



