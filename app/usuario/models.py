from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class Roles(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre = models.CharField('Nombre',max_length=50, unique=True)
    tiene_permisos = models.CharField(max_length=2, default='No',choices=[('Si','Si'),('No','No')])
    fch_creacion = models.DateTimeField(auto_now_add=True)
    usuario_creacion = models.IntegerField(blank=True,null=True)
    fch_modificacion = models.CharField(max_length=35, blank=True)
    usuario_modificacion = models.IntegerField(blank=True,null=True)
    estado = models.CharField(max_length=1, default='1',choices=[('1','Activo'),('2','Inactivo')])
    borrado = models.CharField(max_length=1, default='0',choices=[('1','Si'),('0','No')])

    def __str__(self):
        return self.nombre
    
    def toJSON(self): 
        item = model_to_dict(self, exclude=['usuario_modificacion'])
        return item

    class Meta:
        verbose_name_plural = "Roles"
        ordering = ['id_rol']

class UsuarioManager(BaseUserManager):
    def create_user(self,email,username,nombres,id_departamento,id_puesto,password = None):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')
        
        user = self.model(
            username = username,
            email = self.normalize_email(email),
            nombres = nombres,
            id_departamento = int(id_departamento),
            id_puesto = int(id_puesto)
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,username,email,nombres,password,id_departamento,id_puesto):
        user = self.create_user(
            email,
            username = username,
            nombres = nombres,
            password = password,
            id_departamento = int(id_departamento),
            id_puesto = int(id_puesto)
        )
        user.usuario_administrador = True
        user.save()
        return user

class Usuario(AbstractBaseUser):
    username = models.CharField('Usuario',max_length=20, unique=True)
    email = models.EmailField('Correo Electrónico', max_length=70,unique=True)
    nombres = models.CharField('Nombres',max_length=30,blank= True, null = True)
    apellidos = models.CharField('Apellidos',max_length=30,blank= True, null = True)
    id_departamento = models.IntegerField("Departamento",blank=True, null=True)
    id_puesto = models.IntegerField("Puesto",blank=True, null=True)
    ip_ultimo_acceso = models.CharField(max_length=50, blank=True)
    usuario_creacion = models.IntegerField(blank=True, null=True)
    fch_creacion = models.DateTimeField(auto_now_add=True)
    fch_modificacion = models.CharField(max_length=35, blank=True)
    usuario_modificacion = models.IntegerField(blank=True,null=True)
    estado = models.CharField('Estado',max_length=1, default='1',choices=[('1','Activo'),('2','Inactivo')])
    borrado = models.CharField(max_length=1, default='0',choices=[('1','Si'),('0','No')])
    cambiar_contrasenia = models.CharField(max_length=1, default='1',choices=[('1','Si'),('0','No')])
    bloqueado = models.CharField(max_length=1, default='0',choices=[('1','Bloqueado'),('0','Desbloqueado')])
    usuario_administrador = models.BooleanField(default = False)
    id_rol = models.ForeignKey(Roles,on_delete=models.PROTECT,verbose_name="Perfil de Usuario",null=True)
    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','nombres','id_departamento','id_puesto']

    def __str__(self):
        return self.username
    
    def has_perm(self,perm,obj = None):
        return True
    
    def has_module_perms(self,app_label):
        return True
    
    @property
    def is_staff(self):
        return self.usuario_administrador


class Pantallas(models.Model):
    id_pantalla = models.AutoField(primary_key=True)
    nombre = models.CharField('Pantalla',max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "Pantallas"
        ordering = ['id_pantalla']

class Permisos(models.Model):
    id_permiso = models.AutoField(primary_key=True)
    id_rol = models.ForeignKey(Roles,on_delete=models.PROTECT,verbose_name="Perfil de Usuario")
    pantalla = models.ForeignKey(Pantallas,on_delete=models.PROTECT,verbose_name="Pantalla")
    ver = models.IntegerField(default=1,blank=True,null=True)
    actualizar = models.IntegerField(default=1,blank=True,null=True)
    crear = models.IntegerField(default=1,blank=True,null=True)
    borrar = models.IntegerField(default=1,blank=True,null=True)
    fch_creacion = models.DateTimeField(auto_now_add=True)
    usuario_creacion = models.IntegerField(blank=True,null=True)
    fch_modificacion = models.CharField(max_length=35, blank=True)
    usuario_modificacion = models.IntegerField(blank=True,null=True)
    estado = models.CharField(max_length=1, default='1',choices=[('1','Activo'),('2','Inactivo')])
    borrado = models.CharField(max_length=1, default='0',choices=[('1','Si'),('0','No')])

    def __str__(self):
        return self.pantalla
    
    def toJSON(self): 
        item = model_to_dict(self, exclude=['usuario_modificacion'])
        return item

    class Meta:
        verbose_name_plural = "Permisos"
        ordering = ['id_permiso']

