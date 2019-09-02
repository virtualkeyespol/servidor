from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate, login, logout

from rest import utils
from rest.models import *

##########################################################################################
##  LOS PARÁMETROS QUE SE REFIEREN EN ESTAS INSTRUCCIONES SON LOS PARÁMETROS INCLUIDOS  ##
##  EN EL CUERPO DEL REQUEST                                                            ##
##########################################################################################


#############################################################
                    ## AUTENTICACION
#############################################################
##  Parámetros Obligatorios: <CORREO>, <CONTRASENA>, <NOMBRES>, <APELLIDOS> (a través de POST)
##  Con éxito la función retorna el token de sesión, con error la función retorna mensaje de error.
@csrf_exempt
def rest_crear_usuario(request):
    if request.method == "POST":
        body = utils.request_todict(request)
        usuario = Usuario().create(body)
        if usuario is not None:
            sesion = Sesion().create(usuario)
            return JsonResponse({
                'STATUS' : 'OK',
                'RESPUESTA' : sesion.token
            })
        else:
            return JsonResponse({
                'STATUS' : 'ERROR',
                'RESPUESTA' : 'Error creando usuario'
            })            
    return JsonResponse({
        'STATUS' : 'ERROR',
        'RESPUESTA' : 'Error de solicitud'
    })

        

##  Parámetros Obligatorios: <USUARIO> y <CONTRASENA> (a través de POST)
##  Con éxito la función retorna el token de sesión, con error la función retorna mensaje de error.
@csrf_exempt
def rest_iniciar_sesion(request):
    if request.method == "POST":
        body = utils.request_todict(request)
        username = body.get("USUARIO", None)
        password = body.get("CONTRASENA", None)
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            sesion = Sesion().create(usuario)
            return JsonResponse({
                'STATUS' : 'OK',
                'RESPUESTA' : sesion.token
            })
        else:
            return JsonResponse({
                'STATUS' : 'ERROR',
                'RESPUESTA' : 'Error de credenciales'
            })            
    return JsonResponse({
        'STATUS' : 'ERROR',
        'RESPUESTA' : 'Error de solicitud'
    })

##  Parámetro Obligatorio: <TOKEN> (a través de POST)
##  Con éxito la función retorna mensaje de cierre de sesión, con error la función retorna mensaje de error.
@csrf_exempt
def rest_cerrar_sesion(request):
    token = Sesion().is_autenticated(request)
    if request.method == "POST" and token:
        Sesion().logout(token)
        return JsonResponse({
            'STATUS' : 'OK',
            'RESPUESTA' : 'Sesión cerrada'
        })            
    return JsonResponse({
        'STATUS' : 'ERROR',
        'RESPUESTA' : 'Error de solicitud'
    })

#############################################################
                    ## DISPOSITIVOS
#############################################################

##  Parámetro Obligatorio: <TOKEN> (a tráves de GET):
##  Parámetros Opcionales:
##  1) <DISPOSITIVO_ID> se retornará el dispositivo correspondiente a ese ID.
##  Sí no se envía parámetro se retornará los dispositivos que pertenezcan al usuario autenticado.
##  Con éxito la función retorna una o varias instancias de dispositivo según solicitada, 
##  con error la función retorna mensaje de error.
def read_dispositivo(request):
    token = Sesion().is_autenticated(request)
    if request.method == "GET" and token:
        respuesta = Dispositivo().read(request)
        if not respuesta==None:
            return JsonResponse({
                'STATUS' : 'OK',
                'RESPUESTA' : respuesta
            })
    return JsonResponse({
        'STATUS' : 'ERROR',
        'RESPUESTA' : 'Error de solicitud'
    })

##  Parámetros Obligatorios: <TOKEN> y <NUMERO_SERIE> (a tráves de POST)
##  Paramétros opcionales: <NOMBRE> y <ESTADO>.
##  Con éxito la función retorna la instacia de dispositivo actualizada, con error la función retorna mensaje de error.
##  Parámetro <ESTADO> acepta "True" o "False"
@csrf_exempt
def update_dispositivo(request):
    token = Sesion().is_autenticated(request)
    if request.method == "POST" and token:
        body = utils.request_todict(request)
        dispositivo = Dispositivo().update(body)
        if dispositivo:
            return JsonResponse({
                'STATUS' : 'OK',
                'RESPUESTA' : model_to_dict(dispositivo)
            })  
    return JsonResponse({
        'STATUS' : 'ERROR',
        'RESPUESTA' : 'Error de solicitud'
    })

##  Parámetros Obligatorios: <TOKEN> y <NUMERO_SERIE> (a tráves de POST)
##  Con éxito la función retorna mensaje de éxito, con error la función retorna mensaje de error.
@csrf_exempt
def delete_dispositivo(request):
    token = Sesion().is_autenticated(request)
    if request.method == "POST" and token:
        body = utils.request_todict(request)
        respuesta = Dispositivo().delete_(body)
        if respuesta:
            return JsonResponse({
                'STATUS' : 'OK',
                'RESPUESTA' : 'Dispositivo eliminado con éxito'
            })  
    return JsonResponse({
        'STATUS' : 'ERROR',
        'RESPUESTA' : 'Error de solicitud'
    }) 


#############################################################
                    ## LLAVES
#############################################################

##  Parámetros Obligatorios: <TOKEN>, <CORREO>, <NUMERO_SERIE> (a tráves de POST)
##  Parámetros opcionales: <MULTIUSO>, <DUENO>, <FECHA_INICIO> y <FECHA_EXPIRACION>
##  Con éxito la función retorna la instancia de llave creada, con error la función retorna mensaje de error.
##  Parámetro <FECHA_INICIO> y <FECHA_EXPIRACION> aceptan formato de fecha ej. "2019-07-23T05:40:27Z"
##  Parámetro <MULTIUSO> y <DUENO> aceptan formato booleano ej. "True" o "False"
@csrf_exempt
def create_llave(request):
    token = Sesion().is_autenticated(request)
    if request.method == "POST" and token:
        body = utils.request_todict(request)
        llave = Llave().create(body)
        if llave:
            return JsonResponse({
                'STATUS' : 'OK',
                'RESPUESTA' : model_to_dict(llave)
            })  
    return JsonResponse({
        'STATUS' : 'ERROR',
        'RESPUESTA' : 'Error de solicitud'
    })

##  Parámetro Obligatorio: <TOKEN> (a tráves de GET)
##  Parámetros Opcionales:
##  1) Sí se envía el parámetro <DISPOSITIVO_ID> se retornará las llaves correspondiente a ese dispositivo.
##  2) Sí se envía el parámetro <NUMERO_SERIE> se retornará las llaves que pertenezcan a dicho dispositivo.
##  3) Sí se envía el parámetro <LLAVE_ID> se retornará la llave correspondiente a ese ID.
##  Sí no se envía parámetro se retornará las llaves correspondiente al usuario autenticados.
##  Con éxito la función retorna una o varias instancias de la o las llaves según solicitada, 
##  con error la función retorna mensaje de error.
def read_llave(request):
    token = Sesion().is_autenticated(request)
    if request.method == "GET" and token:
        body = request.GET
        respuesta = Llave().read(body)
        if not respuesta==None:
            return JsonResponse({
                'STATUS' : 'OK',
                'RESPUESTA' : respuesta
            })
    return JsonResponse({
        'STATUS' : 'ERROR',
        'RESPUESTA' : 'Error de solicitud'
    })

##  Parámetro Obligatorio:  <TOKEN> y <LLAVE_ID> (a tráves de POST)
##  Parámetros Opcionales <FECHA_EXPIRACION> y <REVOCADA>.
##  Con éxito la función retorna la instacia de dispositivo actualizada, con error la función retorna mensaje de error.
##  Parámetro <FECHA_INICIO> y <FECHA_EXPIRACION> aceptan formato ej. "2019-07-23T05:40:27Z"
##  Parámetro <REVOCADA> acepta "True" o "False"
@csrf_exempt
def update_llave(request):
    token = Sesion().is_autenticated(request)
    if request.method == "POST" and token:
        body = utils.request_todict(request)
        llave = Llave().update(body)
        if llave:
            return JsonResponse({
                'STATUS' : 'OK',
                'RESPUESTA' : model_to_dict(llave)
            })  
    return JsonResponse({
        'STATUS' : 'ERROR',
        'RESPUESTA' : 'Error de solicitud'
    })

##  ** PARA DISPOSITIVO **
##  La función toma un unico parámetro <NUMERO_SERIE> (a tráves de GET)
##  Con éxito la función retorna las llaves asociadas al dispositivo ligado al número de serie
##  Con error la función retorna mensaje de error.
def read_llaves_dispositivo(request):
    if request.method == "GET":
        accion = 0
        body = request.GET
        numero_serie = body.get("NUMERO_SERIE", None)
        numero_serie = numero_serie.replace("%", ":")
        if Dispositivo().validar_numero_serie(numero_serie):
            dispositivo = Dispositivo.objects.get(numero_serie=numero_serie)
            llaves = Llave.objects.filter(dispositivo=dispositivo)
            respuesta = utils.instancias_todic(llaves)
            if dispositivo.estado == True:
                accion = 1
                dispositivo.estado = False
                dispositivo.save()
            if not respuesta==None:
                return JsonResponse({
                    'STATUS' : 'OK',
                    'RESPUESTA' : respuesta,
                    'ACCION' : accion
                })
    return JsonResponse({
        'STATUS' : 'ERROR',
        'RESPUESTA' : 'Error de solicitud'
    })

def verificar_llave(request):
    if request.method == "GET":
        body = request.GET
        codigo = body.get("CODIGO", None)
        llave = Llave.objects.filter(codigo=codigo).first()
        print(llave, llave.estado)
        if llave and llave.estado == "Activa":
            return JsonResponse({
                'STATUS' : 'OK'
            })
        else:
            return JsonResponse({
                'STATUS' : 'ERROR',
            })
            
    return JsonResponse({
        'STATUS' : 'ERROR',
        'RESPUESTA' : 'Error de solicitud'
    })


#############################################################
                    ## REGISTROS
#############################################################

##  Parámetro Obligatorio:  <TOKEN> y <LLAVE_ID> (a tráves de POST)
##  Con éxito la función retorna la instancia de registro creado, con error la función retorna mensaje de error.
@csrf_exempt
def create_registro(request):
    token = Sesion().is_autenticated(request)
    if request.method == "POST" and token:
        body = utils.request_todict(request)
        registro = Registro().create(body)
        if registro:
            return JsonResponse({
                'STATUS' : 'OK',
                'RESPUESTA' : model_to_dict(registro)
            })  
    return JsonResponse({
        'STATUS' : 'ERROR',
        'RESPUESTA' : 'Error de solicitud'
    })

##  Parámetro Obligatorio: <TOKEN> (a tráves de GET):
##  Parámetros Opcionales:
##  1) Sí se envía el parámetro <DISPOSITIVO_ID> se retornará los registros correspondientes a ese dispositivo.
##  2) Sí se envía el parámetro <LLAVE_ID> se retornará los registros correspondientes a esa llave.
##  3) Sí se envía el parámetro <REGISTRO_ID> se retornará el registro correspondiente a ese ID.
##  Sí no se envía ningún parametro se retornará los registros correspodientes al usuario autenticado.
##  Con éxito la función retorna una o varias instancias de el o los registros según solicitado, 
##  con error la función retorna mensaje de error.
def read_registro(request):
    token = Sesion().is_autenticated(request)
    if request.method == "GET" and token:
        body = request.GET
        respuesta = Registro().read(body)
        if not respuesta==None:
            return JsonResponse({
                'STATUS' : 'OK',
                'RESPUESTA' : respuesta
            })
    return JsonResponse({
        'STATUS' : 'ERROR',
        'RESPUESTA' : 'Error de solicitud'
    })






@csrf_exempt
def abrir(request):
    token = Sesion().is_autenticated(request)
    if request.method == "POST" and token:
        body = utils.request_todict(request)
        codigo = body.get("CODIGO", None)
        print("CODIGO")
        print(codigo)
        llave = Llave.objects.get(codigo=codigo)
        llave.dispositivo.estado = True 
        llave.dispositivo.save()
        ## CREANDO REGISTRO
        registro = Registro()
        registro.llave = llave
        registro.dispositivo = llave.dispositivo
        registro.usuario = llave.usuario
        registro.save()

        return JsonResponse({
            'STATUS' : 'OK',
            'RESPUESTA' : 'DISPOSITIVO ABIERTO'
        })  
    return JsonResponse({
        'STATUS' : 'ERROR',
        'RESPUESTA' : 'Error de solicitud'
    })






