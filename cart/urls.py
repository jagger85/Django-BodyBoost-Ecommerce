from django.urls import path
from .views import get_cart_totals, get_cart_quantity, get_cart_variant_quantity, add_variant, clear_variant, remove_variant, checkout, checkout_validation, get_cart_variant_subtotal


app_name = 'cart'

urlpatterns = [
    path('quantity/', get_cart_quantity, name='cart_quantity'),
    path('variant_quantity/<int:variant_id>/', get_cart_variant_quantity, name='cart_variant_quantity'),
    path('add_variant/<int:variant_id>/' , add_variant, name='add_variant'),
    path('remove_variant/<int:variant_id>/' , remove_variant, name='remove_variant'),
    path('clear_variant/<int:variant_id>/' , clear_variant, name='clear_variant'),
    path('get-variant-subtotal/<int:variant_id>/', get_cart_variant_subtotal, name='get_cart_variant_subtotal'),
    path('get_cart_totals/', get_cart_totals, name='get_cart_totals'),
    path('checkout/', checkout, name='checkout'),
    path('checkout-validation/', checkout_validation, name='checkout_validation'),
    
]