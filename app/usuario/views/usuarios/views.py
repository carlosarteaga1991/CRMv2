from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from app.cobros.models import Departamentos,Puestos,Recordatorios,Promesas
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from app.usuario.forms import form_usuarios,form_perfil_usuarios
from django.urls import reverse_lazy

from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from app.usuario.models import Usuario,Roles,Permisos
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from app.usuario.permisos import asignar_permiso
from app.usuario.alertas import alertas

class listar_usuarios(LoginRequiredMixin,ListView):
    model = Usuario
    template_name = 'usuario/listar.html'

    def get_queryset(self):
        return self.model.objects.filter(borrado=0)

    @method_decorator(csrf_exempt)
    def dispatch(self, request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plantilla'] = 'Usuarios'
        context['quitar_footer'] = 'si'
        context['titulo_lista'] = 'Usuarios existentes'
        context['create_url'] = reverse_lazy('crear_usuarios')
        context['url_salir'] = reverse_lazy('login:iniciar')
        departamento = Departamentos.objects.filter(borrado=0,estado=1)
        puesto = Puestos.objects.filter(borrado=0,estado=1)
        context['departamento'] = departamento
        context['puesto'] = puesto

        # INICIO VERIFICACIÓN DE PERMISOS
        context['permisos'] = asignar_permiso().metodo_permiso(3,'ver',int(self.request.user.id_rol_id),self.request.user.usuario_administrador)
        # FIN VERIFICACIÓN DE PERMISOS

        # INICIO PARA RECORDATORIOS HEADER
        context['cont_alerta'] = alertas().recordatorios(self.request.user)
        # FIN PARA RECORDATORIOS HEADER

        # INICIO PARA PROMESAS HEADER 
        context['cont_promesa'] = alertas().promesas(self.request.user)
        context['cont_total'] = alertas().promesas(self.request.user) + alertas().recordatorios(self.request.user)
        # FIN PARA PROMESAS HEADER

        return context

class crear_usuario(LoginRequiredMixin,CreateView):
    model = Usuario
    form_class = form_usuarios 
    template_name = 'usuario/crear.html'
    success_url = reverse_lazy('listar_usuarios')

    
    def post(self, request,*args,**kwargs):
        data = {}
        form = self.form_class(request.POST)

        try:
            #if form.is_valid():
                nuevo = Usuario(
                    nombres = request.POST['nombres'],
                    apellidos = request.POST['apellidos'],
                    id_departamento = int(request.POST['id_departamento']),
                    id_puesto = int(request.POST['id_puesto']),
                    password = make_password(request.POST['username']),
                    fch_creacion = datetime.now(),
                    username = request.POST['username'],
                    email = request.POST['email'],
                    usuario_creacion = int(request.user.id),
                    id_rol_id = int(request.POST['id_rol'])
                )
                nuevo.save()
                return redirect('listar_usuarios') 
            #else:
                
        except Exception as e:
            departamento = Departamentos.objects.filter(borrado=0,estado=1)
            puesto = Puestos.objects.filter(borrado=0,estado=1)
            rol = Roles.objects.filter(borrado=0,estado=1,tiene_permisos='Si')
            return render(request, self.template_name, {'rol': rol,'puesto':puesto,'departamento':departamento,'form':form, 'quitar_footer': 'si','ya_existe': 'si','nombres_post':request.POST['nombres'],'apellidos_post':request.POST['apellidos'],'email_post':request.POST['email'],'user_post':request.POST['username'], 'titulo_lista': 'Ingrese datos del nuevo usuario','plantilla': 'Crear'})
            data['error'] = str(e)
        return JsonResponse(data)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plantilla'] = 'Crear'
        context['btn_cancelar'] = reverse_lazy('listar_usuarios')
        context['titulo_lista'] = 'Ingrese datos del nuevo usuario'
        context['quitar_footer'] = 'si'
        context['tipo'] = 'nuevo'
        context['formguardarusuario'] = form_usuarios()
        departamento = Departamentos.objects.filter(borrado=0,estado=1)
        rol = Roles.objects.filter(borrado=0,estado=1,tiene_permisos='Si')
        puesto = Puestos.objects.filter(borrado=0,estado=1)
        context['departamento'] = departamento
        context['puesto'] = puesto
        context['rol'] = rol

        # INICIO VERIFICACIÓN DE PERMISOS
        context['permisos'] = asignar_permiso().metodo_permiso(3,'crear',int(self.request.user.id_rol_id),self.request.user.usuario_administrador)
        # FIN VERIFICACIÓN DE PERMISOS

        # INICIO PARA RECORDATORIOS HEADER
        context['cont_alerta'] = alertas().recordatorios(self.request.user)
        # FIN PARA RECORDATORIOS HEADER

        # INICIO PARA PROMESAS HEADER 
        context['cont_promesa'] = alertas().promesas(self.request.user)
        context['cont_total'] = alertas().promesas(self.request.user) + alertas().recordatorios(self.request.user)
        # FIN PARA PROMESAS HEADER
        
        return context

class editar_usuario(LoginRequiredMixin,UpdateView):
    model = Usuario
    form_class = form_usuarios
    template_name = 'usuario/editar.html'
    success_url = reverse_lazy('listar_usuarios')

    @method_decorator(csrf_exempt)
    def dispatch(self, request,*args,**kwargs):
        self.object = self.get_object()
        return super().dispatch(request,*args,**kwargs)
    
    def post(self, request,*args,**kwargs):
        data = {}
        try:
            registro = self.get_object()
            registro.id_puesto = int(request.POST['id_puesto'])
            registro.id_departamento = int(request.POST['id_departamento'])
            registro.username = request.POST['username']
            registro.email = request.POST['email']
            registro.nombres = request.POST['nombres']
            registro.apellidos = request.POST['apellidos']
            registro.estado = request.POST['estado']
            registro.id_rol_id = request.POST['id_rol']
            if request.POST['cambiar_contrasenia'] == '1':
                registro.cambiar_contrasenia = request.POST['cambiar_contrasenia']
                registro.password = make_password(request.POST['username'])
            else:
                registro.cambiar_contrasenia = request.POST['cambiar_contrasenia']
            registro.bloqueado = request.POST['bloqueado']
            registro.usuario_modificacion = int(request.user.id)
            registro.fch_modificacion = datetime.now()
            registro.save()
            return redirect('listar_usuarios')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plantilla'] = 'Editar'
        context['quitar_footer'] = 'si'
        context['btn_cancelar'] = reverse_lazy('listar_usuarios')
        context['titulo_lista'] = 'Editar usuario'
        departamento = Departamentos.objects.filter(borrado=0,estado=1)
        puesto = Puestos.objects.filter(borrado=0,estado=1)
        context['departamento'] = departamento
        context['puesto'] = puesto
        user = Usuario.objects.filter(borrado=0, id = self.kwargs['pk'])
        z = 0
        zz = 0
        zzz = 0
        for c in user:
            z = c.id_departamento
            zz = c.id_puesto
            zzz = c.id_rol_id
        context['seleccionar_dep'] = z
        context['seleccionar_puesto'] = zz
        context['seleccionar_rol'] = zzz
        rol = Roles.objects.filter(borrado=0,estado=1,tiene_permisos='Si')
        context['rol'] = rol

        # INICIO VERIFICACIÓN DE PERMISOS
        context['permisos'] = asignar_permiso().metodo_permiso(3,'actualizar',int(self.request.user.id_rol_id),self.request.user.usuario_administrador)
        # FIN VERIFICACIÓN DE PERMISOS

        # INICIO PARA RECORDATORIOS HEADER
        context['cont_alerta'] = alertas().recordatorios(self.request.user)
        # FIN PARA RECORDATORIOS HEADER

        # INICIO PARA PROMESAS HEADER 
        context['cont_promesa'] = alertas().promesas(self.request.user)
        context['cont_total'] = alertas().promesas(self.request.user) + alertas().recordatorios(self.request.user)
        # FIN PARA PROMESAS HEADER

        return context


class borrar_usuario(LoginRequiredMixin,DeleteView):
    model = Usuario
    template_name = 'usuario/borrar.html'
    success_url = reverse_lazy('listar_usuarios')

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
        context['btn_cancelar'] = reverse_lazy('listar_usuarios')
        context['list_url'] = reverse_lazy('listar_usuarios')
        context['quitar_footer'] = 'si'
        context['url_salir'] = reverse_lazy('login:iniciar')
        context['titulo_lista'] = 'Eliminar usuario'

        # INICIO VERIFICACIÓN DE PERMISOS
        context['permisos'] = asignar_permiso().metodo_permiso(3,'borrar',int(self.request.user.id_rol_id),self.request.user.usuario_administrador)
        # FIN VERIFICACIÓN DE PERMISOS

        # INICIO PARA RECORDATORIOS HEADER
        context['cont_alerta'] = alertas().recordatorios(self.request.user)
        # FIN PARA RECORDATORIOS HEADER

        # INICIO PARA PROMESAS HEADER 
        context['cont_promesa'] = alertas().promesas(self.request.user)
        context['cont_total'] = alertas().promesas(self.request.user) + alertas().recordatorios(self.request.user)
        # FIN PARA PROMESAS HEADER

        return context

class editar_perfil_usuario(LoginRequiredMixin,UpdateView):
    model = Usuario
    form_class = form_perfil_usuarios
    template_name = 'usuario/perfil.html'
    success_url = reverse_lazy('crm:dashboard')

    @method_decorator(csrf_exempt)
    def dispatch(self, request,*args,**kwargs):
        self.object = self.get_object()
        return super().dispatch(request,*args,**kwargs)

    def get_object(self, get_queryset=None):
        return self.request.user
    
    def post(self, request,*args,**kwargs):
        data = {}
        try:
            registro = self.get_object()
            registro.email = request.POST['email']
            registro.nombres = request.POST['nombres']
            registro.apellidos = request.POST['apellidos']
            registro.usuario_modificacion = int(request.user.id)
            registro.fch_modificacion = datetime.now()
            registro.save()
            return redirect('crm:dashboard')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plantilla'] = 'Editar'
        context['quitar_footer'] = 'si'
        context['btn_cancelar'] = reverse_lazy('crm:dashboard')
        context['titulo_lista'] = 'Editar Perfil de Usuario'
        departamento = Departamentos.objects.filter(borrado=0,estado=1)
        puesto = Puestos.objects.filter(borrado=0,estado=1)
        context['departamento'] = departamento
        context['puesto'] = puesto
        
        user = Usuario.objects.filter(borrado=0, id = self.request.user.id)
        z = 0
        zz = 0
        zzz = 0
        for c in user:
            z = c.id_departamento
            zz = c.id_puesto
            zzz = c.id_rol_id
        context['seleccionar_dep'] = z
        context['seleccionar_puesto'] = zz
        context['seleccionar_rol'] = zzz
        rol = Roles.objects.filter(borrado=0,estado=1,tiene_permisos='Si')
        context['rol'] = rol
        

        # INICIO VERIFICACIÓN DE PERMISOS
        context['permisos'] = asignar_permiso().metodo_permiso(3,'actualizar',int(self.request.user.id_rol_id),self.request.user.usuario_administrador)
        # FIN VERIFICACIÓN DE PERMISOS
        

        # INICIO PARA RECORDATORIOS HEADER
        context['cont_alerta'] = alertas().recordatorios(self.request.user)
        # FIN PARA RECORDATORIOS HEADER

        # INICIO PARA PROMESAS HEADER 
        context['cont_promesa'] = alertas().promesas(self.request.user)
        context['cont_total'] = alertas().promesas(self.request.user) + alertas().recordatorios(self.request.user)
        # FIN PARA PROMESAS HEADER

        return context

class cambiar_password_usuario(LoginRequiredMixin,FormView):
    model = Usuario
    form_class = PasswordChangeForm
    template_name = 'usuario/cambiar_password.html'
    success_url = reverse_lazy('inicio_sesion')

    @method_decorator(csrf_exempt)
    def dispatch(self, request,*args,**kwargs):
        self.object = self.get_object()
        return super().dispatch(request,*args,**kwargs)
    
    def get_object(self, get_queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = PasswordChangeForm(user=self.request.user)
        form.fields['old_password'].widget.attrs['class'] = 'form-control'
        form.fields['new_password1'].widget.attrs['class'] = 'form-control'
        form.fields['new_password2'].widget.attrs['class'] = 'form-control'
        
        form.fields['old_password'].widget.attrs['autocomplete'] = 'off'
        form.fields['new_password1'].widget.attrs['autocomplete'] = 'off'
        form.fields['new_password2'].widget.attrs['autocomplete'] = 'off'

        form.fields['old_password'].widget.attrs['placeholder'] = 'Ingrese su contraseña actual'
        form.fields['new_password1'].widget.attrs['placeholder'] = 'Ingrese su nueva contraseña'
        form.fields['new_password2'].widget.attrs['placeholder'] = 'Repita su contraseña'
        return form
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'cambiar_contrasenia':
                form = PasswordChangeForm(user=request.user, data=request.POST)
                form.fields['old_password'].widget.attrs['value'] = request.POST['old_password']
                form.fields['new_password1'].widget.attrs['value'] = request.POST['new_password1']
                form.fields['new_password2'].widget.attrs['value'] = request.POST['new_password2']
                if form.is_valid():
                    form.save()
                    registro = self.get_object()
                    registro.fch_cambio_password = datetime.now()
                    registro.save()
                    #update_session_auth_hash(request, form.user)
                    return redirect('/login/')
                else:
                    data['error'] = form.errors
                    return render(request, self.template_name, {'action': 'cambiar_contrasenia','form':form, 'quitar_footer': 'si', 'titulo_lista': 'Editar Contraseña de Usuario','plantilla': 'Editar Contraseña','permisos':asignar_permiso().metodo_permiso(3,'actualizar',int(self.request.user.id_rol_id),self.request.user.usuario_administrador),'cont_alerta':alertas().recordatorios(self.request.user),'cont_promesa':alertas().promesas(self.request.user),'cont_total': alertas().promesas(self.request.user) + alertas().recordatorios(self.request.user)})
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plantilla'] = 'Editar Contraseña'
        context['quitar_footer'] = 'si'
        context['btn_cancelar'] = reverse_lazy('crm:dashboard')
        context['titulo_lista'] = 'Editar Contraseña de Usuario'
        context['action'] = 'cambiar_contrasenia'
      
        # INICIO VERIFICACIÓN DE PERMISOS
        context['permisos'] = asignar_permiso().metodo_permiso(3,'actualizar',int(self.request.user.id_rol_id),self.request.user.usuario_administrador)
        # FIN VERIFICACIÓN DE PERMISOS
        
        # INICIO PARA RECORDATORIOS HEADER
        context['cont_alerta'] = alertas().recordatorios(self.request.user)
        # FIN PARA RECORDATORIOS HEADER

        # INICIO PARA PROMESAS HEADER 
        context['cont_promesa'] = alertas().promesas(self.request.user)
        context['cont_total'] = alertas().promesas(self.request.user) + alertas().recordatorios(self.request.user)
        # FIN PARA PROMESAS HEADER

        return context