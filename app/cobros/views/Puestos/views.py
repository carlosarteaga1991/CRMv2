from django.views.generic import ListView, CreateView,DeleteView,UpdateView
from app.cobros.models import Puestos,Departamentos
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.urls import reverse_lazy
from app.cobros.forms import formulario_puestos
from django.shortcuts import render,redirect

from datetime import datetime

class listar_puestos(ListView):
    model = Puestos
    template_name = 'Puestos/listar.html'

    def get_queryset(self):
        return self.model.objects.filter(borrado=0)

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre'] = 'carlos arteaga'
        context['plantilla'] = 'Puestos'
        context['titulo'] = 'Puestos existentes'
        context['quitar_footer'] = 'si'
        context['titulo_lista'] = 'Puestos existentes'
        context['create_url'] = reverse_lazy('crm:crear_puesto')
        context['url_salir'] = reverse_lazy('login:iniciar')
        context['tipo'] = ''
        return context

class crear_puesto(CreateView):
    model = Puestos
    template_name = 'Puestos/crear.html'
    form_class = formulario_puestos 
    success_url = reverse_lazy('crm:listar_puestos')

    def post(self, request,*args,**kwargs):
        data = {}
        form = self.form_class(request.POST)
        try:
            if form.is_valid():
                nuevo = Puestos(
                    nombre = form.cleaned_data.get('nombre'),
                    id_departamento_id = int(request.POST['id_departamento']),
                    usuario_creacion = request.user.id,
                    estado = form.cleaned_data.get('estado')
                )
                nuevo.save()
                return redirect('crm:listar_puestos')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre'] = 'carlos arteaga'
        context['plantilla'] = 'Crear'
        context['btn_cancelar'] = reverse_lazy('crm:listar_puestos')
        context['quitar_footer'] = 'si'
        context['titulo_lista'] = 'Ingrese datos del nuevo puesto'
        context['tipo'] = 'nuevo'
        context['select_puesto'] = 'mostrar'
        departamento = Departamentos.objects.filter(borrado=0,estado=1)
        context['departamento'] = departamento
        return context

class borrar_puesto(DeleteView):
    model = Puestos
    template_name = 'Puestos/borrar.html'
    success_url = reverse_lazy('crm:listar_puestos')

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
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
        context['btn_cancelar'] = reverse_lazy('crm:listar_puestos')
        context['list_url'] = reverse_lazy('crm:listar_puestos')
        context['quitar_footer'] = 'si'
        context['url_salir'] = reverse_lazy('login:iniciar')
        context['titulo_lista'] = 'Eliminar puesto'
        return context

class actualizar_puesto(UpdateView):
    model = Puestos
    form_class = formulario_puestos
    template_name = 'Puestos/crear.html'
    success_url = reverse_lazy('crm:listar_puestos')

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request,*args,**kwargs):
        self.object = self.get_object()
        return super().dispatch(request,*args,**kwargs)

    def post(self, request,*args,**kwargs):
        data = {}
        data['nombre'] = request.POST['nombre']
        data['estado'] = request.POST['estado']
        data['id_departamento'] = request.POST['id_departamento']
        try:
            registro = self.get_object()
            registro.id_departamento_id = data['id_departamento']
            registro.nombre = data['nombre']
            registro.estado = data['estado'] 
            registro.usuario_modificacion = request.user.id
            registro.fch_modificacion = datetime.now()
            registro.save()
            return redirect('crm:listar_puestos')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre'] = 'carlos arteaga'
        context['plantilla'] = 'Editar'
        context['btn_cancelar'] = reverse_lazy('crm:listar_puestos')
        context['titulo_lista'] = 'Editar puestos'
        context['quitar_footer'] = 'si' 
        context['tipo'] = 'editar'
        context['select_puesto'] = 'mostrar'
        puesto = Puestos.objects.filter(borrado=0, id_puesto = self.kwargs['pk'])
        z = 0
        for c in puesto:
            z = c.id_departamento_id
        context['seleccionar'] = z
        departamento = Departamentos.objects.filter(borrado=0,estado=1)
        context['departamento'] = departamento
        return context