from django.urls import path
from .views import get_cart_totals, get_cart_quantity, get_cart_variant_quantity, add_variant, clear_variant, remove_variant 


app_name = 'cart'

urlpatterns = [
    path('quantity/', get_cart_quantity, name='cart_quantity'),
    path('variant_quantity/<int:variant_id>/', get_cart_variant_quantity, name='cart_variant_quantity'),
    path('add_variant/<int:variant_id>/' , add_variant, name='add_variant'),
    path('remove_variant/<int:variant_id>/' , remove_variant, name='remove_variant'),
    path('clear_variant/<int:variant_id>/' , clear_variant, name='clear_variant'),
    path('get_cart_totals/', get_cart_totals, name='get_cart_totals')
]