from django.forms import *
from app.cobros.models import Departamentos

class form_departamento(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Departamentos
        fields = '__all__'
        # si deseo excluir ciertos campos coloco
        exclude = ['fch_modificacion','usuario_modificacion','borrado']

        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            ),

            'usuario_creacion': TextInput(
                attrs={
                    'placeholder': 'user',
                }
            ),

            'estado': Select(
                attrs={
                    #'size': '10'
                }
            )

        }
