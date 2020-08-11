from django.db import models
from django.forms import model_to_dict

# Creación de modelos para la versión de prueba número dos
# fecha: 10 de agosto del 2020


class Departamentos(models.Model):
    id_departamento = models.AutoField(primary_key=True)
    nombre = models.CharField('Nombre',max_length=100, unique=True)
    fch_creacion = models.DateTimeField(auto_now_add=True)
    usuario_creacion = models.IntegerField()
    fch_modificacion = models.CharField(max_length=35, blank=True)
    usuario_modificacion = models.IntegerField(blank=True,null=True)
    estado = models.CharField(max_length=1, default='1',choices=[('1','Activo'),('2','Inactivo')])

    def __str__(self):
        return self.nombre
    
    def toJSON(self): #función para crear diccionarios
        item = model_to_dict(self)
        return item


    class Meta:
        verbose_name_plural = "Departamentos"
        ordering = ['id_departamento']

class Puestos(models.Model):
    id_puesto = models.AutoField(primary_key=True)
    id_departamento = models.ForeignKey(Departamentos, on_delete=models.PROTECT) #protege en caso de querer borrar
    nombre = models.CharField(max_length=100)
    fch_creacion = models.DateTimeField(auto_now_add=True)
    usuario_creacion = models.IntegerField()
    fch_modificacion = models.CharField(max_length=35, blank=True)
    usuario_modificacion = models.IntegerField(blank=True,null=True)
    estado = models.CharField(max_length=1, default='1',choices=[('1','Activo'),('2','Inactivo')])

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Puestos" #para que no le agrega una ese en el admin panel de django
        ordering = ['id_puesto']

class Usuarios(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    primer_nombre = models.CharField('Primer Nombre',max_length=35)
    segundo_nombre = models.CharField('Segundo Nombre',max_length=35,blank=True) # verificar si no es obligatorio sino agregar, null=True
    primer_apellido = models.CharField('Primer Apellido',max_length=35)
    segundo_apellido = models.CharField('Segundo Apellido',max_length=35, blank=True)
    Fch_ingreso_labores = models.CharField(max_length=25, blank=True)
    usuario = models.CharField('Usuario',max_length=20, unique=True)#help_text="Ejemplo: nombre.apellido"
    correo = models.EmailField('Email')
    telefono = models.IntegerField('Teléfono')
    id_departamento = models.ForeignKey(Departamentos, on_delete=models.PROTECT)#,'Departamento Asigando'
    id_puesto = models.ForeignKey(Puestos, on_delete=models.PROTECT)#,'Puesto a Desempeñar'
    fch_ultimo_acceso = models.CharField(max_length=35,blank=True)
    ip_ultimo_acceso = models.CharField(max_length=50, blank=True)
    fch_creacion = models.DateTimeField(auto_now_add=True)
    usuario_creacion = models.IntegerField(blank=True, null=True)
    fch_modificacion = models.CharField(max_length=35, blank=True)
    usuario_modificacion = models.IntegerField(blank=True,null=True)
    estado = models.CharField('Estado',max_length=1, default='1',choices=[('1','Activo'),('2','Inactivo')])

    def __str__(self):
        return self.primer_nombre + " " + self.segundo_nombre + " " + self.primer_apellido + " " + self.segundo_apellido

    def toJSON(self):
        item = model_to_dict(self)
        return item

    
    class Meta:
        verbose_name_plural = "Usuarios"
        ordering = ['primer_nombre']


class Empresas(models.Model):
    id_empresa = models.AutoField(primary_key=True)
    nombre_empresa = models.CharField(max_length=120)
    descripcion = models.CharField(max_length=450,blank=True)
    telefono = models.CharField(max_length=50, blank=True)
    nombre_contacto = models.CharField(max_length=80,blank=True)
    fch_creacion = models.DateTimeField(auto_now_add=True)
    usuario_creacion = models.IntegerField()
    fch_modificacion = models.CharField(max_length=35, blank=True)
    usuario_modificacion = models.IntegerField(blank=True,null=True)
    estado = models.CharField(max_length=1, default='1',choices=[('1','Activo'),('2','Inactivo')])

    def __str__(self):
        return self.nombre_empresa 
    
    class Meta:
        verbose_name_plural = 'Empresas'
        ordering = ['id_empresa']

class Clientes(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    id_empresa = models.ForeignKey(Empresas,on_delete=models.PROTECT)
    id_usuario = models.ForeignKey(Usuarios,on_delete=models.PROTECT)
    nombre = models.CharField(max_length=150)
    tipo_id = models.CharField('Tipo de Identificación',max_length=1,default='1',choices= 
    [('1','Cédula de Identidad'),
     ('2','RTN'), 
     ('3','Otro')])
    identidad = models.CharField(max_length=30,blank=True)
    fch_nacimiento = models.CharField(max_length=30,blank=True)
    fch_creacion = models.DateTimeField(auto_now_add=True)
    usuario_creacion = models.IntegerField()
    fch_modificacion = models.CharField(max_length=35, blank=True)
    usuario_modificacion = models.IntegerField(blank=True,null=True)
    estado = models.CharField(max_length=1, default='1',choices=[('1','Activo'),('2','Inactivo')])

    def __str__(self):
        return self.nombre 
    
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
    usuario_creacion = models.IntegerField()
    fch_modificacion = models.CharField(max_length=35, blank=True)
    usuario_modificacion = models.IntegerField(blank=True,null=True)
    estado = models.CharField(max_length=1, default='1',choices=[('1','Activo'),('2','Inactivo')])

    def __str__(self):
        return 'El cliente %s tiene un(a) %s , y su descripción es: %s' % (self.id_cliente,self.tipo_contacto,self.descripcion)
    
    class Meta:
        verbose_name_plural = 'Contactos Cliente'
        ordering = ['tipo_contacto']

class Productos(models.Model):
    id_producto = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Clientes,on_delete=models.PROTECT)
    descripcion = models.TextField()
    numero_producto = models.CharField(max_length=50)
    dias_mora = models.IntegerField()
    saldo_total = models.IntegerField()
    capital = models.IntegerField()
    intereses = models.IntegerField()
    fch_creacion = models.DateTimeField(auto_now_add=True)
    usuario_creacion = models.IntegerField()
    fch_modificacion = models.CharField(max_length=35, blank=True)
    usuario_modificacion = models.IntegerField(blank=True,null=True)
    estado = models.CharField(max_length=1, default='1',choices=[('1','Activo'),('2','Inactivo')])

    def __str__(self):
        return 'El cliente %s , Con número de producto: %s tiene un saldo total de %s lempiras' % (self.id_cliente,self.numero_producto,self.saldo_total)
    
    class Meta:
        verbose_name_plural = 'Productos Cliente'
        ordering = ['descripcion']

class Recordatorios(models.Model):
    id_recordatorio = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Clientes,on_delete=models.PROTECT)
    fch_recordatorio = models.DateField()
    hora_recordatorio = models.TimeField()
    descripción = models.TextField()
    fch_creacion = models.DateTimeField(auto_now_add=True)
    usuario_creacion = models.IntegerField()
    fch_modificacion = models.CharField(max_length=35, blank=True)
    usuario_modificacion = models.IntegerField(blank=True,null=True)
    estado = models.CharField(max_length=1, default='1',choices=[('1','Activo'),('2','Inactivo')])

    def __str__(self):
        return 'El cliente %s Recordatorio para el %s a las %s' % (self.id_cliente, self.fch_recordatorio,self.hora_recordatorio)
    
    class Meta:
        verbose_name_plural = 'Recordatorios Cliente'
        ordering = ['id_cliente']

class Codigos(models.Model):
    id_codigo = models.AutoField(primary_key=True)
    descripción = models.CharField(max_length=100)
    fch_creacion = models.DateTimeField(auto_now_add=True)
    usuario_creacion = models.IntegerField()
    fch_modificacion = models.CharField(max_length=35, blank=True)
    usuario_modificacion = models.IntegerField(blank=True,null=True)
    estado = models.CharField(max_length=1, default='1',choices=[('1','Activo'),('2','Inactivo')])

    def __str__(self):
        return self.descripción
    
    class Meta:
        verbose_name_plural = 'Códigos'
        ordering = ['id_codigo']

class Motivos(models.Model):
    id_motivo = models.AutoField(primary_key=True)
    id_codigo = models.ForeignKey(Codigos,on_delete=models.PROTECT)
    descripción = models.CharField(max_length=100)
    fch_creacion = models.DateTimeField(auto_now_add=True)
    usuario_creacion = models.IntegerField()
    fch_modificacion = models.CharField(max_length=35, blank=True)
    usuario_modificacion = models.IntegerField(blank=True,null=True)
    estado = models.CharField(max_length=1, default='1',choices=[('1','Activo'),('2','Inactivo')])

    def __str__(self):
        return self.descripción
    
    class Meta:
        verbose_name_plural = 'Motivos'
        ordering = ['id_motivo']

class Gestiones(models.Model):
    id_gestion = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Clientes, on_delete=models.PROTECT)
    id_usuario = models.ForeignKey(Usuarios,on_delete=models.PROTECT)
    id_codigo = models.ForeignKey(Codigos,on_delete=models.PROTECT)
    id_motivo = models.ForeignKey(Motivos,on_delete=models.PROTECT)
    fch_gestion = models.DateTimeField(auto_now_add=True)
    fch_creacion = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField()
    usuario_creacion = models.IntegerField()
    fch_modificacion = models.CharField(max_length=35, blank=True)
    usuario_modificacion = models.IntegerField(blank=True,null=True)
    estado = models.CharField(max_length=1, default='1',choices=[('1','Activo'),('2','Inactivo')])
    
    def __str__(self):
        return 'El cliente %s tiene una gestión el: %s' % (self.id_cliente ,self.fch_gestion)
    
    class Meta:
        verbose_name_plural = 'Gestiones'
        ordering = ['fch_gestion']

class Promesas(models.Model):
    id_promesa = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Clientes,on_delete=models.PROTECT)
    id_usuario = models.ForeignKey(Usuarios,on_delete=models.PROTECT)
    fecha = models.DateField()
    hora = models.TimeField()
    valor = models.IntegerField()
    descripcion = models.TextField()
    estatus_promesa = models.CharField('Estatus de la Promesa',max_length=1,default='1',choices=
    [('1','Pendiente'),
     ('2','Cumplida'),
     ('3','Incumplida')])
    fch_creacion = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField()
    usuario_creacion = models.IntegerField()
    fch_modificacion = models.CharField(max_length=35, blank=True)
    usuario_modificacion = models.IntegerField(blank=True,null=True)
    estado = models.CharField(max_length=1, default='1',choices=[('1','Activo'),('2','Inactivo')])

    def __str__(self):
        return 'El cliente %s tiene una promesa para el: %s por un valor de %s lempiras' % (self.id_cliente,self.fecha,self.valor)
          
    class Meta:
        verbose_name_plural = 'Promesas'
        ordering = ['id_cliente']
    
class Pagos(models.Model):
    id_pago = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Clientes,on_delete=models.PROTECT)
    id_usuario = models.ForeignKey(Usuarios,on_delete=models.PROTECT)
    id_promesa = models.ForeignKey(Promesas,on_delete=models.PROTECT, null=True)
    fecha = models.DateField()
    valor = models.IntegerField()
    descripcion = models.TextField()
    fch_creacion = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField()
    usuario_creacion = models.IntegerField()
    fch_modificacion = models.CharField(max_length=35, blank=True)
    usuario_modificacion = models.IntegerField(blank=True,null=True)
    estado = models.CharField(max_length=1, default='1',choices=[('1','Activo'),('2','Inactivo')])

    def __str__(self):
        return 'Cliente Número: %s, fecha pago: %s, por el valor de: %s Lempiras.' % (self.id_cliente,self.fecha,self.valor)
    
    class Meta:
        verbose_name_plural = 'Pagos'
        ordering = ['id_cliente']

class LogCobros(models.Model):
    id_log = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Clientes,on_delete=models.PROTECT)
    nombre_tabla = models.CharField(max_length=35)
    fecha = models.DateTimeField(auto_now_add=True)
    id_registro = models.IntegerField(blank=True,null=True)
    tipo_accion = models.CharField('Tipo de Acción',max_length=35,choices=
    [('Insertar','Insertar'),('Modificar','Modificar'),('Seleccionar','Seleccionar'),('Borrar','Borrar')])
    Dato_anterior = models.CharField(max_length=400,blank=True)
    Dato_despues = models.CharField(max_length=400,blank=True)
    campo_afectado = models.CharField(max_length=35,blank=True)

    def __str__(self):
        return 'Cliente Número: %s, tabla afectada: %s' %( self.id_cliente,self.nombre_tabla)
    
    class Meta:
        verbose_name_plural = 'Bitácora App Cobros'
        ordering = ['fecha']
    






