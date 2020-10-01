from django.views.generic import ListView,UpdateView
from app.cobros.models import Promesas
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.urls import reverse_lazy
from app.cobros.forms import formulario_seg_promesas
from django.shortcuts import render,redirect

from datetime import datetime

class listar_seg_promesas(ListView):
    model = Promesas
    template_name = 'seguimiento_promesas/listar.html'

    def get_queryset(self):
        return self.model.objects.filter(borrado=0)

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plantilla'] = 'Seguimiento'
        context['titulo_lista'] = 'Total de promesas'
        #context['create_url'] = reverse_lazy('crm:crear_motivo')
        #context['url_salir'] = reverse_lazy('login:iniciar')
        context['quitar_footer'] = 'si'
        context['quitar_btn_nuevo'] = 'si'
        return context

class actualizar_seg_promesas(UpdateView):
    model = Promesas
    form_class = formulario_seg_promesas
    template_name = 'seguimiento_promesas/crear.html'
    success_url = reverse_lazy('crm:listar_seg_promesas')

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request,*args,**kwargs):
        self.object = self.get_object()
        return super().dispatch(request,*args,**kwargs)

    
    def post(self, request,*args,**kwargs):
        data = {}
        try:
            registro = self.get_object()
            registro.valor = request.POST['valor']
            registro.estatus_promesa = request.POST['estatus_promesa']
            registro.usuario_modificacion = request.user.id
            registro.fch_modificacion = datetime.now()
            registro.save()
            return redirect('crm:listar_seg_promesas')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plantilla'] = 'Editar'
        context['quitar_footer'] = 'si'
        context['btn_cancelar'] = reverse_lazy('crm:listar_seg_promesas')
        context['titulo_lista'] = 'Editar promesa'
        context['tipo'] = 'editar'
        return context