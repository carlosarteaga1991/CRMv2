
from django.db import models
from django.forms import model_to_dict
from app.usuario.models import Usuario


class Departamentos(models.Model):
    id_departamento = models.AutoField(primary_key=True)
    nombre = models.CharField('Nombre',max_length=100, unique=True)
    fch_creacion = models.DateTimeField(auto_now_add=True)
    usuario_creacion = models.IntegerField(blank=True,null=True)
    fch_modificacion = models.CharField(max_length=35, blank=True)
    usuario_modificacion = models.IntegerField(blank=True,null=True)
    estado = models.CharField(max_length=1, default='1',choices=[('1','Activo'),('2','Inactivo')])
    borrado = models.CharField(max_length=1, default='0',choices=[('1','Si'),('0','No')])

    def __str__(self):
        return self.nombre
    
    def toJSON(self): #función para crear diccionarios que se envían en la vista
        item = model_to_dict(self, exclude=['usuario_modificacion']) # si deseamos excluir ciertos parámetros usamos  como atributo ,exclude['']
        return item

    class Meta:
        verbose_name_plural = "Departamentos"
        ordering = ['id_departamento']

class Puestos(models.Model):
    id_puesto = models.AutoField(primary_key=True)
    id_departamento = models.ForeignKey(Departamentos, on_delete=models.PROTECT) #protege en caso de querer borrar
    nombre = models.CharField(max_length=100)
    fch_creacion = models.DateTimeField(auto_now_add=True)
    usuario_creacion = models.IntegerField(blank=True,null=True)
    fch_modificacion = models.CharField(max_length=35, blank=True)
    usuario_modificacion = models.IntegerField(blank=True,null=True)
    estado = models.CharField(max_length=1, default='1',choices=[('1','Activo'),('2','Inactivo')])
    borrado = models.CharField(max_length=1, default='0',choices=[('1','Si'),('0','No')])

    def __str__(self):
        return self.nombre
    
    def toJSON(self): #función para crear diccionarios que se envían en la vista
        item = model_to_dict(self, exclude=['usuario_modificacion']) # si deseamos excluir ciertos parámetros usamos  como atributo ,exclude['']
        return item

    class Meta:
        verbose_name_plural = "Puestos" #para que no le agrega una ese en el admin panel de django
        ordering = ['id_puesto']


class Empresas(models.Model):
    id_empresa = models.AutoField(primary_key=True)
    nombre_empresa = models.CharField("Nombre de la empresa",max_length=120, unique=True)
    descripcion = models.CharField("Descripción",max_length=450,blank=True)
    telefono = models.CharField("Teléfono",max_length=50, blank=True)
    nombre_contacto = models.CharField("Nombre del contacto",max_length=80,blank=True)
    fch_creacion = models.DateTimeField(auto_now_add=True)
    usuario_creacion = models.IntegerField(blank=True,null=True)
    fch_modificacion = models.CharField(max_length=35, blank=True)
    usuario_modificacion = models.IntegerField(blank=True,null=True)
    estado = models.CharField(max_length=1, default='1',choices=[('1','Activo'),('2','Inactivo')])
    borrado = models.CharField(max_length=1, default='0',choices=[('1','Si'),('0','No')])

    def __str__(self):
        return self.nombre_empresa 
    
    def toJSON(self): #función para crear diccionarios que se envían en la vista
        item = model_to_dict(self, exclude=['usuario_modificacion']) # si deseamos excluir ciertos parámetros usamos  como atributo ,exclude['']
        return item
    
    class Meta:
        verbose_name_plural = 'Empresas'
        ordering = ['id_empresa']

class Clientes(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    id_empresa = models.ForeignKey(Empresas,on_delete=models.PROTECT,verbose_name="Empresa")
    id_usuario = models.ForeignKey(Usuario,on_delete=models.PROTECT,verbose_name="Usuario")
    nombre = models.CharField("Nombre del cliente",max_length=150)
    tipo_id = models.CharField('Tipo de Identificación',max_length=1,default='1',choices= 
    [('1','Cédula de Identidad'),
     ('2','RTN'), 
     ('3','Otro')])
    identidad = models.CharField(max_length=30,blank=True)
    fch_nacimiento = models.CharField("Fecha de nacimiento",max_length=30,blank=True)
    estado_civil = models.CharField(max_length=12, default='Soltero',choices=[('Soltero','Soltero'),('Casado','Casado'),('Unión Libre','Unión Libre')])
    fch_creacion = models.DateTimeField(auto_now_add=True)
    usuario_creacion = models.IntegerField(blank=True,null=True)
    fch_modificacion = models.CharField(max_length=35, blank=True)
    usuario_modificacion = models.IntegerField(blank=True,null=True)
    estado = models.CharField(max_length=1, default='1',choices=[('1','Activo'),('2','Inactivo')])
    borrado = models.CharField(max_length=1, default='0',choices=[('1','Si'),('0','No')])

    def __str__(self):
        return self.nombre 
    
    def toJSON(self): #función para crear diccionarios que se envían en la vista
        item = model_to_dict(self, exclude=['usuario_modificacion']) # si deseamos excluir ciertos parámetros usamos  como atributo ,exclude['']
        return item
    
    class Meta:
        verbose_name_plural = 'Clientes'
        ordering = ['nombre']

class Contactos(models.Model):
    id_contacto = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Clientes,on_delete=models.PROTECT)
    tipo_contacto = models.CharField(max_length=35,default='Teléfono', 
    choices=[
        ('Teléfono Trabajo','Teléfono Trabajo'),
        ('Teléfono Casa','Teléfono Casa'),
        ('Celular','Celular'),
        ('Dirección Casa','Dirección Casa'),
        ('Dirección Trabajo','Dirección Trabajo'),
        ('Correo','Correo')])
    descripcion = models.TextField()
    comentario = models.CharField(max_length=200)
    fch_creacion = models.DateTimeField(auto_now_add=True)
    usuario_creacion = models.IntegerField(blank=True,null=True)
    fch_modificacion = models.CharField(max_length=35, blank=True)
    usuario_modificacion = models.IntegerField(blank=True,null=True)
    estado = models.CharField(max_length=1, default='1',choices=[('1','Activo'),('2','Inactivo')])
    borrado = models.CharField(max_length=1, default='0',choices=[('1','Si'),('0','No')])

    def __str__(self):
        return 'El cliente %s tiene un(a) %s , y su descripción es: %s' % (self.id_cliente,self.tipo_contacto,self.descripcion)
    
    def toJSON(self): #función para crear diccionarios que se envían en la vista
        item = model_to_dict(self, exclude=['usuario_modificacion']) # si deseamos excluir ciertos parámetros usamos  como atributo ,exclude['']
        return item
    
    class Meta:
        verbose_name_plural = 'Contactos Cliente'
        ordering = ['tipo_contacto']

class Productos(models.Model):
    id_producto = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Clientes,on_delete=models.PROTECT)
    descripcion = models.TextField()
    numero_producto = models.CharField(max_length=50)
    dias_mora = models.IntegerField()
    saldo_total = models.DecimalField(max_digits=19, decimal_places=2)
    capital = models.DecimalField(max_digits=19, decimal_places=2)
    intereses = models.DecimalField(max_digits=19, decimal_places=2)
    fch_creacion = models.DateTimeField(auto_now_add=True)
    usuario_creacion = models.IntegerField(blank=True,null=True)
    fch_modificacion = models.CharField(max_length=35, blank=True)
    usuario_modificacion = models.IntegerField(blank=True,null=True)
    estado = models.CharField(max_length=1, default='1',choices=[('1','Activo'),('2','Inactivo')])
    borrado = models.CharField(max_length=1, default='0',choices=[('1','Si'),('0','No')])

    def __str__(self):
        return 'El cliente %s , Con número de producto: %s tiene un saldo total de %s lempiras' % (self.id_cliente,self.numero_producto,self.saldo_total)
    
    def toJSON(self): #función para crear diccionarios que se envían en la vista
        item = model_to_dict(self, exclude=['usuario_modificacion']) # si deseamos excluir ciertos parámetros usamos  como atributo ,exclude['']
        return item
    
    class Meta:
        verbose_name_plural = 'Productos Cliente'
        ordering = ['descripcion']

class Recordatorios(models.Model):
    id_recordatorio = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Clientes,on_delete=models.PROTECT)
    fch_recordatorio = models.DateField()
    hora_recordatorio = models.TimeField(default="00:00:00")
    descripcion_alerta = models.CharField(max_length=100, blank=True, null=True)
    fch_creacion = models.DateTimeField(auto_now_add=True)
    usuario_creacion = models.ForeignKey(Usuario,on_delete=models.PROTECT,verbose_name="Usuario")
    fch_modificacion = models.CharField(max_length=35, blank=True)
    usuario_modificacion = models.IntegerField(blank=True,null=True)
    estado = models.CharField(max_length=1, default='1',choices=[('1','Activo'),('2','Inactivo')])
    borrado = models.CharField(max_length=1, default='0',choices=[('1','Si'),('0','No')])

    def __str__(self):
        return 'El cliente %s Recordatorio para el %s a las %s' % (self.id_cliente, self.fch_recordatorio,self.hora_recordatorio)
    
    def toJSON(self): 
        item = model_to_dict(self, exclude=['usuario_modificacion'])
        return item
    
    class Meta:
        verbose_name_plural = 'Recordatorios Cliente'
        ordering = ['id_cliente']

class Codigos(models.Model):
    id_codigo = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50, unique=True)
    fch_creacion = models.DateTimeField(auto_now_add=True)
    usuario_creacion = models.IntegerField(blank=True,null=True)
    fch_modificacion = models.CharField(max_length=35, blank=True)
    usuario_modificacion = models.IntegerField(blank=True,null=True)
    estado = models.CharField(max_length=1, default='1',choices=[('1','Activo'),('2','Inactivo')])
    borrado = models.CharField(max_length=1, default='0',choices=[('1','Si'),('0','No')])

    def __str__(self):
        return self.descripcion
    
    def toJSON(self): #función para crear diccionarios que se envían en la vista
        item = model_to_dict(self, exclude=['usuario_modificacion']) # si deseamos excluir ciertos parámetros usamos  como atributo ,exclude['']
        return item
    
    class Meta:
        verbose_name_plural = 'Códigos'
        ordering = ['id_codigo']

class Motivos(models.Model):
    id_motivo = models.AutoField(primary_key=True)
    id_codigo = models.ForeignKey(Codigos,on_delete=models.PROTECT)
    descripcion = models.CharField(max_length=50, unique=True)
    fch_creacion = models.DateTimeField(auto_now_add=True)
    usuario_creacion = models.IntegerField(blank=True,null=True)
    fch_modificacion = models.CharField(max_length=35, blank=True)
    usuario_modificacion = models.IntegerField(blank=True,null=True)
    estado = models.CharField(max_length=1, default='1',choices=[('1','Activo'),('2','Inactivo')])
    borrado = models.CharField(max_length=1, default='0',choices=[('1','Si'),('0','No')])

    def __str__(self):
        return self.descripcion
    
    def toJSON(self): #función para crear diccionarios que se envían en la vista
        item = model_to_dict(self, exclude=['usuario_modificacion']) # si deseamos excluir ciertos parámetros usamos  como atributo ,exclude['']
        return item
    
    class Meta:
        verbose_name_plural = 'Motivos'
        ordering = ['id_motivo']

class Gestiones(models.Model):
    id_gestion = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Clientes, on_delete=models.PROTECT)
    id_codigo = models.ForeignKey(Codigos,on_delete=models.PROTECT)
    id_motivo = models.ForeignKey(Motivos,on_delete=models.PROTECT)
    fch_gestion = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField()
    usuario_creacion = models.ForeignKey(Usuario,on_delete=models.PROTECT,verbose_name="Usuario")
    fch_modificacion = models.CharField(max_length=35, blank=True)
    usuario_modificacion = models.IntegerField(blank=True,null=True)
    estado = models.CharField(max_length=1, default='1',choices=[('1','Activo'),('2','Inactivo')])
    borrado = models.CharField(max_length=1, default='0',choices=[('1','Si'),('0','No')])
    
    def __str__(self):
        return 'El cliente %s tiene una gestión el: %s' % (self.id_cliente ,self.fch_gestion)
    
    def toJSON(self): #función para crear diccionarios que se envían en la vista
        item = model_to_dict(self, exclude=['usuario_modificacion']) # si deseamos excluir ciertos parámetros usamos  como atributo ,exclude['']
        return item
    
    class Meta:
        verbose_name_plural = 'Gestiones'
        ordering = ['-fch_gestion']

class Promesas(models.Model):
    id_promesa = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Clientes,on_delete=models.PROTECT)
    id_usuario = models.ForeignKey(Usuario,on_delete=models.PROTECT,verbose_name="Usuario")
    fecha = models.DateField()
    hora = models.TimeField()
    valor = models.DecimalField(max_digits=19, decimal_places=2)
    descripcion = models.TextField()
    motivo_descrip = models.CharField(max_length=20, blank=True, null=True)
    estatus_promesa = models.CharField('Estatus de la Promesa',max_length=11,default='Pendiente',choices=
    [('Pendiente','Pendiente'),
     ('Cumplida','Cumplida'),
     ('Incumplida','Incumplida')])
    fch_creacion = models.DateTimeField(auto_now_add=True)
    descripcion = models.CharField(max_length=600, blank=True)
    usuario_creacion = models.IntegerField(blank=True,null=True)
    fch_modificacion = models.CharField(max_length=35, blank=True)
    usuario_modificacion = models.IntegerField(blank=True,null=True)
    estado = models.CharField(max_length=1, default='1',choices=[('1','Activo'),('2','Inactivo')])
    borrado = models.CharField(max_length=1, default='0',choices=[('1','Si'),('0','No')])

    def __str__(self):
        return 'El cliente %s tiene una promesa para el: %s por un valor de %s lempiras' % (self.id_cliente,self.fecha,self.valor)
    
    def toJSON(self): #función para crear diccionarios que se envían en la vista
        item = model_to_dict(self, exclude=['usuario_modificacion']) # si deseamos excluir ciertos parámetros usamos  como atributo ,exclude['']
        return item
          
    class Meta:
        verbose_name_plural = 'Promesas'
        ordering = ['id_cliente']
    
class Pagos(models.Model):
    id_pago = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Clientes,on_delete=models.PROTECT)
    id_usuario = models.ForeignKey(Usuario,on_delete=models.PROTECT,verbose_name="Usuario")
    fecha = models.DateField()
    valor = models.DecimalField(max_digits=19, decimal_places=2)
    fch_creacion = models.DateTimeField(auto_now_add=True)
    descripcion = models.CharField(max_length=600, blank=True)
    usuario_creacion = models.IntegerField(blank=True,null=True)
    fch_modificacion = models.CharField(max_length=35, blank=True)
    usuario_modificacion = models.IntegerField(blank=True,null=True)
    estado = models.CharField(max_length=1, default='1',choices=[('1','Activo'),('2','Inactivo')])
    borrado = models.CharField(max_length=1, default='0',choices=[('1','Si'),('0','No')])

    def __str__(self):
        return 'Cliente Número: %s, fecha pago: %s, por el valor de: %s Lempiras.' % (self.id_cliente,self.fecha,self.valor)
    
    def toJSON(self): #función para crear diccionarios que se envían en la vista
        item = model_to_dict(self, exclude=['usuario_modificacion']) # si deseamos excluir ciertos parámetros usamos  como atributo ,exclude['']
        return item
    
    class Meta:
        verbose_name_plural = 'Pagos'
        ordering = ['fecha']

class Visitas(models.Model):
    id_visita = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Clientes,on_delete=models.PROTECT)
    id_usuario = models.ForeignKey(Usuario,on_delete=models.PROTECT,verbose_name="Usuario")
    fch_creacion = models.DateTimeField(auto_now_add=True)
    fch_visita_realizada = models.DateField(blank=True, null=True)
    lugar = models.CharField(max_length=1500, blank=True)
    motivo_descrip = models.CharField(max_length=20, blank=True, null=True)
    respuesta_visita = models.CharField(max_length=1500, blank=True)
    estatus_visita = models.CharField('Estatus de la Visita',max_length=25,default='Pendiente',choices=
    [('Pendiente','Pendiente'),
     ('Localizado sin Promesa','Localizado sin Promesa'),
     ('Localizado con Promesa','Localizado con Promesa'),
     ('Dirección Incorrecta','Dirección Incorrecta')])
    usuario_creacion = models.IntegerField(blank=True,null=True)
    fch_modificacion = models.CharField(max_length=35, blank=True)
    usuario_modificacion = models.IntegerField(blank=True,null=True)
    estado = models.CharField(max_length=1, default='1',choices=[('1','Activo'),('2','Inactivo')])
    borrado = models.CharField(max_length=1, default='0',choices=[('1','Si'),('0','No')])

    def __str__(self):
        return self.lugar
    
    def toJSON(self): #función para crear diccionarios que se envían en la vista
        item = model_to_dict(self, exclude=['usuario_modificacion']) # si deseamos excluir ciertos parámetros usamos  como atributo ,exclude['']
        return item
    
    class Meta:
        verbose_name_plural = 'Visitas'
        ordering = ['id_cliente']

class LogCobros(models.Model):
    id_log = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(Usuario,on_delete=models.PROTECT,default=1,verbose_name="Usuario")
    nombre_tabla = models.CharField(max_length=35)
    fecha = models.DateTimeField(auto_now_add=True)
    id_registro = models.IntegerField(blank=True,null=True)
    tipo_accion = models.CharField('Tipo de Acción',max_length=35,choices=
    [('Insertar','Insertar'),('Modificar','Modificar'),('Seleccionar','Seleccionar'),('Borrar','Borrar')])
    Dato_anterior = models.CharField(max_length=400,blank=True)
    Dato_despues = models.CharField(max_length=400,blank=True)
    campo_afectado = models.CharField(max_length=35,blank=True)

    def __str__(self):
        return self.nombre_tabla
    
    def toJSON(self): #función para crear diccionarios que se envían en la vista
        item = model_to_dict(self) # si deseamos excluir ciertos parámetros usamos  como atributo ,exclude['']
        return item
    
    class Meta:
        verbose_name_plural = 'Bitácora App Cobros'
        ordering = ['fecha']
    