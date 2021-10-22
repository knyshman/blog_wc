from django.contrib.auth.views import PasswordResetView
from django.urls import path
from .views import RegisterView, MyLoginView, MyLogoutView, SuccessActivationView, \
    UserActivationView, RegisterDone

urlpatterns = [

    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    path('activate/complete/', SuccessActivationView.as_view(), name='activation_done'),
    path('activate/<str:activation_key>/', UserActivationView.as_view(), name='django_registration_activate'),
    path('register/', RegisterView.as_view(), name='register'),
    path('register_done/', RegisterDone.as_view(), name='register_done'),

]

