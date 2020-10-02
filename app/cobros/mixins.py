from django.shortcuts import redirect
from datetime import date,datetime

class IsSuperuserMixin(object):
    def dispatch(self, request,*args,**kwargs):
        if request.user.usuario_administrador:
            return super().dispatch(request,*args,**kwargs)
        return redirect('home')
    # esta clase es buena para dar permisos a obciones que sólo el administrador puede ver como ser visualizar los requerimientos
    # también se le puede agregar diccionarios a get_conbtext_data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nueva_variable'] = date.now()
        return context