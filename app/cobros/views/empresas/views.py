from django.views.generic import ListView, CreateView,DeleteView,UpdateView
from app.cobros.models import Empresas,Recordatorios,Promesas
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.urls import reverse_lazy
from app.cobros.forms import formulario_empresa
from django.shortcuts import render,redirect

from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from app.usuario.models import *

from app.usuario.permisos import asignar_permiso
from app.usuario.alertas import alertas

class listar_empresas(LoginRequiredMixin,ListView):
    model = Empresas
    template_name = 'Empresas/listar.html'

    def get_queryset(self):
        return self.model.objects.filter(borrado=0)

    @method_decorator(csrf_exempt)
    #@method_decorator(login_required)
    def dispatch(self, request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre'] = 'carlos arteaga'
        context['plantilla'] = 'Empresas'
        context['titulo'] = 'Empresas existentes'
        context['titulo_lista'] = 'Empresas existentes'
        context['create_url'] = reverse_lazy('crm:crear_empresa')
        context['quitar_footer'] = 'si'
        context['url_salir'] = reverse_lazy('login:iniciar')
        context['tipo'] = ''

        # INICIO VERIFICACIÓN DE PERMISOS
        context['permisos'] = asignar_permiso().metodo_permiso(7,'ver',int(self.request.user.id_rol_id),self.request.user.usuario_administrador)
        # FIN VERIFICACIÓN DE PERMISOS

        # INICIO PARA RECORDATORIOS HEADER 
        context['cont_alerta'] = alertas().recordatorios(self.request.user)
        # FIN PARA RECORDATORIOS HEADER

        # INICIO PARA PROMESAS HEADER
        context['cont_promesa'] = alertas().promesas(self.request.user)
        context['cont_total'] = alertas().promesas(self.request.user) + alertas().recordatorios(self.request.user)
        # FIN PARA PROMESAS HEADER

        return context



class crear_empresa(LoginRequiredMixin,CreateView):
    model = Empresas
    template_name = 'Empresas/crear.html'
    form_class = formulario_empresa 
    success_url = reverse_lazy('crm:listar_empresa')

    
    def post(self, request,*args,**kwargs):
        data = {}
        form = self.form_class(request.POST)
        try:
            if form.is_valid():
                nuevo = Empresas(
                    nombre_empresa = form.cleaned_data.get('nombre_empresa'),
                    descripcion = form.cleaned_data.get('descripcion'),
                    telefono = form.cleaned_data.get('telefono'),
                    nombre_contacto = form.cleaned_data.get('nombre_contacto'),
                    usuario_creacion = request.user.id,
                    estado = form.cleaned_data.get('estado')
                )
                nuevo.save()
                return redirect('crm:listar_empresa')
            else:
                return render(request, self.template_name, {'form':form, 'quitar_footer': 'si', 'titulo_lista': 'Ingrese datos de la nueva empresa','plantilla': 'Crear'})
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre'] = 'carlos arteaga'
        context['plantilla'] = 'Crear'
        context['btn_cancelar'] = reverse_lazy('crm:listar_empresa')
        context['titulo_lista'] = 'Ingrese datos de la nueva empresa'
        context['quitar_footer'] = 'si'
        context['tipo'] = 'nuevo'

        # INICIO VERIFICACIÓN DE PERMISOS
        context['permisos'] = asignar_permiso().metodo_permiso(7,'crear',int(self.request.user.id_rol_id),self.request.user.usuario_administrador)
        # FIN VERIFICACIÓN DE PERMISOS

        # INICIO PARA RECORDATORIOS HEADER 
        context['cont_alerta'] = alertas().recordatorios(self.request.user)
        # FIN PARA RECORDATORIOS HEADER

        # INICIO PARA PROMESAS HEADER
        context['cont_promesa'] = alertas().promesas(self.request.user)
        context['cont_total'] = alertas().promesas(self.request.user) + alertas().recordatorios(self.request.user)
        # FIN PARA PROMESAS HEADER

        return context

class borrar_empresa(LoginRequiredMixin,DeleteView):
    model = Empresas
    template_name = 'Empresas/borrar.html'
    success_url = reverse_lazy('crm:listar_empresa')

    @method_decorator(csrf_exempt)
    #@method_decorator(login_required)
    def dispatch(self, request,*args,**kwargs):
        self.object = self.get_object()
        return super().dispatch(request,*args,**kwargs)

    def post(self, request,*args,**kwargs):
        data = {}
        try:
            registro = self.get_object()
            registro.borrado = 1
            registro.usuario_modificacion = request.user.id
            registro.fch_modificacion = datetime.now()
            registro.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre'] = 'carlos arteaga'
        context['plantilla'] = 'Eliminar'
        context['btn_cancelar'] = reverse_lazy('crm:listar_empresa')
        context['list_url'] = reverse_lazy('crm:listar_empresa')
        context['quitar_footer'] = 'si'
        context['url_salir'] = reverse_lazy('login:iniciar')
        context['titulo_lista'] = 'Eliminar empresa'

        # INICIO VERIFICACIÓN DE PERMISOS
        context['permisos'] = asignar_permiso().metodo_permiso(7,'borrar',int(self.request.user.id_rol_id),self.request.user.usuario_administrador)
        # FIN VERIFICACIÓN DE PERMISOS

        # INICIO PARA RECORDATORIOS HEADER 
        context['cont_alerta'] = alertas().recordatorios(self.request.user)
        # FIN PARA RECORDATORIOS HEADER

        # INICIO PARA PROMESAS HEADER
        context['cont_promesa'] = alertas().promesas(self.request.user)
        context['cont_total'] = alertas().promesas(self.request.user) + alertas().recordatorios(self.request.user)
        # FIN PARA PROMESAS HEADER

        return context


class actualizar_empresa(LoginRequiredMixin,UpdateView):
    model = Empresas
    form_class = formulario_empresa
    template_name = 'Empresas/crear.html'
    success_url = reverse_lazy('crm:listar_empresa')

    @method_decorator(csrf_exempt)
    #@method_decorator(login_required)
    def dispatch(self, request,*args,**kwargs):
        self.object = self.get_object()
        return super().dispatch(request,*args,**kwargs)

    
    def post(self, request,*args,**kwargs):
        """
        data = {}
        data['nombre_empresa'] = request.POST['nombre_empresa']
        data['descripcion'] = request.POST['descripcion']
        data['telefono'] = request.POST['telefono']
        data['nombre_contacto'] = request.POST['nombre_contacto']
        data['estado'] = request.POST['estado']
        try:
            registro = self.get_object()
            registro.nombre_empresa = data['nombre_empresa']
            registro.descripcion = data['descripcion']
            registro.telefono = data['telefono']
            registro.nombre_contacto = data['nombre_contacto']
            registro.estado = data['estado'] 
            registro.usuario_modificacion = request.user.id
            registro.fch_modificacion = datetime.now()
            registro.save()
            return redirect('crm:listar_empresa')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
        """
        data = {}
        form = self.form_class(request.POST)
        data['nombre_empresa'] = request.POST['nombre_empresa']
        data['descripcion'] = request.POST['descripcion']
        data['telefono'] = request.POST['telefono']
        data['nombre_contacto'] = request.POST['nombre_contacto']
        data['estado'] = request.POST['estado']
        try:
            #if form.is_valid():
                registro = self.get_object()
                registro.nombre_empresa = data['nombre_empresa']
                registro.descripcion = data['descripcion']
                registro.telefono = data['telefono']
                registro.nombre_contacto = data['nombre_contacto']
                registro.estado = data['estado'] 
                registro.usuario_modificacion = request.user.id
                registro.fch_modificacion = datetime.now()
                try:
                    registro.save()
                    return redirect('crm:listar_empresa')
                except Exception as e:
                    return render(request, self.template_name, {'form':form, 'quitar_footer': 'si', 'titulo_lista': 'Editar empresa','plantilla': 'Editar'})
                
            #else:
                #return render(request, self.template_name, {'form':form, 'quitar_footer': 'si', 'titulo_lista': 'Editar departamento','plantilla': 'Editar'})
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre'] = 'carlos arteaga'
        context['plantilla'] = 'Editar'
        context['btn_cancelar'] = reverse_lazy('crm:listar_empresa')
        context['titulo_lista'] = 'Editar empresa'
        context['quitar_footer'] = 'si'
        context['tipo'] = 'editar'

        # INICIO VERIFICACIÓN DE PERMISOS
        context['permisos'] = asignar_permiso().metodo_permiso(7,'actualizar',int(self.request.user.id_rol_id),self.request.user.usuario_administrador)
        # FIN VERIFICACIÓN DE PERMISOS

        # INICIO PARA RECORDATORIOS HEADER 
        context['cont_alerta'] = alertas().recordatorios(self.request.user)
        # FIN PARA RECORDATORIOS HEADER

        # INICIO PARA PROMESAS HEADER
        context['cont_promesa'] = alertas().promesas(self.request.user)
        context['cont_total'] = alertas().promesas(self.request.user) + alertas().recordatorios(self.request.user)
        # FIN PARA PROMESAS HEADER

        return context
