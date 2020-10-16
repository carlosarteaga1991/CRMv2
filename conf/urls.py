"""CRMv2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from app.homepage.views import indexview
from app.login.views import login

from django.conf import settings
from django.conf.urls.static import static

from app.usuario.views.usuarios.views import *
from app.usuario.views.roles.views import *
from app.usuario.views.permisos.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',indexview.as_view(), name='principal'),
    path('login/',include('app.login.urls'), name='inicio_sesion'),
    path('cobros/',include('app.cobros.urls')), # incluimos el app y el llamado a sus urls

    # URL para USUARIOS
    path('usuarios/',listar_usuarios.as_view(), name='listar_usuarios'),
    path('usuarios/crear/',crear_usuario.as_view(), name='crear_usuarios'),
    path('usuarios/editar/<int:pk>/',editar_usuario.as_view(), name='editar_usuarios'),
    path('usuarios/borrar/<int:pk>/',borrar_usuario.as_view(), name='borrar_usuarios'),

    # URL para ROLES - PERFILES
    path('perfiles/',listar_roles.as_view(), name='listar_roles'),
    path('perfiles/crear/',crear_roles.as_view(), name='crear_roles'),
    path('perfiles/editar/<int:pk>/',editar_roles.as_view(), name='editar_roles'),
    path('perfiles/borrar/<int:pk>/',borrar_roles.as_view(), name='borrar_roles'),

    # URL para PERMISOS
    path('permisos/',listar_permisos.as_view(), name='listar_permisos'),
    path('permisos/crear/',crear_permisos.as_view(), name='crear_permisos'),
    path('permisos/editar/<int:pk>/',editar_permisos.as_view(), name='editar_permisos'),
    path('permisos/borrar/<int:pk>/',borrar_permisos.as_view(), name='borrar_permisos'),

    # URL para PERFIL DE USUARIOS
    path('perfil_usuario/',editar_perfil_usuario.as_view(), name='editar_perfil_usuario'),

    # URL para CAMBIAR PASSWORD USUARIO
    path('cambiar_password/',cambiar_password_usuario.as_view(), name='cambiar_password'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
