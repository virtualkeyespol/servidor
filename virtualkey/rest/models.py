from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Llave (models.Model):
    dispositivo = models.ForeignKey('Dispositivo', on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField()
    fecha_expiracion = models.DateTimeField()
    revocada = models.BooleanField(default=True)

    def __str__(self):
        return "Llave de: " + self.dispositivo.nombre

    @classmethod
    def create(cls, dispositivo, usuario, fecha_inicio, fecha_expiracion, revocada):
        llave = cls(dispositivo=dispositivo, usuario=usuario, fecha_inicio=fecha_inicio, fecha_expiracion=fecha_expiracion)
        llave.save()
        return llave

    @property
    def estado(self):
        if self.revocada:
            return "Revocada"
        elif self.fecha_inicio > timezone.now():
            return "No activa"
        elif self.fecha_expiracion < timezone.now():
            return "Expirada"
        return "Activa"

    def cambiarEstado(self, id, revocada):
        llave = Llave.objects.get(pk=id)
        llave.revocada = revocada
        llave.save()
        return llave


class Dispositivo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    estado = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

    @classmethod
    def create(cls, usuario, nombre, estado):
        dispositivo = cls(usuario=usuario, nombre=nombre)
        dispositivo.save()
        return dispositivo

    def cambiarEstado(self, id, estado):
        dispositivo = Dispositivo.objects.get(pk=id)
        dispositivo.estado = estado
        dispositivo.save()
        return dispositivo

class Registro(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    dispositivo = models.ForeignKey('Dispositivo', on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.usuario.username + " | " + self.dispositivo.nombre + " | " + str(self.fecha) 

    @classmethod
    def create(cls, usuario, dispositivo, fecha):
        registro = cls(usuario=usuario, dispositivo=dispositivo, fecha=fecha)
        registro.save()
        return registro