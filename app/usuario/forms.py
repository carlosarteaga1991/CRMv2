from django.forms import *
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from app.cobros.models import Departamentos,Clientes,Puestos,Empresas,Contactos,Productos,Codigos,Motivos,Gestiones,Recordatorios, Promesas, Visitas
from app.usuario.models import Usuario,Roles,Permisos
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.urls import reverse_lazy
from django.contrib.admin import widgets

class form_usuarios(ModelForm):
    user = Usuario.objects.filter(borrado=0,estado=1)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['nombres'].widget.attrs['autofocus'] = True

    class Meta():
        model = Usuario
        
        fields = '__all__'
        # si deseo excluir ciertos campos coloco
        exclude = ['fch_modificacion','usuario_modificacion','is_active','usuario_creacion','borrado','id_rol','password','last_login','ip_ultimo_acceso','usuario_administrador','id_departamento','id_puesto']

        widgets = {
            'nombres': TextInput(
                attrs={
                    'placeholder': 'Ingrese los primeros nombres',
                    'onkeypress': 'return nombre(event)',
                }
            ),
            'apellidos': TextInput(
                attrs={
                    'placeholder': 'Ingrese los apellidos',
                    'onkeypress': 'return nombre(event)',
                }
            ),
            'username': TextInput(
                attrs={
                    'placeholder': 'Formado por primero nombre y apellido, ejemplo: "nombre.apellido"',
                }
            ),
            'username': TextInput(
                attrs={
                    'onkeypress': 'return usuario(event)',
                }
            )
    
        }

class form_roles(ModelForm):
    user = Roles.objects.filter(borrado=0,estado=1)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta():
        model = Roles
        
        fields = '__all__'
        # si deseo excluir ciertos campos coloco
        exclude = ['fch_modificacion','usuario_modificacion','usuario_creacion','borrado','tiene_permisos']

        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre del perfil',
                    'onkeypress': 'return nombre(event)',
                }
            )
    
        }

class form_permisos(ModelForm):
    user = Permisos.objects.filter(borrado=0,estado=1)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['pantalla'].widget.attrs['autofocus'] = True

    class Meta():
        model = Permisos
        
        fields = '__all__'
        # si deseo excluir ciertos campos coloco
        exclude = ['fch_modificacion','usuario_modificacion','usuario_creacion','borrado','tiene_permisos']

        widgets = {
            'pantalla': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre del perfil',
                    'onkeypress': 'return nombre(event)',
                }
            )
    
        }

class form_perfil_usuarios(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['nombres'].widget.attrs['autofocus'] = True

    class Meta():
        model = Usuario
        fields = '__all__'
        exclude = ['fch_modificacion','primer_ingreso','fch_cambio_password','usuario_modificacion','cambiar_contrasenia','estado','bloqueado','is_active','usuario_creacion','borrado','id_rol','password','last_login','ip_ultimo_acceso','usuario_administrador','id_departamento','id_puesto']

        widgets = {
            'nombres': TextInput(
                attrs={
                    'placeholder': 'Ingrese los primeros nombres',
                    'onkeypress': 'return nombre(event)',
                }
            ),
            'apellidos': TextInput(
                attrs={
                    'placeholder': 'Ingrese los apellidos',
                    'onkeypress': 'return nombre(event)',
                }
            ),
            'username': TextInput(
                attrs={
                    'placeholder': 'Formado por primero nombre y apellido, ejemplo: "nombre.apellido"',
                }
            ),
            'username': TextInput(
                attrs={
                    'disabled': 'True',
                }
            )
    
        }