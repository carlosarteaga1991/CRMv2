from django.views.generic import TemplateView

class dashboard_vista(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['panel'] = 'Panel de Administrador'
        context['plantilla'] = 'Dashboard'
        context['nombre'] = 'carlos arteaga'
        return context