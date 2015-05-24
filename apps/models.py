from django.db import models
import datetime

# Create your models here.

class Actividad(models.Model):
	titulo = models.CharField(max_length=100)
	tipo = models.CharField(max_length=100)
	precio = models.CharField(max_length=32)
	fecha = models.DateField()
	hora = models.TimeField()
	duracion = models.DateTimeField()
	eslargo = models.IntegerField()
	urlinfo = models.TextField()
	fechamod = models.DateTimeField()
	masinfo = models.TextField()
	puntuacion  = models.IntegerField(default = 0)
	

class Actividad_User(models.Model):
	titulo = models.CharField(max_length=100)
	fecha = models.DateField()
	urlinfo = models.TextField()
	fechaadd = models.DateTimeField()
	comentario = models.TextField()

class Variablescss(models.Model):
	user = models.CharField(max_length=32)
	name =  models.CharField(max_length=100)
	colorletra = models.CharField(max_length=32, default = "")
	tamannoletra = models.CharField(max_length=32, default = "")
	colorfondo = models.CharField(max_length=32, default = "")

class Usuario(models.Model):
	user = models.CharField(max_length=32)
	title = models.CharField(max_length=100)
	descripcion = models.TextField()
	actividades = models.ManyToManyField(Actividad_User)
	css = models.ManyToManyField(Variablescss)

class Comentario(models.Model):
	tituloactividad = models.CharField(max_length=100)
	comentario = models.TextField()


class Comments(models.Model):
	user = models.CharField(max_length=32)
	titulo = models.CharField(max_length=100)
	comments = models.ManyToManyField(Comentario)









