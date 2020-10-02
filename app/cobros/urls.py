from django.urls import path
from app.cobros.views.Departamento.views import *
from app.cobros.views.Puestos.views import *
from app.cobros.views.empresas.views import *
from app.cobros.views.clientes.views import *
from app.cobros.views.clientes.contactos.views import *
from app.cobros.views.clientes.productos.views import *
from app.cobros.views.codigos.views import *
from app.cobros.views.motivos.views import *
from app.cobros.views.gestiones.views import *
from app.cobros.views.dashboard.views import *
from app.cobros.views.seguimiento_promesas.views import *
from app.cobros.views.seguimiento_visitas.views import *
from app.cobros.views.seguimiento_alertas.views import *
from app.cobros.views.promesas_del_dia.views import *
from app.cobros.views.alertas_del_dia.views import *


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

    # URL para gestiones --> CLIENTES, CONTACTOS, GESTIONES, PRODUCTOS
    path('gestion/<int:pk>/',listar_gestiones.as_view(), name='listar_gestiones'),

    # URL para seguimiento de PROMESAS
    path('seguimiento/promesas/',listar_seg_promesas.as_view(), name='listar_seg_promesas'),
    path('seguimiento/promesas/actualizar/<int:pk>/',actualizar_seg_promesas.as_view(), name='actualizar_seg_promesa'),

    # URL para seguimiento de VISITAS
    path('seguimiento/visitas/',listar_seg_visitas.as_view(), name='listar_seg_visita'),
    path('seguimiento/visitas/respuesta/<int:pk>/',respuesta_seg_visitas.as_view(), name='respuesta_seg_visita'),

    # URL para seguimiento de ALERTAS
    path('seguimiento/alertas/',listar_seg_alertas.as_view(), name='listar_seg_alertas'),
    path('seguimiento/alertas/editar/<int:pk>/',actualizar_seg_alertas.as_view(), name='actualizar_seg_alertas'),

    # URL para promesas del día
    path('promesas/hoy/',listar_promesas_hoy.as_view(), name='listar_promesas_hoy'),
    path('promesas/actualizar/<int:pk>/',actualizar_promesas_hoy.as_view(), name='actualizar_promesas_hoy'),

    # URL para alertas del d+ia
    path('alertas/hoy/',listar_alertas_hoy.as_view(), name='listar_alertas_hoy'),
    path('alertas/editar/<int:pk>/',actualizar_alertas_hoy.as_view(), name='actualizar_alertas_hoy'),
]