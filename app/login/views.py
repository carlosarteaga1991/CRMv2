from django.shortcuts import render,redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import FormView
from django.urls import reverse_lazy


class login(LoginView):
    template_name = 'login.html'

    # importante se sobre escribe este método para verificar si está loggeado y si es así redireccionarlo
    # importante recordar q esa URL se configura en setting .py usando LOGIN_REDIRECT_URL = '/cobros/departamento/' si desea volver a loggerse
    def dispatch(self, request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('crm:listar_departamento')
        return super().dispatch(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plantilla'] = 'Login'
        context['btn_cancelar'] = reverse_lazy('principal')
        context['titulo_lista'] = 'Iniciar Sesión'
        context['login_url']= reverse_lazy('inicio_sesion')
        return context

