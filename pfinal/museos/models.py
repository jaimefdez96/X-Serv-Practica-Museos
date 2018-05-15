from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

#Models provisional
class Museo(models.Model):
    nombre = models.CharField(max_length=32)
    distrito = models.CharField(max_length=32)
    descripcion = models.TextField()
    accesible = models.BooleanField(default=False)
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
    titulo = models.CharField(max_length = 32)#O menos
    color = models.CharField(max_length = 32)
    fuente = models.PositiveIntegerField()

class Comentario(models.Model):
    autor = models.CharField(max_length = 32)
    texto = models.TextField()
    fecha = models.DateTimeField(timezone.now())
    museo = models.ForeignKey(Museo)
    def __str__(self):
        return self.autor + ': ' + self.texto
