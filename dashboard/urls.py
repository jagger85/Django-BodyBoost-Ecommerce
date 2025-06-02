from .views import dashboard, settings, address_manager, address_form, add_address, delete_address
from django.urls import path

app_name = 'dashboard'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('settings/', settings, name='dashboard_settings'),
    path('address/', address_manager, name='dashboard_address'),
    path('address-form/', address_form, name='address_form'),
    path('add-address/', add_address, name='add_address'),
    path('delete-address/<int:address_id>/', delete_address, name='delete_address')
]