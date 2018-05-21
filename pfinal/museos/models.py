from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

#Models provisional
class Museo(models.Model):
    nombre = models.CharField(max_length=32)
    descripcion = models.TextField()
    horario = models.TextField()
    transporte = models.TextField()
    accesibilidad = models.BooleanField(default=False)#Debería cambiarlo a accesibilidad
    url = models.TextField()
    calle = models.CharField(max_length=32)
    numero = models.CharField(max_length=32)
    localidad = models.CharField(max_length=32)
    codigo_postal = models.CharField(max_length=32)
    distrito = models.CharField(max_length=32)
    telefono = models.CharField(max_length=32)
    fax = models.CharField(max_length=32)
    email = models.CharField(max_length=32)
    def __str__(self):
        return self.nombre + ': ' + self.descripcion

class Selec(models.Model):
    usuario = models.ForeignKey(User)
    museo = models.ManyToManyField(Museo)
    fecha = models.DateTimeField(timezone.now())
    def __str__(self):
        return 'Museos de ' + self.usuario.username

class Conf(models.Model):
    usuario = models.OneToOneField(User)
    titulo = models.CharField(max_length = 32,default='')#O menos
    color = models.CharField(max_length = 32,default='gainsboro')
    fuente = models.CharField(max_length = 3,default= '15px')
    def __str__(self):
        return 'Configuraciones de' + self.usuario.username

class Comentario(models.Model):
    autor = models.CharField(max_length = 32)
    texto = models.TextField()
    fecha = models.DateTimeField(timezone.now())
    museo = models.ForeignKey(Museo)
    def __str__(self):
        return self.autor + ': ' + self.texto
