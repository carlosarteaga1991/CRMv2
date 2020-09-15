
from django.urls import path,include
from app.login.views import *

app_name = 'login'

urlpatterns = [
    path('',login.as_view(), name='iniciar'),
    path('logout/',LogoutView.as_view(), name='salir'),#path('logout/',LogoutView.as_view(next_page='iniciar'), name='salir'),
]