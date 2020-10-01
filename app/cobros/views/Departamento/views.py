from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from app.cobros.models import Departamentos,Clientes,Recordatorios,Promesas
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from app.cobros.forms import form_departamento
from django.urls import reverse_lazy

from datetime import datetime

# Create your views here.


def home(request):
    diccionario = { 
        'nombre': 'carlos portillo',
        'plantilla': 'Home',
        'objeto_departamento': Departamentos.objects.all()
    }
    return render(request, 'home.html', diccionario)



"""
def listar_departamento(request):
    data = {
        'nombre': 'carlos arteaga',
        'plantilla': 'Departamentos',
        'titulo': 'Departamentos existentes',
        'titulo_lista': 'Departamentos existentes',
        'objeto_departamento': Departamentos.objects.all()
    }
    return render(request, 'Departamento/listar.html', data)
"""

# declarando vistas basadas en clase

class listview_departamento(ListView):
    model = Departamentos
    template_name = 'Departamento/listar.html'


    #esto para filtrar todos los q estén activos
    def get_queryset(self):
        return self.model.objects.filter(borrado=0)

    # sobre escribiendo el método POST
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        data = {}
        # para controlar en caso q despliegue error
        try:
            # #1: se comenta para hacer la cargada en la taba usandoi AJAX
            # #1 data = Departamentos.objects.get(pk=request.POST['id_departamento']).toJSON() #sino existe error llamará al método tiJSON definido en models.py en departamentos
            action = request.POST['action']
            
            if action == 'searchdata':
                data = []
                for i in Departamentos.objects.filter(borrado=0): # si deseamos todos colocamos .all()
                    data.append(i.toJSON())
            else:
                data['error']='Ha ocurrido un error al cargar con AJAX'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
        # #2: se comenta ya que como se envía una coleccion de diccionarios y vienen serializados se coloca el atributo, safe=False.
        # #2return JsonResponse(data)

    
    
    #para enviar un diccionario en la clase hay que sobre escribir el método get_context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre'] = 'carlos arteaga'
        context['plantilla'] = 'Departamentos'
        context['titulo'] = 'Departamentos existentes'
        context['quitar_footer'] = 'si'
        context['titulo_lista'] = 'Departamentos existentes'
        context['create_url'] = reverse_lazy('crm:crear_departamento')
        context['url_salir'] = reverse_lazy('login:iniciar')
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
    
class createview_departamento(CreateView):
    model = Departamentos
    form_class = form_departamento 
    template_name = 'Departamento/crear.html'
    success_url = reverse_lazy('crm:listar_departamento')

    
    def post(self, request,*args,**kwargs):
        data = {}
        form = self.form_class(request.POST)
        try:
            if form.is_valid():
                nuevo = Departamentos(
                    nombre = form.cleaned_data.get('nombre'),
                    usuario_creacion = request.user.id,
                    estado = form.cleaned_data.get('estado')
                )
                nuevo.save()
                return redirect('crm:listar_departamento') 
            else:
                #return render(request, self.template_name, {'error1': 'error', 'form':form, 'quitar_footer': 'si', 'tabla': 'departamento', 'titulo_lista': 'Ingrese datos del nuevo departamento'})
                return render(request, self.template_name, {'form':form, 'quitar_footer': 'si', 'titulo_lista': 'Ingrese datos del nuevo departamento','plantilla': 'Crear'})
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre'] = 'carlos arteaga'
        context['plantilla'] = 'Crear'
        context['btn_cancelar'] = reverse_lazy('crm:listar_departamento')
        context['titulo_lista'] = 'Ingrese datos del nuevo departamento'
        context['quitar_footer'] = 'si'
        context['tipo'] = 'nuevo'
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

class updateview_departamento(UpdateView):
    model = Departamentos
    form_class = form_departamento # llamamos al formulario creado en forms.py y hay q importarlo
    template_name = 'Departamento/crear.html'
    success_url = reverse_lazy('crm:listar_departamento')

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request,*args,**kwargs):
        self.object = self.get_object()
        return super().dispatch(request,*args,**kwargs)

    def post(self, request,*args,**kwargs):
        data = {}
        form = self.form_class(request.POST)
        try:
            #if form.is_valid():
                registro = self.get_object()
                registro.nombre = request.POST['nombre']
                registro.estado = request.POST['estado']
                registro.usuario_modificacion = request.user.id
                registro.fch_modificacion = datetime.now()
                try:
                    registro.save()
                    return redirect('crm:listar_departamento')
                except Exception as e:
                    return render(request, self.template_name, {'form':form, 'quitar_footer': 'si', 'titulo_lista': 'Editar departamento','plantilla': 'Editar'})
                
            #else:
                #return render(request, self.template_name, {'form':form, 'quitar_footer': 'si', 'titulo_lista': 'Editar departamento','plantilla': 'Editar'})
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre'] = 'carlos arteaga'
        context['plantilla'] = 'Editar'
        context['btn_cancelar'] = reverse_lazy('crm:listar_departamento')
        context['titulo_lista'] = 'Editar departamento'
        context['quitar_footer'] = 'si'
        context['tipo'] = 'editar'
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

class deleteview_departamento(DeleteView):
    model = Departamentos
    template_name = 'Departamento/borrar.html'
    success_url = reverse_lazy('crm:listar_departamento')

    #@method_decorator(csrf_exempt)
    def dispatch(self, request,*args,**kwargs):
        self.object = self.get_object()
        return super().dispatch(request,*args,**kwargs)

    def post(self, request,*args,**kwargs):
        data = {}
        try:
            #self.object.delete()
            registro = self.get_object()
            registro.usuario_modificacion = request.user.id
            registro.fch_modificacion = datetime.now()
            registro.borrado = 1
            registro.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre'] = 'carlos arteaga'
        context['plantilla'] = 'Eliminar'
        context['btn_cancelar'] = reverse_lazy('crm:listar_departamento')
        context['list_url'] = reverse_lazy('crm:listar_departamento')
        context['url_salir'] = reverse_lazy('login:iniciar')
        context['quitar_footer'] = 'si'
        context['titulo_lista'] = 'Eliminar departamento'
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

"""
class formview_departamento(FormView):
    # esto verificará q el formulario sea válido
    form_class = form_departamento
    template_name = 'Departamento/crear.html'
    success_url = reverse_lazy('crm:listar_departamento')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre'] = 'carlos arteaga'
        context['plantilla'] = 'Crear'
        context['btn_cancelar'] = reverse_lazy('crm:listar_departamento')
        context['titulo_lista'] = 'Form departamento'
        return context
"""