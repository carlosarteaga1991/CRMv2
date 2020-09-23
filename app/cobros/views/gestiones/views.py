from django.views.generic import ListView, CreateView,DeleteView,UpdateView,TemplateView
from app.cobros.models import Codigos,Motivos,Gestiones,Contactos,Clientes,Productos
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.urls import reverse_lazy
from app.cobros.forms import formulario_motivos,formulario_gestion,formualario_guardar_gestion
from django.shortcuts import render,redirect

from datetime import datetime


class listar_gestiones(TemplateView):
    template_name = 'gestiones/listar.html'
    form_class = formualario_guardar_gestion 

    def get_queryset(self):
        return self.model.objects.filter(borrado=0)

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        form = self.form_class(request.POST)
        
        try:
            # INICIO esto para hacer el select anidado con AJAX
           
            #action = request.POST['action']
            #if action == 'search_codigo_id':
            #    data = []
            #    #data = [{'id': '', 'text': '---------'}]
            #    for i in Motivos.objects.filter(id_codigo=request.POST['id']):
            #        data.append({'id':i.id_motivo, 'descripcion':i.descripcion})
            #        #data.append({'id':i.id_motivo, 'text':i.descripcion})
            #else:
            #    data['error'] = 'Ha ocurrido un error'
            
            # FIN esto para hacer el select anidado con AJAX
           
            # importante cuando quiuto lo del anidamiento si guarda bien y comento lo del form.is_valid y sus referencias

            #if form.is_valid():
            nuevo = Gestiones(
                descripcion = request.POST['descripcion'],
                id_codigo_id = int(request.POST['codigo']),
                id_motivo_id = int(request.POST['motivo']),
                id_cliente_id = self.kwargs['pk'],
                #id_usuario_id = request.user.id,
                usuario_creacion_id = request.user.id,
                estado = '1'
            )
            nuevo.save()
            return redirect('/cobros/gestion/' + str(self.kwargs['pk']) +'/')
     
                
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        var = 0
        var2 = 0
        cliente = Clientes.objects.filter(borrado=0,id_cliente=self.kwargs['pk'])
        productos = Productos.objects.filter(borrado=0,id_cliente=self.kwargs['pk'])
        contactos = Contactos.objects.filter(borrado=0,id_cliente=self.kwargs['pk'])
        gestiones = Gestiones.objects.filter(borrado=0,id_cliente=self.kwargs['pk']).order_by('-fch_gestion')
        codigos = Codigos.objects.filter(borrado=0,estado=1)
        motivos = Motivos.objects.filter(borrado=0,estado=1)
        mora = 0

        for x in productos:
            var += x.saldo_total
            var2 += 1
            if x.dias_mora >= mora:
                mora = x.dias_mora
        
        for y in cliente:
            usuario_duenio = y.id_usuario
          

        context = super().get_context_data(**kwargs)
        context['saldo_total'] = var
        context['estado'] = var2
        context['usuario_duenio'] = usuario_duenio
        context['plantilla'] = 'Gestiones'
        context['dias_mora'] = mora
        context['quitar_footer'] = 'si'
        context['create_url'] = reverse_lazy('crm:crear_motivo')
        context['url_salir'] = reverse_lazy('login:iniciar')
        context['form'] = formulario_gestion()
        context['formGuardar'] = formualario_guardar_gestion()
        context['btn_cancelar'] = reverse_lazy('crm:listar_cliente')
        context['tipo'] = ''
        
        return {'cliente': cliente, 'contactos':contactos, 'gestiones': gestiones, 'context': context, 'productos': productos,'codigos': codigos, 'motivos': motivos}



"""

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
        context['btn_cancelar'] = reverse_lazy('crm:listar_motivos')
        context['titulo_lista'] = 'Editar motivo'
        context['tipo'] = 'editar'
        return context

"""