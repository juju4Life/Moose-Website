
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
if settings.DEBUG == True:
    import debug_toolbar

urlpatterns = [
    path(r'^__debug__/', include(debug_toolbar.urls)),
    path('sms/', include('sms.urls')),
    path('admin/', admin.site.urls),
    path('', home_views.home_base, name='base'),
    path('home/', home_views.home, name='home'),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('contact/', contact_views.contact, name='contact'),
    path('ip/', customer_views.get_ip, name='ip'),
    path('buylist/', buylist_views.buylist_home, name='buylist'),
    path('buylist/buylist-page/', buylist_views.buylist_page, name='buylist_page'),
    path('privacy-policy/', contact_views.policy, name='policy'),
    path('accounts/', include('allauth.account.urls')),
    path('facebook_bot/', include('facebook_bot.urls')),
    path('results/', home_views.search, name='search'),
    path('buylist/results/', buylist_views.search, name='search_buylist'),
    path('list_results/', home_views.search_list, name='search_list'),
    path('order_view/<product_info>', home_views.orders_view, name='orders'),
    path('search-result/', home_views.search_result, name='search-result'),
    path('cart/', home_views.get_cart, name='cart'),
    path('buylist/cart/', buylist_views.get_cart, name='buylist_cart'),
    path('checkout/', home_views.checkout, name='checkout'),
    path('buylist/checkout/', buylist_views.checkout, name='buylist_checkout'),
    path('cart/add/<product_id>', home_views.add_to_cart, name='add_to_cart'),
    path('cart/add-buylist-item/<product_id>', buylist_views.add_to_cart, name='add_to_cart_buylist'),
    path('cart/remove/<product_id>', home_views.remove_from_cart, name='remove_from_cart'),
    path('cart/remove-buylist-item/<product_id>', buylist_views.remove_from_cart, name='remove_from_cart_buylist'),
    path('cart/clear/', home_views.clear, name= 'empty_cart'),
    path('cart/clear-buylist-item/', buylist_views.clear, name= 'empty_cart_buylist'),
    path('product/<product_id>', home_views.product_detail, name='product_detail'),
    path('supplies/', home_views.supplies, name='supplies'),
    path('binders/', home_views.binders, name='binders'),
    path('sleeves/', home_views.sleeves, name='sleeves'),
    path('item/<global_id>', home_views.item, name='item'),
    path('booster-packs/', home_views.booster_packs, name='booster_packs'),
    path('deckboxes/', home_views.deckboxes, name='deckboxes'),
    path('playmats-tubes/', home_views.playmats_tubes, name='playmats_tubes'),
    path('snacks-drinks/', home_views.snacks_drinks, name='snacks_drinks'),
    path('preorders/', home_views.preorders, name='preorders'),
    path('supplies/<global_id>', home_views.category, name='supply_category'),
    path('expansions/<set_name>', home_views.expansion, name='expansion'),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT,)

