from django.urls import path
from app.cobros.views import funcion1,funcion2

app_name = 'crm'

urlpatterns = [
    path('home/',funcion1, name='home'),
    path('dos/',funcion2, name='vista2'),
]