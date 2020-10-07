from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from app.usuario.forms import form_roles
from django.urls import reverse_lazy
from app.cobros.models import Departamentos,Puestos,Recordatorios,Promesas
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from app.usuario.models import Usuario,Roles,Permisos
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User


class listar_roles(LoginRequiredMixin,ListView):
    model = Roles
    template_name = 'roles/listar.html'

    def get_queryset(self):
        return self.model.objects.filter(borrado=0)

    @method_decorator(csrf_exempt)
    def dispatch(self, request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plantilla'] = 'Perfiles'
        context['quitar_footer'] = 'si'
        context['titulo_lista'] = 'Perfiles existentes'
        context['create_url'] = reverse_lazy('crear_roles')
        context['url_salir'] = reverse_lazy('login:iniciar')

        # INICIO VERIFICACIÓN DE PERMISOS
        permisos_usuario = Permisos.objects.filter(id_rol_id = self.request.user.id_rol_id)
        pantalla_actual = 1
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

class crear_roles(LoginRequiredMixin,CreateView):
    model = Roles
    form_class = form_roles
    template_name = 'roles/crear.html'
    success_url = reverse_lazy('listar_roles')

    
    def post(self, request,*args,**kwargs):
        data = {}
        form = self.form_class(request.POST)

        try:
            #if form.is_valid():
                nuevo = Roles(
                    nombre = request.POST['nombre'],
                    fch_creacion = datetime.now(),
                    usuario_creacion = int(request.user.id)
                )
                nuevo.save()
                return redirect('listar_roles') 
            #else:
                
        except Exception as e:
            return render(request, self.template_name, {'form':form, 'quitar_footer': 'si','ya_existe': 'si', 'titulo_lista': 'Ingrese datos del nuevo perfil','plantilla': 'Crear'})
            data['error'] = str(e)
        return JsonResponse(data)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plantilla'] = 'Crear'
        context['btn_cancelar'] = reverse_lazy('listar_roles')
        context['titulo_lista'] = 'Ingrese datos del nuevo perfil'
        context['quitar_footer'] = 'si'
        context['tipo'] = 'nuevo'
        #context['formguardarusuario'] = form_usuarios()
       
        # INICIO VERIFICACIÓN DE PERMISOS
        permisos_usuario = Permisos.objects.filter(id_rol_id = self.request.user.id_rol_id)
        pantalla_actual = 1
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

class editar_roles(LoginRequiredMixin,UpdateView):
    model = Roles
    form_class = form_roles
    template_name = 'roles/editar.html'
    success_url = reverse_lazy('listar_roles')

    @method_decorator(csrf_exempt)
    def dispatch(self, request,*args,**kwargs):
        self.object = self.get_object()
        return super().dispatch(request,*args,**kwargs)
    
    def post(self, request,*args,**kwargs):
        data = {}
        try:
            registro = self.get_object()
            registro.nombre = request.POST['nombre']
            registro.estado = request.POST['estado']
            registro.usuario_modificacion = int(request.user.id)
            registro.fch_modificacion = datetime.now()
            registro.save()
            return redirect('listar_roles')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plantilla'] = 'Editar'
        context['quitar_footer'] = 'si'
        context['btn_cancelar'] = reverse_lazy('listar_roles')
        context['titulo_lista'] = 'Editar perfil'

        # INICIO VERIFICACIÓN DE PERMISOS
        permisos_usuario = Permisos.objects.filter(id_rol_id = self.request.user.id_rol_id)
        pantalla_actual = 1
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


class borrar_roles(LoginRequiredMixin,DeleteView):
    model = Roles
    template_name = 'roles/borrar.html'
    success_url = reverse_lazy('listar_roles')

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
        context['btn_cancelar'] = reverse_lazy('listar_roles')
        context['list_url'] = reverse_lazy('listar_roles')
        context['quitar_footer'] = 'si'
        context['url_salir'] = reverse_lazy('login:iniciar')
        context['titulo_lista'] = 'Eliminar perfil'

        # INICIO VERIFICACIÓN DE PERMISOS
        permisos_usuario = Permisos.objects.filter(id_rol_id = self.request.user.id_rol_id)
        pantalla_actual = 1
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

