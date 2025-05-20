from django.urls import path
from .views import CartView , get_cart_quantity


app_name = 'cart'

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('<int:product_id>/', CartView.as_view(), name='cart_product'),
    path('product/<int:product_id>/', CartView.as_view(), name='cart_product'),
    path('quantity/', get_cart_quantity, name='cart_quantity'),
]