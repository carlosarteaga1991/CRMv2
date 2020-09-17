from django.urls import path
from app.cobros.views.Departamento.views import *
from app.cobros.views.Puestos.views import *
from app.cobros.views.empresas.views import *
from app.cobros.views.clientes.views import *
from app.cobros.views.clientes.contactos.views import *
from app.cobros.views.clientes.productos.views import *
from app.cobros.views.codigos.views import *
from app.cobros.views.motivos.views import *
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

    # URL para puestos
    path('puestos/',listar_puestos.as_view(), name='listar_puestos'),
    path('puestos/crear/',crear_puesto.as_view(), name='crear_puesto'),
    path('puestos/borrar/<int:pk>/',borrar_puesto.as_view(), name='borrar_puesto'),
    path('puestos/actualizar/<int:pk>/',actualizar_puesto.as_view(), name='actualizar_puesto'),

    # URL para empresas
    path('empresa/',listar_empresas.as_view(), name='listar_empresa'),
    path('empresa/crear/',crear_empresa.as_view(), name='crear_empresa'),
    path('empresa/borrar/<int:pk>/',borrar_empresa.as_view(), name='borrar_empresa'),
    path('empresa/actualizar/<int:pk>/',actualizar_empresa.as_view(), name='actualizar_empresa'),

    # URL para clientes
    path('cliente/',listar_cliente.as_view(), name='listar_cliente'),
    path('cliente/crear/',crear_cliente.as_view(), name='crear_cliente'),
    path('cliente/borrar/<int:pk>/',borrar_cliente.as_view(), name='borrar_cliente'),
    path('cliente/actualizar/<int:pk>/',actualizar_cliente.as_view(), name='actualizar_cliente'),

    # URL para clientes --> CONTACTOS
    path('cliente/contactos/<int:pk>/<name>/',listar_cliente_contactos.as_view(), name='listar_cliente_contactos'),
    path('cliente/contactos/crear/<int:pk>/<name>/',crear_cliente_contactos.as_view(), name='crear_cliente_contactos'),
    path('cliente/contactos/borrar/<int:pk>/<name>/<int:ant>/',borrar_cliente_contactos.as_view(), name='borrar_cliente_contactos'),
    path('cliente/contactos/actualizar/<int:pk>/<name>/<int:ant>/',actualizar_cliente_contactos.as_view(), name='actualizar_cliente_contactos'),

    # URL para clientes --> PRODUCTOS
    path('cliente/productos/<int:pk>/<name>/',listar_cliente_productos.as_view(), name='listar_cliente_productos'),
    path('cliente/productos/crear/<int:pk>/<name>/',crear_cliente_productos.as_view(), name='crear_cliente_productos'),
    path('cliente/productos/borrar/<int:pk>/<name>/<int:ant>/',borrar_cliente_productos.as_view(), name='borrar_cliente_productos'),
    path('cliente/productos/actualizar/<int:pk>/<name>/<int:ant>/',actualizar_cliente_productos.as_view(), name='actualizar_cliente_productos'),

    # URL para códigos
    path('codigos/',listar_codigos.as_view(), name='listar_codigos'),
    path('codigos/crear/',crear_codigos.as_view(), name='crear_codigo'),
    path('codigos/borrar/<int:pk>/',borrar_codigos.as_view(), name='borrar_codigo'),
    path('codigos/actualizar/<int:pk>/',actualizar_codigos.as_view(), name='actualizar_codigo'),

    # URL para motivos
    path('motivos/',listar_motivos.as_view(), name='listar_motivos'),
    path('motivos/crear/',crear_motivos.as_view(), name='crear_motivo'),
    path('motivos/borrar/<int:pk>/',borrar_motivos.as_view(), name='borrar_motivo'),
    path('motivos/actualizar/<int:pk>/',actualizar_motivos.as_view(), name='actualizar_motivo'),
]