from datetime import datetime
from app.usuario.models import Usuario,Roles,Permisos,Pantallas
from django.contrib.auth.models import User


class asignar_permiso():
    def metodo_permiso(objeto,numpantalla, vista, id_rol, es_admin):
        context = {}
        pantalla_actual = int(numpantalla)
        context['pantalla_template'] = vista


        #prueba
        context['numpantalla'] = pantalla_actual
        context['vista'] = vista
        context['id_rol'] = int(id_rol)
        context['es_admin'] = bool(es_admin)
        #prueba

        permisos_usuario = Permisos.objects.filter(id_rol_id = int(id_rol), estado=1, borrado=0, pantalla_id=pantalla_actual)
        permisos_menu = Permisos.objects.filter(id_rol_id = int(id_rol), estado=1, borrado=0) 
        ver = 0
        borrar = 0
        actualizar = 0
        crear = 0
        for x in permisos_usuario:
            if x.ver == 1:
                ver += 1
            if x.actualizar == 1 :
                actualizar += 1
            if x.crear == 1 :
                crear += 1
            if x.borrar == 1 :
                borrar += 1
        context['permisos_usuario'] = permisos_menu
        context['ver_pantalla'] = ver
        context['actualizar_pantalla'] = actualizar
        context['crear_pantalla'] = crear
        context['crear_actualizar'] = crear + actualizar
        context['borrar_pantalla'] = borrar
        context['numero_pantalla'] = pantalla_actual
        context['usuario_administrador'] = bool(es_admin)
        return context