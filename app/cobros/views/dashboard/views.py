from django.views.generic import TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin

class dashboard_vista(LoginRequiredMixin,TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['panel'] = 'Panel de Administrador'
        context['plantilla'] = 'Dashboard'
        context['nombre'] = 'carlos arteaga'
        return context