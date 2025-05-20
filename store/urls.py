from django.urls import path
from .views import store, ProductDetail, search


app_name = 'store'

urlpatterns = [
    path('', store , name='store'),
    path('category/<slug:category_slug>/', store, name='product_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', ProductDetail.as_view(), name='product_detail'),
    path('search/', search, name='search')
    
]
