from django.urls import path
from app.cobros.views.Departamento.views import *


app_name = 'crm'

urlpatterns = [
    path('home/',home, name='home'),
    path('departamento/',listview_departamento.as_view(), name='listar_departamento'),
    path('departamento/crear/',createview_departamento.as_view(), name='crear_departamento'),
    path('departamento/actualizar/<int:pk>/',updateview_departamento.as_view(), name='actualizar_departamento'),
    path('departamento/borrar/<int:pk>/',deleteview_departamento.as_view(), name='borrar_departamento'),
    
]