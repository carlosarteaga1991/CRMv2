from django.views.generic import ListView, CreateView,DeleteView,UpdateView
from app.cobros.models import Clientes,Empresas,Promesas,Recordatorios
from app.usuario.models import Usuario
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.urls import reverse_lazy
from app.cobros.forms import formulario_cliente
from django.shortcuts import render,redirect

from datetime import datetime

class listar_cliente(ListView):
    model = Clientes
    template_name = 'clientes/listar.html'

    def get_queryset(self):
        return self.model.objects.filter(borrado=0)

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre'] = 'carlos arteaga'
        context['plantilla'] = 'Clientes'
        context['titulo'] = 'Clientes existentes'
        context['titulo_lista'] = 'Clientes existentes'
        context['create_url'] = reverse_lazy('crm:crear_cliente')
        context['url_salir'] = reverse_lazy('login:iniciar')
        context['quitar_footer'] = 'si'
        context['tipo'] = ''
        # INICIO PARA RECORDATORIOS HEADER
        now = datetime.now()
        cont_rcrio = 0
        if len(str(now.month)) == 1:
            mes = '0' + str(now.month)
        else:
            mes = str(now.month)
        fecha = str(now.year) + '-' + mes + '-' + str(now.day)
        recordatorios = Recordatorios.objects.filter(borrado=0,usuario_creacion=self.request.user,estatus_alerta='Pendiente',fch_recordatorio=fecha)
        for x in recordatorios:
            cont_rcrio += 1
        context['cont_alerta'] = cont_rcrio 
        # FIN PARA RECORDATORIOS HEADER

        # INICIO PARA PROMESAS HEADER
        cont_promesa = 0
        promesa = Promesas.objects.filter(borrado=0,id_usuario=self.request.user,estatus_promesa='Pendiente',fecha=fecha)
        for x in promesa:
            cont_promesa += 1
        context['cont_promesa'] = cont_promesa 
        context['cont_total'] = cont_promesa + cont_rcrio
        # FIN PARA PROMESAS HEADER
        return context



class crear_cliente(CreateView):
    model = Clientes
    template_name = 'clientes/crear.html'
    form_class = formulario_cliente 
    success_url = reverse_lazy('crm:listar_cliente')

    def post(self, request,*args,**kwargs):
        data = {}
        form = self.form_class(request.POST)
        try:
            if form.is_valid():
                nuevo = Clientes(
                    nombre = form.cleaned_data.get('nombre'),
                    id_empresa = form.cleaned_data.get('id_empresa'),
                    id_usuario = form.cleaned_data.get('id_usuario'),
                    tipo_id = form.cleaned_data.get('tipo_id'),
                    identidad = form.cleaned_data.get('identidad'),
                    fch_nacimiento = form.cleaned_data.get('fch_nacimiento'),
                    usuario_creacion = request.user.id,
                    estado = form.cleaned_data.get('estado')
                )
                nuevo.save()
                return redirect('crm:listar_cliente')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre'] = 'carlos arteaga'
        context['plantilla'] = 'Crear'
        context['btn_cancelar'] = reverse_lazy('crm:listar_cliente')
        context['titulo_lista'] = 'Ingrese datos del nuevo cliente'
        context['quitar_footer'] = 'si'
        context['tipo'] = 'nuevo'
        context['select_cliente'] = 'mostrar'
        empresa = Empresas.objects.filter(borrado=0,estado=1)
        context['empresa'] = empresa
        usuario = Usuario.objects.filter(borrado=0,estado=1)
        context['usuario'] = usuario
        # INICIO PARA RECORDATORIOS HEADER
        now = datetime.now()
        cont_rcrio = 0
        if len(str(now.month)) == 1:
            mes = '0' + str(now.month)
        else:
            mes = str(now.month)
        fecha = str(now.year) + '-' + mes + '-' + str(now.day)
        recordatorios = Recordatorios.objects.filter(borrado=0,usuario_creacion=self.request.user,estatus_alerta='Pendiente',fch_recordatorio=fecha)
        for x in recordatorios:
            cont_rcrio += 1
        context['cont_alerta'] = cont_rcrio 
        # FIN PARA RECORDATORIOS HEADER

        # INICIO PARA PROMESAS HEADER
        cont_promesa = 0
        promesa = Promesas.objects.filter(borrado=0,id_usuario=self.request.user,estatus_promesa='Pendiente',fecha=fecha)
        for x in promesa:
            cont_promesa += 1
        context['cont_promesa'] = cont_promesa 
        context['cont_total'] = cont_promesa + cont_rcrio
        # FIN PARA PROMESAS HEADER
        return context



class borrar_cliente(DeleteView):
    model = Clientes
    template_name = 'clientes/borrar.html'
    success_url = reverse_lazy('crm:listar_cliente')

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
        context['btn_cancelar'] = reverse_lazy('crm:listar_cliente')
        context['list_url'] = reverse_lazy('crm:listar_cliente')
        context['quitar_footer'] = 'si'
        context['url_salir'] = reverse_lazy('login:iniciar')
        context['titulo_lista'] = 'Eliminar cliente'
        # INICIO PARA RECORDATORIOS HEADER
        now = datetime.now()
        cont_rcrio = 0
        if len(str(now.month)) == 1:
            mes = '0' + str(now.month)
        else:
            mes = str(now.month)
        fecha = str(now.year) + '-' + mes + '-' + str(now.day)
        recordatorios = Recordatorios.objects.filter(borrado=0,usuario_creacion=self.request.user,estatus_alerta='Pendiente',fch_recordatorio=fecha)
        for x in recordatorios:
            cont_rcrio += 1
        context['cont_alerta'] = cont_rcrio 
        # FIN PARA RECORDATORIOS HEADER

        # INICIO PARA PROMESAS HEADER
        cont_promesa = 0
        promesa = Promesas.objects.filter(borrado=0,id_usuario=self.request.user,estatus_promesa='Pendiente',fecha=fecha)
        for x in promesa:
            cont_promesa += 1
        context['cont_promesa'] = cont_promesa 
        context['cont_total'] = cont_promesa + cont_rcrio
        # FIN PARA PROMESAS HEADER
        return context



class actualizar_cliente(UpdateView):
    model = Clientes
    form_class = formulario_cliente
    template_name = 'clientes/crear.html'
    success_url = reverse_lazy('crm:listar_cliente')

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request,*args,**kwargs):
        self.object = self.get_object()
        return super().dispatch(request,*args,**kwargs)

    def post(self, request,*args,**kwargs):
        data = {}
        try:
            registro = self.get_object()
            registro.nombre = request.POST['nombre']
            registro.id_empresa_id = request.POST['id_empresa']
            registro.id_usuario_id = request.POST['id_usuario']
            registro.tipo_id = request.POST['tipo_id']
            registro.identidad = request.POST['identidad']
            registro.fch_nacimiento = request.POST['fch_nacimiento']
            registro.estado_civil = request.POST['estado_civil']
            registro.estado = request.POST['estado'] 
            registro.usuario_modificacion = request.user.id
            registro.fch_modificacion = datetime.now()
            registro.save()
            return redirect('crm:listar_cliente')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre'] = 'carlos arteaga'
        context['plantilla'] = 'Editar'
        context['btn_cancelar'] = reverse_lazy('crm:listar_cliente')
        context['titulo_lista'] = 'Editar cliente'
        context['quitar_footer'] = 'si'
        context['tipo'] = 'editar'
        context['select_cliente'] = 'mostrar'
        cliente = Clientes.objects.filter(borrado=0, id_cliente = self.kwargs['pk'])
        z = 0
        x = 0
        for c in cliente:
            z = c.id_empresa_id
            x = c.id_usuario_id
        
        usuario = Usuario.objects.filter(borrado=0,estado=1)

        context['seleccionar'] = z
        context['seleccionaruser'] = x
        empresa = Empresas.objects.filter(borrado=0,estado=1)
        context['empresa'] = empresa
        context['usuario'] = usuario
        # INICIO PARA RECORDATORIOS HEADER
        now = datetime.now()
        cont_rcrio = 0
        if len(str(now.month)) == 1:
            mes = '0' + str(now.month)
        else:
            mes = str(now.month)
        fecha = str(now.year) + '-' + mes + '-' + str(now.day)
        recordatorios = Recordatorios.objects.filter(borrado=0,usuario_creacion=self.request.user,estatus_alerta='Pendiente',fch_recordatorio=fecha)
        for x in recordatorios:
            cont_rcrio += 1
        context['cont_alerta'] = cont_rcrio 
        # FIN PARA RECORDATORIOS HEADER

        # INICIO PARA PROMESAS HEADER
        cont_promesa = 0
        promesa = Promesas.objects.filter(borrado=0,id_usuario=self.request.user,estatus_promesa='Pendiente',fecha=fecha)
        for x in promesa:
            cont_promesa += 1
        context['cont_promesa'] = cont_promesa 
        context['cont_total'] = cont_promesa + cont_rcrio
        # FIN PARA PROMESAS HEADER
        return context

