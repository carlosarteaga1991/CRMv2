from django.views.generic import TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin

from app.usuario.permisos import asignar_permiso
from app.usuario.alertas import alertas

class dashboard_vista(LoginRequiredMixin,TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['panel'] = 'Panel de Administrador'
        context['plantilla'] = 'Dashboard'
        context['nombre'] = 'carlos arteaga'
        context['quitar_footer'] = 'si'

        # INICIO VERIFICACIÓN DE PERMISOS 
        context['permisos'] = asignar_permiso().metodo_permiso(28,'ver',int(self.request.user.id_rol_id),self.request.user.usuario_administrador)
        # FIN VERIFICACIÓN DE PERMISOS

        # INICIO PARA RECORDATORIOS HEADER
        context['cont_alerta'] = alertas().recordatorios(self.request.user)
        # FIN PARA RECORDATORIOS HEADER

        # INICIO PARA PROMESAS HEADER
        context['cont_promesa'] = alertas().promesas(self.request.user)
        context['cont_total'] = alertas().promesas(self.request.user) + alertas().recordatorios(self.request.user)
        # FIN PARA PROMESAS HEADER

        return context