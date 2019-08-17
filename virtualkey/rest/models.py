import datetime
import secrets
import random
from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.forms.models import model_to_dict

from rest import utils


#############################################################
                    ## USUARIO
#############################################################
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


#############################################################
                    ## SESION
#############################################################
class Sesion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    token =  models.CharField(max_length=70)
    created_at = models.DateTimeField(auto_now_add=True)

    def create(self, usuario):
        s = Sesion()
        s.usuario = usuario
        s.token = secrets.token_hex(32)
        s.save()
        return s
    def logout(self, token):
        try:
            s = Sesion.objects.get(token=token)
            s.delete()
            return  True
        except:
            return False
    def get_sesion(self, usuario):
        try:
            s = Sesion.objects.get(usuario=usuario)
            return s
        except:
            return None
    def get_user(self, token):
        try:
            s = Sesion.objects.get(token=token)
            return s.usuario
        except:
            return None

    def is_autenticated(self, body):
        try:
            if body.method == "POST":
                body = utils.request_todict(body)
            else: 
                body = body.GET
            token = body.get("TOKEN", None)
            Sesion.objects.get(token=token)
            return token
        except:
            return None

    def __str__ (self):
        return self.usuario.username



#############################################################
                    ## DISPOSITIVO
#############################################################
class Dispositivo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    modelo = models.CharField(max_length=50, default="")
    numero_serie = models.CharField(max_length=10, default="")
    nombre = models.CharField(max_length=100, null=True)
    estado = models.BooleanField(default=False)

    def __str__(self):
        if self.nombre:
            return self.nombre
        else:
            return self.modelo

    @classmethod
    def create(cls, body):
        modelo = body.get("MODELO", None)
        try:
            dispositivo = cls(modelo=modelo, numero_serie=secrets.randbits(32))
            dispositivo.save()
            return dispositivo
        except:
            return None

    def read(self, body):
        dispositivo_id = body.GET.get("DISPOSITIVO_ID", None)
        token = body.GET.get("TOKEN", None)
        try:
            if dispositivo_id:
                dispositivo = Dispositivo.objects.get(pk=dispositivo_id)
                ## AÑADIR DESCRIPCION EXTRA DE USUARIO Y DISPOSITIVO
                dispositivo = model_to_dict(dispositivo)
                usuario = model_to_dict(Usuario().getUser(dispositivo["usuario"]))
                dispositivo["usuario"] = usuario
                return dispositivo
            else:
                usuario = Sesion().get_user(token)
                dispositivos = Dispositivo.objects.filter(usuario=usuario)
                dispositivos = utils.instancias_todic(dispositivos)
                ## AÑADIR DESCRIPCION EXTRA DE USUARIO Y DISPOSITIVO
                for i in range(0, len(dispositivos)):
                    usuario = model_to_dict(Usuario().getUser(dispositivos[i]["usuario"]))
                    dispositivos[i]["usuario"] = usuario
                return dispositivos
        except Exception as e:
            print(str(e))
            return None

    def update(self, body):
        numero_serie = body.get("NUMERO_SERIE", None)
        token = body.get("TOKEN", None)
        usuario_id = body.get("USUARIO_ID", None)
        nombre = body.get("NOMBRE", None)
        estado = body.get("ESTADO", None)
        try:
            dispositivo = Dispositivo.objects.get(numero_serie=numero_serie)
            if not dispositivo.usuario:
                usuario = Sesion().get_user(token)
                if not usuario:
                    usuario = Usuario().getUser(usuario_id)
                dispositivo.usuario = usuario

                ## CREANDO LLAVE MASTER
                llave = Llave()
                llave.usuario = usuario
                llave.dispositivo = dispositivo
                llave.correo = usuario.username
                llave.codigo = secrets.token_urlsafe(15)
                llave.es_dueno = True
                llave.save()
            if nombre:
                dispositivo.nombre = nombre
            if estado:
                dispositivo.estado = estado

            dispositivo.save()
            return dispositivo
        except Exception as e:
            print(str(e))
            return None

    def delete_(self, body):
        numero_serie = body.get("NUMERO_SERIE", None)
        try:
            dispositivo = Dispositivo.objects.get(numero_serie=numero_serie)
            dispositivo.delete()
            return True
        except:
            return False

    def cambiarEstado(self, id, estado):
        dispositivo = Dispositivo.objects.get(pk=id)
        dispositivo.estado = estado
        dispositivo.save()
        return dispositivo

    def validar_numero_serie(self, numero_serie):
        if len(Dispositivo.objects.filter(numero_serie=numero_serie)) == 1:
            return True
        return False



#############################################################
                    ## LLAVE
#############################################################
class Llave(models.Model):
    dispositivo = models.ForeignKey('Dispositivo', on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    correo = models.EmailField(default="")
    codigo = models.CharField(max_length=20, default="")
    fecha_inicio = models.DateTimeField(null=True)
    fecha_expiracion = models.DateTimeField(null=True)
    revocada = models.BooleanField(default=False)
    es_multiuso = models.BooleanField(default=True)
    es_dueno = models.BooleanField(default=False)

    def __str__(self):
        return "Llave de: " + self.dispositivo.nombre

    @classmethod
    def create(cls, body):
        token = body.get("TOKEN", None)
        numero_serie = body.get("NUMERO_SERIE", None)
        dispositivo_id = body.get("DISPOSITIVO_ID", None)
        correo = body.get("CORREO", None)
        fecha_inicio = body.get("FECHA_INICIO", None)
        fecha_expiracion = body.get("FECHA_EXPIRACION", None)
        es_multiuso =  body.get("MULTIUSO", None)
        try:
            dispositivo = Dispositivo.objects.filter(numero_serie=numero_serie).first()
            if not dispositivo:
                dispositivo = Dispositivo.objects.get(pk=dispositivo_id)
            usuario = Usuario().findbyemail(correo)
            llave = cls(dispositivo=dispositivo, usuario=usuario, correo=correo, codigo=secrets.token_urlsafe(15), fecha_inicio=fecha_inicio, fecha_expiracion=fecha_expiracion)
            if es_multiuso == "on":
                llave.es_multiuso = False
            if es_dueno == True:
                llave.es_dueno = True 
            llave.save()
            return llave
        except:
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
        token = body.get("TOKEN", None)
        dispositivo_id = body.get("DISPOSITIVO_ID", None)
        llave_id = body.get("LLAVE_ID", None)
        numero_serie = body.get("NUMERO_SERIE", None)
        try:
            if dispositivo_id:    
                dispositivo = Dispositivo.objects.get(pk=dispositivo_id)
                llaves = Llave.objects.filter(dispositivo=dispositivo)
                llaves = utils.instancias_todic(llaves)
                ## AÑADIR DESCRIPCION EXTRA DE USUARIO Y DISPOSITIVO
                for i in range(0, len(llaves)):
                    usuario = model_to_dict(Usuario().getUser(llaves[i] ["usuario"]))
                    dispositivo = model_to_dict(Dispositivo.objects.get(pk=llaves[i] ["dispositivo"]))
                    llaves[i]["usuario"] = usuario
                    llaves[i]["dispositivo"] = dispositivo
                return llaves
            elif llave_id:
                llave = Llave.objects.get(pk=llave_id)
                ## AÑADIR DESCRIPCION EXTRA DE USUARIO Y DISPOSITIVO
                llave = model_to_dict(llave)
                usuario = model_to_dict(Usuario().getUser(llave["usuario"]))
                dispositivo = model_to_dict(Dispositivo.objects.get(pk=llave["dispositivo"]))
                llave["usuario"] = usuario
                llave["dispositivo"] = dispositivo
                return llave
            elif numero_serie:
                dispositivo = Dispositivo.objects.get(numero_serie=numero_serie)
                llaves = Llave.objects.filter(dispositivo=dispositivo)
                llaves = utils.instancias_todic(llaves)
                ## AÑADIR DESCRIPCION EXTRA DE USUARIO Y DISPOSITIVO
                for i in range(0, len(llaves)):
                    usuario = model_to_dict(Usuario().getUser(llaves[i]["usuario"]))
                    dispositivo = model_to_dict(Dispositivo.objects.get(pk=llaves[i]["dispositivo"]))
                    llaves[i]["usuario"] = usuario
                    llaves[i]["dispositivo"] = dispositivo
                return llaves
            else:
                usuario = Sesion().get_user(token)
                llaves = Llave.objects.filter(usuario=usuario)
                llaves = utils.instancias_todic(llaves)
                ## AÑADIR DESCRIPCION EXTRA DE USUARIO Y DISPOSITIVO
                for i in range(0, len(llaves)):
                    usuario = model_to_dict(Usuario().getUser(llaves[i]["usuario"]))
                    dispositivo = model_to_dict(Dispositivo.objects.get(pk=llaves[i]["dispositivo"]))
                    llaves[i]["usuario"] = usuario
                    llaves[i]["dispositivo"] = dispositivo
                return llaves
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



#############################################################
                    ## REGISTRO
#############################################################
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
        token = body.get("TOKEN", None)
        try:
            if registro_id:
                registro = Registro.objects.get(pk=registro_id)
                registro = model_to_dict(registro)
                ## AÑADIR DESCRIPCION EXTRA DE USUARIO Y DISPOSITIVO
                usuario = model_to_dict(Usuario().getUser(registro["usuario"]))
                dispositivo = model_to_dict(Dispositivo.objects.get(pk=registro["dispositivo"]))
                registro["usuario"] = usuario
                registro["dispositivo"] = dispositivo
                return registro
            elif llave_id:
                llave = Llave.objects.get(pk=llave_id)
                registros = Registro.objects.filter(llave=llave)
                registros = utils.instancias_todic(registros)
                ## AÑADIR DESCRIPCION EXTRA DE USUARIO Y DISPOSITIVO
                for i in range(0, len(registros)):
                    usuario = model_to_dict(Usuario().getUser(registros[i]["usuario"]))
                    dispositivo = model_to_dict(Dispositivo.objects.get(pk=registros[i]["dispositivo"]))
                    registros[i]["usuario"] = usuario
                    registros[i]["dispositivo"] = dispositivo
                return registros
            elif dispositivo_id:
                dispositivo = Dispositivo.objects.get(pk=dispositivo_id)
                registros = Registro.objects.filter(dispositivo=dispositivo)
                registros = utils.instancias_todic(registros)
                ## AÑADIR DESCRIPCION EXTRA DE USUARIO Y DISPOSITIVO
                for i in range(0, len(registros)):
                    usuario = model_to_dict(Usuario().getUser(registros[i]["usuario"]))
                    dispositivo = model_to_dict(Dispositivo.objects.get(pk=registros[i]["dispositivo"]))
                    registros[i]["usuario"] = usuario
                    registros[i]["dispositivo"] = dispositivo
                return registros
            else:
                usuario = Sesion().get_user(token)
                registros = Registro.objects.filter(usuario=usuario)
                registros = utils.instancias_todic(registros)
                ## AÑADIR DESCRIPCION EXTRA DE USUARIO Y DISPOSITIVO
                for i in range(0, len(registros)):
                    usuario = model_to_dict(Usuario().getUser(registros[i]["usuario"]))
                    dispositivo = model_to_dict(Dispositivo.objects.get(pk=registros[i]["dispositivo"]))
                    registros[i]["usuario"] = usuario
                    registros[i]["dispositivo"] = dispositivo
                return registros
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
    hoy = datetime.now()
    ayer = hoy - timedelta(1)
    anteayer = hoy - timedelta(2)
    anteanteayer = hoy - timedelta(3)

        
    paquete = {}
    paquete["labels"] = [        
        anteanteayer.strftime("%A"),
        anteayer.strftime("%A"),
        ayer.strftime("%A"),
        hoy.strftime("%A")
    ]
    datasets = []
    dispositivos = Dispositivo.objects.filter(usuario=request.user)
    for dispositivo in dispositivos:
        dispositivo_paquete = {}
        dias = []
        dias.append(0)
        dias.append(0)
        dias.append(0)
        dias.append(0)

        registros = Registro.objects.filter(dispositivo=dispositivo)
        for registro in registros:
            if registro.fecha.date() == hoy.date():
                dias[3] += 1
            elif registro.fecha.date() == (hoy - timedelta(1)).date():
                dias[2] += 1
            elif registro.fecha.date() == (hoy - timedelta(2)).date():
                dias[1] += 1
            elif registro.fecha.date() == (hoy - timedelta(3)).date():
                dias[0] += 1
        color = "#" + "%06x" % random.randint(0, 0xFFFFFF)
        dispositivo_paquete["data"] = dias
        dispositivo_paquete["lineTension"] = 0
        dispositivo_paquete["backgroundColor"] = 'transparent'
        dispositivo_paquete["borderColor"] = color
        dispositivo_paquete["borderWidth"] = 4
        dispositivo_paquete["pointBackgroundColor"] = color
        dispositivo_paquete["label"] = dispositivo.nombre
        dispositivo_paquete["dispositivo"] = dispositivo.nombre
        datasets.append(dispositivo_paquete)
    paquete["datasets"] = datasets

    return paquete




