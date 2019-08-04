import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.forms.models import model_to_dict

from rest import utils

class Usuario(models.Model):
    def create(self, body):
        try:
            correo = body.get("CORREO", None)
            contrasena = body.get("CONTRASENA", None)
            nombres = body.get("NOMBRES", None)
            apellidos = body.get("APELLIDOS", None)

            usuario = User.objects.create_user(correo, correo, contrasena)
            usuario.first_name = nombres
            usuario.last_name = apellidos
            usuario.save()

            ##  BUSCANDO LLAVES PENDIENTES Y AGREGANDOLAS AL USUARIO
            llaves = Llave.objects.filter(correo=correo)
            for llave in llaves:
                llave.usuario = usuario
                llave.save()

            return usuario
        except:
            return None

    def getUser(self, usuario_id):
        try:
            usuario = User.objects.get(pk=usuario_id)
            return usuario
        except :
            return None
    def findbyemail(self, email):
        try:
            usuario = User.objects.filter(email=email).first()
            return usuario
        except:
            return None

    def update(self, body):
        usuario_id = body.get("USUARIO_ID", None)
        nombres = body.get("NOMBRES", None)
        apellidos = body.get("APELLIDOS", None)
        correo = body.get("CORREO", None)
        try:
            usuario = User.objects.get(pk=usuario_id)
            if nombres:
                usuario.first_name = nombres
            if apellidos:
                usuario.last_name = apellidos
            if correo: 
                usuario.username = correo
                usuario.email = correo
            usuario.save()
            return usuario
        except:
            return None


class Llave(models.Model):
    dispositivo = models.ForeignKey('Dispositivo', on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    correo = models.EmailField(default="")
    fecha_inicio = models.DateTimeField()
    fecha_expiracion = models.DateTimeField()
    revocada = models.BooleanField(default=False)

    def __str__(self):
        return "Llave de: " + self.dispositivo.nombre

    @classmethod
    def create(cls, body):
        dispositivo_id = body.get("DISPOSITIVO_ID", None)
        correo = body.get("CORREO", None)
        fecha_inicio = body.get("FECHA_INICIO", None)
        fecha_expiracion = body.get("FECHA_EXPIRACION", None)
        try:
            dispositivo = Dispositivo.objects.get(pk=dispositivo_id)
            usuario = Usuario().findbyemail(correo)
            llave = cls(dispositivo=dispositivo, usuario=usuario, correo=correo, fecha_inicio=fecha_inicio, fecha_expiracion=fecha_expiracion)
            llave.save()
            return llave
        except Exception as e:
            print(str(e))
            return None

    @property
    def estado(self):
        if self.revocada:
            return "Revocada"
        elif self.fecha_inicio > timezone.now():
            return "No activa"
        elif self.fecha_expiracion < timezone.now():
            return "Expirada"
        return "Activa"

    def read(self, body):
        dispositivo_id = body.get("DISPOSITIVO_ID", None)
        usuario_id = body.get("USUARIO_ID", None)
        llave_id = body.get("LLAVE_ID", None)
        try:
            if dispositivo_id:    
                dispositivo = Dispositivo.objects.get(pk=dispositivo_id)
                llaves = Llave.objects.filter(dispositivo=dispositivo)
                return utils.instancias_todic(llaves)
            elif usuario_id:
                usuario = Usuario().getUser(usuario_id)
                llaves = Llave.objects.filter(usuario=usuario)
                return utils.instancias_todic(llaves)
            elif llave_id:
                llave = Llave.objects.get(pk=llave_id)
                return model_to_dict(llave)
            else:
                return None
        except:
            return None

    def update(self, body):
        llave_id = body.get("LLAVE_ID", None)
        revocada = body.get("REVOCADA", None)
        fecha_expiracion = body.get("FECHA_EXPIRACION", None)
        try:
            llave = Llave.objects.get(pk=llave_id)
            if revocada:
                llave.revocada = revocada
            if fecha_expiracion:
                llave.fecha_expiracion = fecha_expiracion
            llave.save()
            return llave
        except:
            return None

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
    def create(cls, body):
        usuario_id = body.get("USUARIO_ID", None)
        nombre = body.get("NOMBRE", None)
        try:
            usuario = Usuario().getUser(usuario_id)
            dispositivo = cls(usuario=usuario, nombre=nombre)
            dispositivo.save()
            return dispositivo
        except:
            return None

    def read(self, body):
        dispositivo_id = body.GET.get("DISPOSITIVO_ID", None)
        usuario = body.user
        try:
            if dispositivo_id:
                dispositivo = Dispositivo.objects.get(pk=dispositivo_id)
                return model_to_dict(dispositivo)
            elif usuario:
                dispositivos = Dispositivo.objects.filter(usuario=usuario)
                return utils.instancias_todic(dispositivos)
            else:
                return None
        except:
            return None

    def update(self, body):
        dispositivo_id = body.get("DISPOSITIVO_ID", None)
        nombre = body.get("NOMBRE", None)
        estado = body.get("ESTADO", None)
        try:
            dispositivo = Dispositivo.objects.get(pk=dispositivo_id)
            if nombre:
                dispositivo.nombre = nombre
            if estado:
                dispositivo.estado = estado
                ## CREAR REGISTRO

            dispositivo.save()
            return dispositivo
        except:
            return None

    def delete_(self, body):
        dispositivo_id = body.get("DISPOSITIVO_ID", None)
        try:
            dispositivo = Dispositivo.objects.get(pk=dispositivo_id)
            dispositivo.delete()
            return True
        except:
            return False

    def cambiarEstado(self, id, estado):
        dispositivo = Dispositivo.objects.get(pk=id)
        dispositivo.estado = estado
        dispositivo.save()
        return dispositivo

class Registro(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    dispositivo = models.ForeignKey('Dispositivo', on_delete=models.CASCADE)
    llave = models.ForeignKey('Llave', on_delete=models.CASCADE, default=None)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.usuario.username + " | " + self.dispositivo.nombre + " | " + str(self.fecha) 

    @classmethod
    def create(cls, body):
        llave_id = body.get("LLAVE_ID", None)
        try:
            llave = Llave.objects.get(pk=llave_id)
            registro = cls(usuario=llave.usuario, dispositivo=llave.dispositivo, llave=llave)
            registro.save()
            return registro
        except Exception as e:
            return None

    def read(self, body):
        registro_id = body.get("REGISTRO_ID", None)
        llave_id = body.get("LLAVE_ID", None)
        dispositivo_id = body.get("DISPOSITIVO_ID", None)
        usuario_id = body.get("USUARIO_ID", None)
        try:
            if registro_id:
                registro = Registro.objects.get(pk=registro_id)
                return model_to_dict(registro)
            elif llave_id:
                llave = Llave.objects.get(pk=llave_id)
                registros = Registro.objects.filter(llave=llave)
                return utils.instancias_todic(registros)
            elif dispositivo_id:
                dispositivo = Dispositivo.objects.get(pk=dispositivo_id)
                registros = Registro.objects.filter(dispositivo=dispositivo)
                return utils.instancias_todic(registros)
            elif usuario_id:
                usuario = Usuario().getUser(usuario_id)
                registros = Registro.objects.filter(usuario=usuario)
                return utils.instancias_todic(registros)
            else:
                return None
        except:
            return None



##########################################################################
############                MODEL FUNCTIONS                   ############ 
##########################################################################


##GENERAR ESTADISTICA PARA PANEL DE CONTROL
def generar_estadistica(request):
    ##
    ## ARREGLAR QUERIES DE BUSQUEDA SEGUN FECHAS
    ##

    ##  ENCONTRAR RANGOS DE INICIOS Y FINAL DE SEMANA
    hoy = datetime.date.today()
    tercero = hoy - datetime.timedelta(1)
    segundo = hoy - datetime.timedelta(2)
    primero = hoy - datetime.timedelta(3)
    
    

    ##  BUSCAR REGISTROS QUE ENTREN EN EL RANGO
    reportes_primero = Registro.objects.filter(usuario=request.user, fecha__gt=primero - datetime.timedelta(1), fecha__lte=primero)
    reportes_segundo = Registro.objects.filter(usuario=request.user, fecha__gt=primero, fecha__lte=segundo)
    reportes_tercero = Registro.objects.filter(usuario=request.user, fecha__gt=segundo, fecha__lte=tercero)
    reportes_cuarto = Registro.objects.filter(usuario=request.user, fecha__gt=tercero, fecha__lte=hoy)

    paquete = {}
    dispositivos = Dispositivo.objects.filter(usuario=request.user)
    for dispositivo in dispositivos:
        if not dispositivo.nombre in paquete:
            paquete[dispositivo.nombre] = [0,0,0,0]

    for dispositivo in dispositivos:
        for r in reportes_primero:
            if r.dispositivo == dispositivo:
                paquete[dispositivo.nombre][0] += 1
        for r in reportes_segundo:
            if r.dispositivo == dispositivo:
                paquete[dispositivo.nombre][1] += 1
        for r in reportes_tercero:
            if r.dispositivo == dispositivo:
                paquete[dispositivo.nombre][2] += 1
        for r in reportes_cuarto:
            if r.dispositivo == dispositivo:
                paquete[dispositivo.nombre][3] += 1

    print(Registro.objects.last().fecha, hoy)
    print(Registro.objects.filter(fecha__gte=tercero, fecha__lte=hoy))
    print(reportes_primero, reportes_segundo, reportes_tercero, reportes_cuarto)
    print(paquete)







