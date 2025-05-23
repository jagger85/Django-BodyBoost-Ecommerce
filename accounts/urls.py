from django.urls import path
from .views import login, logout, register, activate, password_recovery, reset_password_validation, password_reset

app_name = 'auth'

urlpatterns = [
    path('login/', login, name='login' ),
    path('logout/', logout, name='logout' ),
    path('register/', register, name='register' ),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('password-recovery/', password_recovery, name= 'password_recovery'),
    path('password-reset/', password_reset, name= 'password_reset'),
    path('reset-password-validation/', reset_password_validation, name= 'reset_password_validation'),
]