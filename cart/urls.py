from django.urls import path
from .views import CartView, add_to_cart, remove_from_cart, remove_all_itemcart_products


app_name = 'cart'

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('<int:product_id>/', CartView.as_view(), name='cart_product'),
    path('product/<int:product_id>/', CartView.as_view(), name='cart_product'),
    # Legacy URLs for non-HTMX requests
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('remove_product/<int:product_id>/', remove_all_itemcart_products, name='remove_product'),
]