from django.shortcuts import render
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from app.cobros.models import Departamentos,Clientes
from django.views.generic import ListView, CreateView, UpdateView
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
    
    #para enviar un diccionario en la clase hay que sobre escribir el método get_context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre'] = 'carlos arteaga'
        context['plantilla'] = 'Departamentos'
        context['titulo'] = 'Departamentos existentes'
        context['titulo_lista'] = 'Departamentos existentes'
        context['create_url'] = reverse_lazy('crm:crear_departamento')
        return context

    # sobre escribiendo el método POST
    @method_decorator(csrf_exempt)
    def dispatch(self, request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        data = {}
        # para controlar en caso q despliegue error
        try:
            data = Departamentos.objects.get(pk=request.POST['id_departamento']).toJSON() #sino existe error llamará al método tiJSON definido en models.py en departamentos
        except Exception as e:
            data['error'] = str(e)
        
        return JsonResponse(data)

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