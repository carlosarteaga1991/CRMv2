from django.views.generic import ListView, CreateView,DeleteView,UpdateView
from app.cobros.models import Contactos,Clientes,Promesas,Recordatorios
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.urls import reverse_lazy
from app.cobros.forms import formulario_cliente_contactos
from django.shortcuts import render,redirect

from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from app.usuario.models import *

from app.usuario.permisos import asignar_permiso
from app.usuario.alertas import alertas

class listar_cliente_contactos(LoginRequiredMixin,ListView):
    model = Contactos
    template_name = 'clientes/contactos/listar.html'

    def get_queryset(self,**kwargs):
        return self.model.objects.filter(borrado=0,id_cliente_id=self.kwargs['pk'])

    @method_decorator(csrf_exempt)
    #@method_decorator(login_required)
    def dispatch(self, request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre'] = 'carlos arteaga'
        context['plantilla'] = 'Contactos'
        context['titulo'] = 'Contactos del clientes'
        context['titulo_lista'] = 'Información para contactar a: '
        context['nombre_cliente'] = self.kwargs['name']
        context['create_url'] = '/cobros/cliente/contactos/crear/'+ str(self.kwargs['pk']) + '/' + str(self.kwargs['name']) + '/'
        context['url_salir'] = reverse_lazy('login:iniciar')
        context['boton_volver'] = 'si'
        context['quitar_footer'] = 'si'
        context['url_boton_volver'] = reverse_lazy('crm:listar_cliente')

        # INICIO VERIFICACIÓN DE PERMISOS
        context['permisos'] = asignar_permiso().metodo_permiso(14,'ver',int(self.request.user.id_rol_id),self.request.user.usuario_administrador)
        # FIN VERIFICACIÓN DE PERMISOS

        # INICIO PARA RECORDATORIOS HEADER 
        context['cont_alerta'] = alertas().recordatorios(self.request.user)
        # FIN PARA RECORDATORIOS HEADER

        # INICIO PARA PROMESAS HEADER
        context['cont_promesa'] = alertas().promesas(self.request.user)
        context['cont_total'] = alertas().promesas(self.request.user) + alertas().recordatorios(self.request.user)
        # FIN PARA PROMESAS HEADER
        return context



class crear_cliente_contactos(LoginRequiredMixin,CreateView):
    model = Contactos
    template_name = 'clientes/contactos/crear.html'
    form_class = formulario_cliente_contactos 
    #success_url = 'cliente/contactos/' + str(self.kwargs['pk']) +'/' 
    #reverse_lazy('crm:listar_cliente')

    def post(self, request,*args,**kwargs):
        data = {}
        form = self.form_class(request.POST)
        try:
            if form.is_valid():
                nuevo = Contactos(
                    tipo_contacto = form.cleaned_data.get('tipo_contacto'),
                    descripcion = form.cleaned_data.get('descripcion'),
                    comentario = form.cleaned_data.get('comentario'),
                    id_cliente_id = self.kwargs['pk'],
                    usuario_creacion = request.user.id,
                    estado = form.cleaned_data.get('estado')
                )
                nuevo.save()#'crm:listar_cliente_contactos' + self.kwargs['pk'] +'/'
                return redirect('/cobros/cliente/contactos/' + str(self.kwargs['pk']) +'/' + str(self.kwargs['name']) + '/')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre'] = 'carlos arteaga'
        context['plantilla'] = 'Crear'
        context['btn_cancelar'] = '/cobros/cliente/contactos/' + str(self.kwargs['pk']) +'/' + str(self.kwargs['name']) + '/'
        context['titulo_lista'] = 'Ingrese datos del nuevo registro de contacto para: '
        context['nombre_cliente'] = self.kwargs['name']
        context['success_url'] = '/cobros/cliente/contactos/' + str(self.kwargs['pk']) +'/' + str(self.kwargs['name']) + '/'
        context['boton_volver'] = 'si'
        context['quitar_footer'] = 'si'
        context['url_boton_volver'] = reverse_lazy('crm:listar_cliente')

        # INICIO VERIFICACIÓN DE PERMISOS
        context['permisos'] = asignar_permiso().metodo_permiso(14,'crear',int(self.request.user.id_rol_id),self.request.user.usuario_administrador)
        # FIN VERIFICACIÓN DE PERMISOS

        # INICIO PARA RECORDATORIOS HEADER 
        context['cont_alerta'] = alertas().recordatorios(self.request.user)
        # FIN PARA RECORDATORIOS HEADER

        # INICIO PARA PROMESAS HEADER
        context['cont_promesa'] = alertas().promesas(self.request.user)
        context['cont_total'] = alertas().promesas(self.request.user) + alertas().recordatorios(self.request.user)
        # FIN PARA PROMESAS HEADER

        return context



class borrar_cliente_contactos(LoginRequiredMixin,DeleteView):
    model = Contactos
    template_name = 'clientes/contactos/borrar.html'
    #success_url = reverse_lazy('crm:listar_cliente')

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
        context['btn_cancelar'] = '/cobros/cliente/contactos/' + str(self.kwargs['ant']) +'/' + str(self.kwargs['name']) + '/'
        context['list_url'] = '/cobros/cliente/contactos/' + str(self.kwargs['ant']) +'/' + str(self.kwargs['name']) + '/'
        context['de'] = 'de'
        context['nombre_cliente'] = 'del cliente ' + self.kwargs['name']
        context['url_salir'] = reverse_lazy('login:iniciar')
        context['titulo_lista'] = 'Eliminar contacto'
        context['quitar_footer'] = 'si'
        context['success_url'] = '/cobros/cliente/contactos/' + str(self.kwargs['ant']) +'/' + str(self.kwargs['name']) + '/'

        # INICIO VERIFICACIÓN DE PERMISOS 
        context['permisos'] = asignar_permiso().metodo_permiso(14,'borrar',int(self.request.user.id_rol_id),self.request.user.usuario_administrador)
        # FIN VERIFICACIÓN DE PERMISOS

        # INICIO PARA RECORDATORIOS HEADER 
        context['cont_alerta'] = alertas().recordatorios(self.request.user)
        # FIN PARA RECORDATORIOS HEADER

        # INICIO PARA PROMESAS HEADER
        context['cont_promesa'] = alertas().promesas(self.request.user)
        context['cont_total'] = alertas().promesas(self.request.user) + alertas().recordatorios(self.request.user)
        # FIN PARA PROMESAS HEADER

        return context



class actualizar_cliente_contactos(LoginRequiredMixin,UpdateView):
    model = Contactos
    form_class = formulario_cliente_contactos
    template_name = 'clientes/contactos/crear.html'
    #success_url = reverse_lazy('crm:listar_cliente')

    @method_decorator(csrf_exempt)
    #@method_decorator(login_required)
    def dispatch(self, request,*args,**kwargs):
        self.object = self.get_object()
        return super().dispatch(request,*args,**kwargs)

    def post(self, request,*args,**kwargs):
        data = {}
        try:
            registro = self.get_object()
            registro.descripcion = request.POST['descripcion']
            registro.comentario = request.POST['comentario']
            registro.tipo_contacto = request.POST['tipo_contacto']
            registro.id_cliente_id = self.kwargs['ant']
            registro.estado = request.POST['estado'] 
            registro.usuario_modificacion = request.user.id
            registro.fch_modificacion = datetime.now()
            registro.save()
            return redirect('/cobros/cliente/contactos/' + str(self.kwargs['ant']) +'/' + str(self.kwargs['name']) + '/')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre'] = 'carlos arteaga'
        context['plantilla'] = 'Editar'
        context['nombre_cliente'] = self.kwargs['name']
        context['quitar_footer'] = 'si'
        context['btn_cancelar'] = '/cobros/cliente/contactos/' + str(self.kwargs['ant']) +'/' + str(self.kwargs['name']) + '/'
        context['titulo_lista'] = 'Editar contacto de cliente'
        context['success_url'] = '/cobros/cliente/contactos/' + str(self.kwargs['ant']) +'/' + str(self.kwargs['name']) + '/'

        # INICIO VERIFICACIÓN DE PERMISOS 
        context['permisos'] = asignar_permiso().metodo_permiso(14,'actualizar',int(self.request.user.id_rol_id),self.request.user.usuario_administrador)
        # FIN VERIFICACIÓN DE PERMISOS

        # INICIO PARA RECORDATORIOS HEADER 
        context['cont_alerta'] = alertas().recordatorios(self.request.user)
        # FIN PARA RECORDATORIOS HEADER

        # INICIO PARA PROMESAS HEADER
        context['cont_promesa'] = alertas().promesas(self.request.user)
        context['cont_total'] = alertas().promesas(self.request.user) + alertas().recordatorios(self.request.user)
        # FIN PARA PROMESAS HEADER

        return context

