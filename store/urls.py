from django.urls import path
from .views import store, search, cart, product_detail, product_detail_card


app_name = 'store'

urlpatterns = [
    path('', store , name='store'),
    path('cart/', cart, name='cart'),
    path('category/<slug:category_slug>/', store, name='product_by_category'),
    path('product_detail/<slug:category_slug>/<slug:product_slug>/<int:variant_id>/', product_detail, name='product_detail'),
    path('product_detail_card/<slug:category_slug>/<slug:product_slug>/<int:variant_id>/',product_detail_card, name='product_detail_card'),
    path('search/', search, name='search'),    
]
