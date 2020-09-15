from django.forms import *
from app.cobros.models import Departamentos,Puestos
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from app.cobros.models import Departamentos,Clientes
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.urls import reverse_lazy




class form_departamento(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['nombre'].widget.attrs['autofocus'] = True
        
        #self.fields['usuario_creacion'].widget.attrs['value'] = ''

    class Meta():
        model = Departamentos
        
        fields = '__all__'
        # si deseo excluir ciertos campos coloco
        exclude = ['fch_modificacion','usuario_modificacion','usuario_creacion','borrado']

        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            ),
            """
            'usuario_creacion': TextInput(
                attrs={
                    'placeholder': 'user',
                    #'type': 'hidden',
                    

                }
            ),
            """
            'estado': Select(
                attrs={
                    #'size': '10'
                }
            )


     
        }


class formulario_puestos(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['nombre'].widget.attrs['autofocus'] = True
        
        #self.fields['usuario_creacion'].widget.attrs['value'] = ''

    class Meta():
        model = Puestos
        fields = '__all__'
        exclude = ['fch_modificacion','usuario_modificacion','usuario_creacion','borrado']

        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre del puesto',
                }
            ),
            """
            'usuario_creacion': TextInput(
                attrs={
                    'placeholder': 'user',
                    #'type': 'hidden',
                    

                }
            ),
            """
            'estado': Select(
                attrs={
                    #'size': '10'
                }
            )


     
        }
