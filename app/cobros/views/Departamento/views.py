from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from app.cobros.models import Departamentos,Clientes
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from app.cobros.forms import form_departamento
from django.urls import reverse_lazy

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
        context['titulo_lista'] = 'Departamentos existentes'
        context['create_url'] = reverse_lazy('crm:crear_departamento')
        return context
    
class createview_departamento(CreateView):
    model = Departamentos
    form_class = form_departamento # llamamos al formulario creado en forms.py y hay q importarlo
    template_name = 'Departamento/crear.html'
    success_url = reverse_lazy('crm:listar_departamento')

    # se comenta ya que en el crear.html la variable {{ form.errors }} contiene lo mismo
    """
    def post(self, request, *args, **kwargs):
        form = form_departamento(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)
        else:
            self.object = None
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return render(request, self.template_name, context)   
    """ 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre'] = 'carlos arteaga'
        context['plantilla'] = 'Crear'
        context['btn_cancelar'] = reverse_lazy('crm:listar_departamento')
        context['titulo_lista'] = 'Ingrese datos del nuevo departamentos'
        return context

class updateview_departamento(UpdateView):
    model = Departamentos
    form_class = form_departamento # llamamos al formulario creado en forms.py y hay q importarlo
    template_name = 'Departamento/crear.html'
    success_url = reverse_lazy('crm:listar_departamento')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre'] = 'carlos arteaga'
        context['plantilla'] = 'Editar'
        context['btn_cancelar'] = reverse_lazy('crm:listar_departamento')
        context['titulo_lista'] = 'Editar departamento'
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
        context['titulo_lista'] = 'Eliminar departamento'
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