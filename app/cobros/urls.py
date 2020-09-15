from django.urls import path
from app.cobros.views.Departamento.views import *
from app.cobros.views.dashboard.views import *


app_name = 'crm'

urlpatterns = [
    # URL para departamento
    path('home/',home, name='home'),
    path('departamento/',listview_departamento.as_view(), name='listar_departamento'),
    path('departamento/crear/',createview_departamento.as_view(), name='crear_departamento'),
    path('departamento/actualizar/<int:pk>/',updateview_departamento.as_view(), name='actualizar_departamento'),
    path('departamento/borrar/<int:pk>/',deleteview_departamento.as_view(), name='borrar_departamento'),
    
    # URL para dashboard
    path('dashboard/',dashboard_vista.as_view(), name='dashboard'),
]