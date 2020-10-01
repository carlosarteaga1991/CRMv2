from django.forms import *
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from app.cobros.models import Departamentos,Clientes,Puestos,Empresas,Contactos,Productos,Codigos,Motivos,Gestiones,Recordatorios, Promesas, Visitas
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.urls import reverse_lazy
from django.contrib.admin import widgets




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
        exclude = ['fch_modificacion','usuario_modificacion','usuario_creacion','borrado', 'id_departamento']

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

class formulario_empresa(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['nombre_empresa'].widget.attrs['autofocus'] = True
        
        #self.fields['usuario_creacion'].widget.attrs['value'] = ''

    class Meta():
        model = Empresas
        fields = '__all__'
        exclude = ['fch_modificacion','usuario_modificacion','usuario_creacion','borrado']

        widgets = {
            'nombre_empresa': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre de la empresa',
                }
            ),
            'descripcion': TextInput(
                attrs={
                    'placeholder': 'Breve descripción del rubro de la empresa',
                }
            ),
            'telefono': TextInput(
                attrs={
                    'placeholder': 'Ingrese el o los números de contacto',
                }
            ),
            'nombre_contacto': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre del contacto directo',
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

class formulario_cliente(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['nombre'].widget.attrs['autofocus'] = True
        
        #self.fields['usuario_creacion'].widget.attrs['value'] = ''

    class Meta():
        model = Clientes
        fields = '__all__'
        exclude = ['fch_modificacion','usuario_modificacion','usuario_creacion','borrado', 'id_empresa','id_usuario']

        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre de la empresa',
                }
            ),
            'identidad': TextInput(
                attrs={
                    'placeholder': 'Ingrese la identidad',
                }
            ),
            'fch_nacimiento': TextInput(
                attrs={
                    'placeholder': 'aaaa/mm/dd',
                }
            ),
            'estado': Select(
                attrs={
                    #'size': '10'
                }
            )
        }

class formulario_cliente_contactos(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['descripcion'].widget.attrs['autofocus'] = True
        
        #self.fields['usuario_creacion'].widget.attrs['value'] = ''

    class Meta():
        model = Contactos
        fields = '__all__'
        exclude = ['fch_modificacion','usuario_modificacion','usuario_creacion','borrado','id_cliente']

        widgets = {
            'descripcion': TextInput(
                attrs={
                    'placeholder': 'Ingrese la descripción de contacto',
                }
            ),
            'comentario': TextInput(
                attrs={
                    'placeholder': 'Si desea ingrese un comentario del contacto',
                }
            ),
            'estado': Select(
                attrs={
                    #'size': '10'
                }
            )
        }

class formulario_cliente_productos(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['descripcion'].widget.attrs['autofocus'] = True
        
        #self.fields['usuario_creacion'].widget.attrs['value'] = ''

    class Meta():
        model = Productos
        fields = '__all__'
        exclude = ['fch_modificacion','usuario_modificacion','usuario_creacion','borrado','id_cliente']

        widgets = {
            'descripcion': TextInput(
                attrs={
                    'placeholder': 'Tarjeta de Crédito/Préstamo Banco/Línea de crédito en casa Comercial/Otros',
                }
            ),
            'numero_producto': TextInput(
                attrs={
                    'placeholder': 'Ingrese el número del producto',
                }
            ),
            'estado': Select(
                attrs={
                    #'size': '10'
                }
            )
        }

class formulario_codigos(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['descripcion'].widget.attrs['autofocus'] = True
        
        #self.fields['usuario_creacion'].widget.attrs['value'] = ''

    class Meta():
        model = Codigos
        fields = '__all__'
        exclude = ['fch_modificacion','usuario_modificacion','usuario_creacion','borrado','id_cliente']

        widgets = {
            'descripcion': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre del código',
                }
            ),
            'estado': Select(
                attrs={
                    #'size': '10'
                }
            )
        }

class formulario_motivos(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['descripcion'].widget.attrs['autofocus'] = True
        
        #self.fields['usuario_creacion'].widget.attrs['value'] = ''

    class Meta():
        model = Motivos
        fields = '__all__'
        exclude = ['fch_modificacion','usuario_modificacion','usuario_creacion','borrado']

        widgets = {
            'descripcion': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre del código',
                }
            ),
            'estado': Select(
                attrs={
                    #'size': '10'
                }
            )
        }

class formulario_gestion(Form):
    #codigoanidado = ModelChoiceField(queryset=Codigos.objects.filter(borrado=0,estado=1),widget=Select(attrs={'class': 'form-control select2'}))
    #motivoanidado = ModelChoiceField(queryset=Motivos.objects.none(), widget=Select(attrs={'class': 'form-control select2'}))

    codigoanidado = ModelChoiceField(queryset=Codigos.objects.filter(borrado=0,estado=1),widget=Select(attrs={'class': 'form-control '}))
    motivoanidado = ModelChoiceField(queryset=Motivos.objects.none(), widget=Select(attrs={'class': 'form-control '}))

class formualario_guardar_gestion(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['descripcion'].widget.attrs['autofocus'] = True


    class Meta():
        model = Gestiones
        fields = '__all__'
        exclude = ['fch_modificacion','usuario_modificacion','usuario_creacion','borrado','estado']

        widgets = {
            'descripcion': Textarea(
                attrs={
                    'placeholder': 'Ingrese la nueva gestión',
                    'rows': '2',
                    #'font-size': '8px',
                    #'cols': '5',
                    #'style': 'width: 150%;',
        


                }
            ),
        }

class formulario_alertas(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['descripcion_alerta'].widget.attrs['autofocus'] = True
        #self.fields['fch_recordatorio'].widget = widgets.AdminSplitDateTime()
        
        #self.fields['usuario_creacion'].widget.attrs['value'] = ''

    class Meta():
        model = Recordatorios
        fields = '__all__'
        exclude = ['id_cliente','fch_modificacion','usuario_modificacion','usuario_creacion','borrado','estado']

        widgets = {
            'descripcion_alerta': TextInput(attrs={'placeholder': 'Ingrese una breve descripción', }),
     
        }

class formulario_seg_promesas(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['valor'].widget.attrs['autofocus'] = True
        
        #self.fields['usuario_creacion'].widget.attrs['value'] = ''

    class Meta():
        model = Promesas
        fields = '__all__'
        exclude = ['fch_modificacion','usuario_modificacion','usuario_creacion','borrado','estado','id_usuario','fecha','hora','descripcion', 'id_cliente','motivo_descrip']

class formulario_seg_visitas(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['respuesta_visita'].widget.attrs['autofocus'] = True
        
        #self.fields['usuario_creacion'].widget.attrs['value'] = ''

    class Meta():
        model = Visitas
        fields = '__all__'
        exclude = ['fch_modificacion','usuario_modificacion','usuario_creacion','borrado','estado','id_usuario','fch_creacion','lugar','fch_visita_realizada', 'id_cliente','motivo_descrip']


        widgets = {
            'respuesta_visita': Textarea(
                attrs={
                    'placeholder': 'Ingrese la respuesta de la visita realizada',
                    'rows': '4',
                }
            ),
        }

class formulario_seg_alertas(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        #self.fields['descri'].widget.attrs['autofocus'] = True
        
        #self.fields['usuario_creacion'].widget.attrs['value'] = ''

    class Meta():
        model = Recordatorios
        fields = '__all__'
        exclude = ['fch_modificacion','usuario_modificacion','usuario_creacion','borrado','estado','id_usuario','fch_creacion', 'id_cliente','fch_recordatorio','hora_recordatorio']

