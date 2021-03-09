from app.cobros.models import Departamentos,Puestos,Recordatorios,Promesas
from datetime import datetime

class alertas():
    def recordatorios(objeto,user_creacion):
        now = datetime.now()
        cont_rcrio = 0
        if len(str(now.month)) == 1:
            mes = '0' + str(now.month)
        else:
            mes = str(now.month)
        fecha = str(now.year) + '-' + mes + '-' + str(now.day)
        recordatorios = Recordatorios.objects.filter(borrado=0,usuario_creacion= user_creacion,estatus_alerta='Pendiente',fch_recordatorio=fecha)
        for x in recordatorios:
            cont_rcrio += 1
        return cont_rcrio 

    def promesas(objeto,user_creacion):
        cont_promesa = 0
        now = datetime.now()
        cont_rcrio = 0
        if len(str(now.month)) == 1:
            mes = '0' + str(now.month)
        else:
            mes = str(now.month)
        fecha = str(now.year) + '-' + mes + '-' + str(now.day)
        promesa = Promesas.objects.filter(borrado=0,id_usuario=user_creacion,estatus_promesa='Pendiente',fecha=fecha)
        for x in promesa:
            cont_promesa += 1
        return cont_promesa 
        #context['cont_total'] = cont_promesa + cont_rcrio