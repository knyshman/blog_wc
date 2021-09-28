from django.urls import path
from .views import logout_view, registration_view, login_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', registration_view, name='register')

]