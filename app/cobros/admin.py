from django.contrib import admin
from app.cobros.models import Puestos, Departamentos, Empresas, Clientes, Contactos, Productos, Recordatorios, Codigos, Motivos, Gestiones, Promesas, Pagos, LogCobros
from app.usuario.models import Usuario



#para agregar filtros en el panel de administración
class filtroDepartamentos(admin.ModelAdmin):
    list_display = ("nombre","usuario_creacion","estado") # esto para mostrar sólo algunos campos
    # y se agrega al admin.site.register
    # y para agregar los filtros de busqueda se colocan los campos q se desan hacer búsqueda
    search_fields = ("nombre","usuario_creacion","estado")

admin.site.register(Usuario)

admin.site.register(Puestos)
admin.site.register(Departamentos, filtroDepartamentos)
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
