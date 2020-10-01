from django.views.generic import ListView, CreateView,DeleteView,UpdateView
from app.cobros.models import Motivos
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.urls import reverse_lazy
from app.cobros.forms import formulario_motivos
from django.shortcuts import render,redirect

from datetime import datetime

class listar_motivos(ListView):
    model = Motivos
    template_name = 'motivos/listar.html'

    def get_queryset(self):
        return self.model.objects.filter(borrado=0)

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre'] = 'carlos arteaga'
        context['plantilla'] = 'Motivos'
        context['titulo'] = 'Motivos existentes'
        context['titulo_lista'] = 'Motivos existentes'
        context['create_url'] = reverse_lazy('crm:crear_motivo')
        context['url_salir'] = reverse_lazy('login:iniciar')
        context['quitar_footer'] = 'si'
        context['tipo'] = ''
        return context



class crear_motivos(CreateView):
    model = Motivos
    template_name = 'motivos/crear.html'
    form_class = formulario_motivos 
    success_url = reverse_lazy('crm:listar_motivos')

    def post(self, request,*args,**kwargs):
        data = {}
        form = self.form_class(request.POST)
        try:
            if form.is_valid():
                nuevo = Motivos(
                    descripcion = form.cleaned_data.get('descripcion'),
                    id_codigo = form.cleaned_data.get('id_codigo'),
                    usuario_creacion = request.user.id,
                    estado = form.cleaned_data.get('estado')
                )
                nuevo.save()
                return redirect('crm:listar_motivos')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre'] = 'carlos arteaga'
        context['plantilla'] = 'Crear'
        context['btn_cancelar'] = reverse_lazy('crm:listar_motivos')
        context['quitar_footer'] = 'si'
        context['titulo_lista'] = 'Ingrese datos del nuevo motivo'
        context['tipo'] = 'nuevo'
        return context



class borrar_motivos(DeleteView):
    model = Motivos
    template_name = 'motivos/borrar.html'
    success_url = reverse_lazy('crm:listar_motivos')

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
        context['btn_cancelar'] = reverse_lazy('crm:listar_motivos')
        context['list_url'] = reverse_lazy('crm:listar_motivos')
        context['quitar_footer'] = 'si'
        context['url_salir'] = reverse_lazy('login:iniciar')
        context['titulo_lista'] = 'Eliminar motivo'
        return context



class actualizar_motivos(UpdateView):
    model = Motivos
    form_class = formulario_motivos
    template_name = 'motivos/crear.html'
    success_url = reverse_lazy('crm:listar_motivos')

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
            registro.id_codigo_id = request.POST['id_codigo']
            registro.usuario_modificacion = request.user.id
            registro.fch_modificacion = datetime.now()
            registro.save()
            return redirect('crm:listar_motivos')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre'] = 'carlos arteaga'
        context['plantilla'] = 'Editar'
        context['quitar_footer'] = 'si'
        context['btn_cancelar'] = reverse_lazy('crm:listar_motivos')
        context['titulo_lista'] = 'Editar motivo'
        context['tipo'] = 'editar'
        return context

