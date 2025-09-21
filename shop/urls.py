from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from shop.api.home_views import HomeViewSet
from shop.api.categories_views import CategoriesViewSet
from shop.api.about_views import AboutViewSet
from shop.api.products_views import ProductsViewSet
from shop.api.auth_views import AuthViewSet
from shop.api.cart_views import CartViewSet
from shop.api.payments_views import CheckoutView
from shop.api.payments_webhooks import stripe_webhook
from shop.api.orders_views import OrdersViewSet


auth_login = AuthViewSet.as_view({'get': 'login', 'post': 'login'})
auth_register = AuthViewSet.as_view({'get': 'register', 'post': 'register'})
auth_logout = AuthViewSet.as_view({'get': 'logout'})

urlpatterns = [
    path('', HomeViewSet.as_view({'get': 'list'}), name='home'),
    path('categories/', CategoriesViewSet.as_view({'get': 'list'}), name='categories'),
    path('about/', AboutViewSet.as_view({'get': 'list'}), name='about'),

    path('categories/<int:pk>/', CategoriesViewSet.as_view({'get': 'retrieve'}), name='category-products'),
    path("product/<int:category_id>/<int:pk>/", ProductsViewSet.as_view({"get": "retrieve"}), name="product-details"),
    path('product/<int:category_id>/<int:pk>/add-to-cart/', ProductsViewSet.as_view({'post' : 'add_to_cart'}), name='add-to-cart'),

    path('auth/login/', auth_login, name='auth-login'),
    path('auth/register/', auth_register, name='auth-register'),
    path('auth/logout/', auth_logout, name='auth-logout'),

    path('cart/', CartViewSet.as_view({'get' : 'list'}), name='cart'),
    path('cart/<int:pk>/remove/', CartViewSet.as_view({'post' : 'remove'}), name='remove-from-cart'),

    path("cart/checkout/get/", CheckoutView.as_view(), name="checkout-get"),
    path("cart/checkout/post/", CheckoutView.as_view(), name="checkout-post"),
    path("stripe/webhook/", stripe_webhook, name="stripe-webhook"),
    path('order/success_payment/', OrdersViewSet.as_view({'get' : 'success_payment'}), name='success-payment')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)