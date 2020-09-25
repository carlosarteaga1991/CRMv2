from django.views.generic import ListView, CreateView,DeleteView,UpdateView,TemplateView
from app.cobros.models import Codigos,Motivos,Gestiones,Contactos,Clientes,Productos,Promesas,Pagos,Visitas
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.urls import reverse_lazy
from app.cobros.forms import formulario_motivos,formulario_gestion,formualario_guardar_gestion,formulario_alertas
from django.shortcuts import render,redirect

from datetime import datetime,date


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
        now = datetime.now()
        var = 0
        var2 = 0
        var3 = 0
        var4 = 0
        var5 = 0
        var6 = 0
        var7 = 0
        var8 = 0
        cliente = Clientes.objects.filter(borrado=0,id_cliente=self.kwargs['pk'])
        productos = Productos.objects.filter(borrado=0,id_cliente=self.kwargs['pk'])
        promesas = Promesas.objects.filter(borrado=0,id_cliente=self.kwargs['pk'])
        visitas = Visitas.objects.filter(borrado=0,id_cliente=self.kwargs['pk'])
        promesas_incumplidas = Promesas.objects.filter(borrado=0,estatus_promesa=3,id_cliente=self.kwargs['pk'])
        pagos = Pagos.objects.filter(borrado=0,id_cliente=self.kwargs['pk'])
        ultimo_pago = Pagos.objects.filter(borrado=0,id_cliente=self.kwargs['pk'])
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
        
        for x in promesas:
            var3 += 1

        for x in promesas_incumplidas:
            var5 += 1
        
        for x in visitas:
            var7 += 1
        
        for x in pagos:
            var4 += 1
        
        for x in contactos:
            var8 += 1
        
        for x in ultimo_pago:
            ultimo_pago = x.fecha
            var6 += 1
        if var6 == 0:
            ultimo_pago='Sin Pagos'

        for y in cliente:
            usuario_duenio = y.id_usuario

        if len(str(now.month)) == 1:
            mes = '0' + str(now.month)
          

        context = super().get_context_data(**kwargs)
        context['saldo_total'] = var
        context['cont_produtos'] = var2
        context['cont_pagos'] = var4
        context['cont_visitas'] = var7
        context['cont_promesas'] = var3
        context['cont_contactos'] = var8
        context['promesas_incumplidas'] = var5
        context['ultimo_pago'] = ultimo_pago
        context['usuario_duenio'] = usuario_duenio
        context['plantilla'] = 'Gestiones'
        context['dias_mora'] = mora
        context['fecha_actual'] = str(now.year) + '-' + mes + '-' + str(now.day)
        context['quitar_footer'] = 'si'
        context['create_url'] = reverse_lazy('crm:crear_motivo')
        context['url_salir'] = reverse_lazy('login:iniciar')
        context['form'] = formulario_gestion()
        context['form_alerta'] = formulario_alertas()
        context['formGuardar'] = formualario_guardar_gestion()
        context['btn_cancelar'] = reverse_lazy('crm:listar_cliente')
        context['tipo'] = ''
        context['abrir']=0
        
        return {'cliente': cliente, 'contactos':contactos, 'gestiones': gestiones,'visitas': visitas, 'context': context,'promesas': promesas, 'productos': productos,'codigos': codigos, 'motivos': motivos, 'pagos': pagos}


