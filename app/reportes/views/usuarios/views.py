from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from app.cobros.models import Departamentos,Puestos,Recordatorios,Promesas
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, TemplateView
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from app.usuario.forms import form_usuarios,form_perfil_usuarios
from django.urls import reverse_lazy

from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from app.usuario.models import Usuario,Roles,Permisos
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from app.usuario.permisos import asignar_permiso
from app.usuario.alertas import alertas

class mostra_tipos_de_reportes(LoginRequiredMixin,TemplateView):
    template_name = 'reportes.html'

    def get_queryset(self):
        return self.model.objects.filter(borrado=0)

    @method_decorator(csrf_exempt)
    def dispatch(self, request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plantilla'] = 'Reportes'
        context['quitar_footer'] = 'si'
        context['titulo_lista'] = 'Tipos de reportes:'
        #context['create_url'] = reverse_lazy('crear_usuarios')
        context['url_salir'] = reverse_lazy('login:iniciar')
        departamento = Departamentos.objects.filter(borrado=0,estado=1)
        puesto = Puestos.objects.filter(borrado=0,estado=1)
        total = Usuario.objects.filter(borrado=0,estado=1).count
        context['departamento'] = departamento
        context['puesto'] = puesto
        context['total'] = total

        # INICIO VERIFICACIÓN DE PERMISOS
        context['permisos'] = asignar_permiso().metodo_permiso(3,'ver',int(self.request.user.id_rol_id),self.request.user.usuario_administrador)
        # FIN VERIFICACIÓN DE PERMISOS

        # INICIO PARA RECORDATORIOS HEADER
        context['cont_alerta'] = alertas().recordatorios(self.request.user)
        # FIN PARA RECORDATORIOS HEADER

        # INICIO PARA PROMESAS HEADER 
        context['cont_promesa'] = alertas().promesas(self.request.user)
        context['cont_total'] = alertas().promesas(self.request.user) + alertas().recordatorios(self.request.user)
        # FIN PARA PROMESAS HEADER

        return context