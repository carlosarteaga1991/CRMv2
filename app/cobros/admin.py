from django.contrib import admin
from app.cobros.models import Puestos, Departamentos, Usuarios, Empresas, Clientes, Contactos, Productos, Recordatorios, Codigos, Motivos, Gestiones, Promesas, Pagos, LogCobros

# Register your models here.

admin.site.register(Puestos)
admin.site.register(Departamentos)
admin.site.register(Usuarios)
admin.site.register(Empresas)
admin.site.register(Clientes)
admin.site.register(Contactos)
admin.site.register(Productos)
admin.site.register(Recordatorios)
admin.site.register(Codigos)
admin.site.register(Motivos)
admin.site.register(Gestiones)
admin.site.register(Promesas)
admin.site.register(Pagos)
admin.site.register(LogCobros)
