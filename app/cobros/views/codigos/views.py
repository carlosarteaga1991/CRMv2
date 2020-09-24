from django.views.generic import ListView, CreateView,DeleteView,UpdateView
from app.cobros.models import Codigos
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.urls import reverse_lazy
from app.cobros.forms import formulario_codigos
from django.shortcuts import render,redirect

from datetime import datetime

class listar_codigos(ListView):
    model = Codigos
    template_name = 'codigos/listar.html'

    def get_queryset(self):
        return self.model.objects.filter(borrado=0)

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre'] = 'carlos arteaga'
        context['plantilla'] = 'Códigos'
        context['titulo'] = 'Códigos existentes'
        context['titulo_lista'] = 'Códigos existentes'
        context['create_url'] = reverse_lazy('crm:crear_codigo')
        context['quitar_footer'] = 'si'
        context['url_salir'] = reverse_lazy('login:iniciar')
        context['tipo'] = ''
        return context



class crear_codigos(CreateView):
    model = Codigos
    template_name = 'codigos/crear.html'
    form_class = formulario_codigos 
    success_url = reverse_lazy('crm:listar_codigos')

    def post(self, request,*args,**kwargs):
        data = {}
        form = self.form_class(request.POST)
        try:
            if form.is_valid():
                nuevo = Codigos(
                    descripcion = form.cleaned_data.get('descripcion'),
                    usuario_creacion = request.user.id,
                    estado = form.cleaned_data.get('estado')
                )
                nuevo.save()
                return redirect('crm:listar_codigos')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre'] = 'carlos arteaga'
        context['plantilla'] = 'Crear'
        context['btn_cancelar'] = reverse_lazy('crm:listar_codigos')
        context['titulo_lista'] = 'Ingrese datos del nuevo código'
        context['quitar_footer'] = 'si'
        context['tipo'] = 'nuevo'
        return context



class borrar_codigos(DeleteView):
    model = Codigos
    template_name = 'codigos/borrar.html'
    success_url = reverse_lazy('crm:listar_codigos')

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
        context['btn_cancelar'] = reverse_lazy('crm:listar_codigos')
        context['list_url'] = reverse_lazy('crm:listar_codigos')
        context['url_salir'] = reverse_lazy('login:iniciar')
        context['quitar_footer'] = 'si'
        context['titulo_lista'] = 'Eliminar código'
        return context



class actualizar_codigos(UpdateView):
    model = Codigos
    form_class = formulario_codigos
    template_name = 'codigos/crear.html'
    success_url = reverse_lazy('crm:listar_codigos')

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request,*args,**kwargs):
        self.object = self.get_object()
        return super().dispatch(request,*args,**kwargs)

    def post(self, request,*args,**kwargs):
        data = {}
        try:
            registro = self.get_object()
            registro.descripcion = request.POST['descripcion']
            registro.estado = request.POST['estado']
            registro.usuario_modificacion = request.user.id
            registro.fch_modificacion = datetime.now()
            registro.save()
            return redirect('crm:listar_codigos')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre'] = 'carlos arteaga'
        context['plantilla'] = 'Editar'
        context['btn_cancelar'] = reverse_lazy('crm:listar_codigos')
        context['quitar_footer'] = 'si'
        context['titulo_lista'] = 'Editar código'
        context['tipo'] = 'editar'
        return context
