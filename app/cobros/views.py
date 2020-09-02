from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from app.cobros.models import Departamentos,Clientes

# Create your views here.

def funcion1(request):
    diccionario = {
        'nombre': 'carlos arteaga',
        'telefono': '9660-3244',
        'objeto_departamento': Departamentos.objects.all()
    }
    return render(request, 'home.html', diccionario)

def funcion2(request):
    diccionario = {
        'objeto_cliente': Clientes.objects.all()
    }
    return render(request, 'index2.html', diccionario)