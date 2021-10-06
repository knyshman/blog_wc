from django.urls import path
from .views import RegisterView, MyLoginView, MyLogoutView, RegisterDone

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    path('register_done/', RegisterDone.as_view(), name='register_done')

]