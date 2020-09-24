from django.views.generic import ListView, CreateView,DeleteView,UpdateView
from app.cobros.models import Contactos,Clientes,Productos
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.urls import reverse_lazy
from app.cobros.forms import formulario_cliente_productos
from django.shortcuts import render,redirect

from datetime import datetime

class listar_cliente_productos(ListView):
    model = Productos
    template_name = 'clientes/productos/listar.html'

    def get_queryset(self,**kwargs):
        return self.model.objects.filter(borrado=0,id_cliente_id=self.kwargs['pk'])

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre'] = 'carlos arteaga'
        context['plantilla'] = 'Productos'
        context['titulo'] = 'productos del clientes'
        context['titulo_lista'] = 'Información de los productos de: '
        context['nombre_cliente'] = self.kwargs['name']
        context['create_url'] = '/cobros/cliente/productos/crear/'+ str(self.kwargs['pk']) + '/' + str(self.kwargs['name']) + '/'
        context['url_salir'] = reverse_lazy('login:iniciar')
        context['boton_volver'] = 'si'
        context['quitar_footer'] = 'si'
        context['url_boton_volver'] = reverse_lazy('crm:listar_cliente')
        return context



class crear_cliente_productos(CreateView):
    model = Productos
    template_name = 'clientes/productos/crear.html'
    form_class = formulario_cliente_productos 
    #success_url = 'cliente/contactos/' + str(self.kwargs['pk']) +'/' 
    #reverse_lazy('crm:listar_cliente')

    def post(self, request,*args,**kwargs):
        data = {}
        form = self.form_class(request.POST)
        try:
            if form.is_valid():
                nuevo = Productos(
                    descripcion = form.cleaned_data.get('descripcion'),
                    numero_producto = form.cleaned_data.get('numero_producto'),
                    dias_mora = form.cleaned_data.get('dias_mora'),
                    capital = form.cleaned_data.get('capital'),
                    intereses = form.cleaned_data.get('intereses'),
                    saldo_total = form.cleaned_data.get('saldo_total'),
                    id_cliente_id = self.kwargs['pk'],
                    usuario_creacion = request.user.id,
                    estado = form.cleaned_data.get('estado')
                )
                nuevo.save()
                return redirect('/cobros/cliente/productos/' + str(self.kwargs['pk']) +'/' + str(self.kwargs['name']) + '/')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre'] = 'carlos arteaga'
        context['plantilla'] = 'Crear'
        context['btn_cancelar'] = '/cobros/cliente/productos/' + str(self.kwargs['pk']) +'/' + str(self.kwargs['name']) + '/'
        context['titulo_lista'] = 'Ingrese datos del nuevo registro del producto para: '
        context['nombre_cliente'] = self.kwargs['name']
        context['success_url'] = '/cobros/cliente/productos/' + str(self.kwargs['pk']) +'/' + str(self.kwargs['name']) + '/'
        context['boton_volver'] = 'si'
        context['quitar_footer'] = 'si'
        context['url_boton_volver'] = reverse_lazy('crm:listar_cliente')
        return context



class borrar_cliente_productos(DeleteView):
    model = Productos
    template_name = 'clientes/productos/borrar.html'
    #success_url = reverse_lazy('crm:listar_cliente')

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
        context['btn_cancelar'] = '/cobros/cliente/productos/' + str(self.kwargs['ant']) +'/' + str(self.kwargs['name']) + '/'
        context['list_url'] = '/cobros/cliente/productos/' + str(self.kwargs['ant']) +'/' + str(self.kwargs['name']) + '/'
        context['de'] = 'de'
        context['nombre_cliente'] =  self.kwargs['name']
        context['url_salir'] = reverse_lazy('login:iniciar')
        context['quitar_footer'] = 'si'
        context['titulo_lista'] = 'Eliminar producto'
        context['success_url'] = '/cobros/cliente/productos/' + str(self.kwargs['ant']) +'/' + str(self.kwargs['name']) + '/'
        return context



class actualizar_cliente_productos(UpdateView):
    model = Productos
    form_class = formulario_cliente_productos
    template_name = 'clientes/productos/crear.html'

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
            registro.numero_producto = request.POST['numero_producto']
            registro.dias_mora = request.POST['dias_mora']
            registro.capital = request.POST['capital']
            registro.intereses = request.POST['intereses']
            registro.saldo_total = request.POST['saldo_total']
            registro.id_cliente_id = self.kwargs['ant']
            registro.estado = request.POST['estado'] 
            registro.usuario_modificacion = request.user.id
            registro.fch_modificacion = datetime.now()
            registro.save()
            return redirect('/cobros/cliente/productos/' + str(self.kwargs['ant']) +'/' + str(self.kwargs['name']) + '/')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre'] = 'carlos arteaga'
        context['plantilla'] = 'Editar'
        context['nombre_cliente'] = self.kwargs['name']
        context['btn_cancelar'] = '/cobros/cliente/productos/' + str(self.kwargs['ant']) +'/' + str(self.kwargs['name']) + '/'
        context['titulo_lista'] = 'Editar contacto de cliente'
        context['quitar_footer'] = 'si'
        context['success_url'] = '/cobros/cliente/productos/' + str(self.kwargs['ant']) +'/' + str(self.kwargs['name']) + '/'
        return context

