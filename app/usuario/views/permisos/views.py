from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from app.usuario.forms import form_permisos
from django.urls import reverse_lazy
from app.cobros.models import Departamentos,Puestos,Recordatorios,Promesas
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from app.usuario.models import Usuario,Roles,Permisos,Pantallas
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User


class listar_permisos(LoginRequiredMixin,ListView):
    model = Permisos
    template_name = 'permisos/listar.html'

    def get_queryset(self):
        return self.model.objects.filter(borrado=0)

    @method_decorator(csrf_exempt)
    def dispatch(self, request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plantilla'] = 'Permisos'
        context['quitar_footer'] = 'si'
        context['titulo_lista'] = 'Permisos existentes'
        context['create_url'] = reverse_lazy('crear_permisos')
        context['url_salir'] = reverse_lazy('login:iniciar')

        # INICIO VERIFICACIÓN DE PERMISOS
        permisos_usuario = Permisos.objects.filter(id_rol_id = self.request.user.id_rol_id)
        pantalla_actual = 2
        ver = 0
        borrar = 0
        actualizar = 0
        crear = 0
        for x in permisos_usuario:
            if x.ver == 1 and x.pantalla_id == pantalla_actual:
                ver += 1
            if x.actualizar == 1 and x.pantalla_id == pantalla_actual:
                actualizar += 1
            if x.crear == 1 and x.pantalla_id == pantalla_actual:
                crear += 1
            if x.borrar == 1 and x.pantalla_id == pantalla_actual:
                borrar += 1
        context['permisos_usuario'] = permisos_usuario
        context['ver_pantalla'] = ver
        context['actualizar_pantalla'] = actualizar
        context['crear_pantalla'] = crear
        context['borrar_pantalla'] = borrar
        context['numero_pantalla'] = pantalla_actual
        context['usuario_administrador'] = self.request.user.usuario_administrador 
        # FIN VERIFICACIÓN DE PERMISOS
        

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

class crear_permisos(LoginRequiredMixin,CreateView):
    model = Permisos
    form_class = form_permisos
    template_name = 'permisos/crear.html'
    success_url = reverse_lazy('listar_roles')

    
    def post(self, request,*args,**kwargs):
        data = {}
        form = self.form_class(request.POST)
        condicion_pantalla = Permisos.objects.filter(borrado=0,estado=1,id_rol_id=int(request.POST['id_rol']))
        x = 0
        for  p in condicion_pantalla:
            if p.pantalla_id == int(request.POST['pantalla']):
                x = 1

        try:
            #for p in condicion_pantalla:
                if x == 1:
                    rol = Roles.objects.filter(borrado=0,estado=1)
                    pantalla = Pantallas.objects.all()
                    return render(request,self.template_name, {'pantalla':pantalla,'ya_existe': 'si','form':form,'rol':rol, 'quitar_footer': 'si', 'titulo_lista': 'Seleccione los datos del nuevo permiso','plantilla': 'Crear'})
                else:
                    nuevo = Permisos(
                        id_rol_id = int(request.POST['id_rol']),
                        pantalla_id = int(request.POST['pantalla']),
                        ver = int(request.POST['ver']),
                        actualizar = int(request.POST['actualizar']),
                        crear = int(request.POST['crear']),
                        borrar = int(request.POST['borrar']),
                        fch_creacion = datetime.now(),
                        usuario_creacion = int(request.user.id)
                    )
                    nuevo.save()
                    return redirect('listar_permisos')
        except Exception as e:
            return render(request, self.template_name, {'form':form, 'quitar_footer': 'si', 'titulo_lista': 'Seleccione los datoxxxs del nuevo permiso','plantilla': 'Crear'})
            data['error'] = str(e)
        return JsonResponse(data)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plantilla'] = 'Crear'
        context['btn_cancelar'] = reverse_lazy('listar_permisos')
        context['titulo_lista'] = 'Seleccione los datos del nuevo permiso'
        context['quitar_footer'] = 'si'
        context['tipo'] = 'nuevo'
        rol = Roles.objects.filter(borrado=0,estado=1)
        context['rol'] = rol
        pantalla = Pantallas.objects.all()
        context['pantalla'] = pantalla
        #context['formguardarusuario'] = form_usuarios()
       
        # INICIO VERIFICACIÓN DE PERMISOS
        permisos_usuario = Permisos.objects.filter(id_rol_id = self.request.user.id_rol_id)
        pantalla_actual = 2
        ver = 0
        borrar = 0
        actualizar = 0
        crear = 0
        for x in permisos_usuario:
            if x.ver == 1 and x.pantalla_id == pantalla_actual:
                ver += 1
            if x.actualizar == 1 and x.pantalla_id == pantalla_actual:
                actualizar += 1
            if x.crear == 1 and x.pantalla_id == pantalla_actual:
                crear += 1
            if x.borrar == 1 and x.pantalla_id == pantalla_actual:
                borrar += 1
        context['permisos_usuario'] = permisos_usuario
        context['ver_pantalla'] = ver
        context['actualizar_pantalla'] = actualizar
        context['crear_pantalla'] = crear
        context['borrar_pantalla'] = borrar
        context['numero_pantalla'] = pantalla_actual
        context['usuario_administrador'] = self.request.user.usuario_administrador 
        # FIN VERIFICACIÓN DE PERMISOS

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

class editar_permisos(LoginRequiredMixin,UpdateView):
    model = Permisos
    form_class = form_permisos
    template_name = 'permisos/editar.html'
    success_url = reverse_lazy('listar_permisos')

    @method_decorator(csrf_exempt)
    def dispatch(self, request,*args,**kwargs):
        self.object = self.get_object()
        return super().dispatch(request,*args,**kwargs)
    
    def post(self, request,*args,**kwargs):
        data = {}
        try:
            registro = self.get_object()
            registro.id_rol_id = request.POST['id_rol']
            registro.pantalla_id = request.POST['pantalla']
            registro.estado = request.POST['estado']
            registro.ver = int(request.POST['ver'])
            registro.actualizar = int(request.POST['actualizar'])
            registro.crear = int(request.POST['crear'])
            registro.borrar = int(request.POST['borrar'])
            registro.usuario_modificacion = int(request.user.id)
            registro.fch_modificacion = datetime.now()
            registro.save()
            return redirect('listar_permisos')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plantilla'] = 'Editar'
        context['quitar_footer'] = 'si'
        context['btn_cancelar'] = reverse_lazy('listar_permisos')
        context['titulo_lista'] = 'Editar permiso'
        rol = Roles.objects.filter(borrado=0,estado=1)
        context['rol'] = rol
        permiso = Permisos.objects.filter(id_permiso = int(self.kwargs['pk']))
        pantalla = Pantallas.objects.all()
        context['iterar_pantalla'] = pantalla
        for x in permiso:
            context['pantalla'] = x.pantalla_id
            context['id_rol'] = x.id_rol_id
            context['ver_select'] = x.ver
            context['actualizar'] = x.actualizar
            context['crear'] = x.crear
            context['borrar'] = x.borrar
        
        # INICIO VERIFICACIÓN DE PERMISOS
        permisos_usuario = Permisos.objects.filter(id_rol_id = self.request.user.id_rol_id)
        pantalla_actual = 2
        ver = 0
        borrar = 0
        actualizar = 0
        crear = 0
        for x in permisos_usuario:
            if x.ver == 1 and x.pantalla_id == pantalla_actual:
                ver += 1
            if x.actualizar == 1 and x.pantalla_id == pantalla_actual:
                actualizar += 1
            if x.crear == 1 and x.pantalla_id == pantalla_actual:
                crear += 1
            if x.borrar == 1 and x.pantalla_id == pantalla_actual:
                borrar += 1
        context['permisos_usuario'] = permisos_usuario
        context['ver_pantalla'] = ver
        context['actualizar_pantalla'] = actualizar
        context['crear_pantalla'] = crear
        context['borrar_pantalla'] = borrar
        context['numero_pantalla'] = pantalla_actual
        context['usuario_administrador'] = self.request.user.usuario_administrador 
        # FIN VERIFICACIÓN DE PERMISOS

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


class borrar_permisos(LoginRequiredMixin,DeleteView):
    model = Permisos
    template_name = 'permisos/borrar.html'
    success_url = reverse_lazy('listar_permisos')

    def dispatch(self, request,*args,**kwargs):
        self.object = self.get_object()
        return super().dispatch(request,*args,**kwargs)

    def post(self, request,*args,**kwargs):
        data = {}
        try:
            registro = self.get_object()
            registro.borrado = 1
            registro.usuario_modificacion = int(request.user.id)
            registro.fch_modificacion = datetime.now()
            registro.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plantilla'] = 'Eliminar'
        context['btn_cancelar'] = reverse_lazy('listar_permisos')
        context['list_url'] = reverse_lazy('listar_permisos')
        context['quitar_footer'] = 'si'
        context['url_salir'] = reverse_lazy('login:iniciar')
        context['titulo_lista'] = 'Eliminar permiso'
        context['borrar_titulo'] = 'de permiso que pertenece a '

        # INICIO VERIFICACIÓN DE PERMISOS
        permisos_usuario = Permisos.objects.filter(id_rol_id = self.request.user.id_rol_id)
        pantalla_actual = 2
        ver = 0
        borrar = 0
        actualizar = 0
        crear = 0
        for x in permisos_usuario:
            if x.ver == 1 and x.pantalla_id == pantalla_actual:
                ver += 1
            if x.actualizar == 1 and x.pantalla_id == pantalla_actual:
                actualizar += 1
            if x.crear == 1 and x.pantalla_id == pantalla_actual:
                crear += 1
            if x.borrar == 1 and x.pantalla_id == pantalla_actual:
                borrar += 1
        context['permisos_usuario'] = permisos_usuario
        context['ver_pantalla'] = ver
        context['actualizar_pantalla'] = actualizar
        context['crear_pantalla'] = crear
        context['borrar_pantalla'] = borrar
        context['numero_pantalla'] = pantalla_actual
        context['usuario_administrador'] = self.request.user.usuario_administrador 
        # FIN VERIFICACIÓN DE PERMISOS

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

