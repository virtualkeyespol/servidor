from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

from rest import utils
from rest.models import *

##########################################################################################
##  LOS PARÁMETROS QUE SE REFIEREN EN ESTAS INSTRUCCIONES SON LOS PARÁMETROS INCLUIDOS  ##
##  EN EL CUERPO DEL REQUEST                                                            ##
##########################################################################################


#############################################################
                    ## DISPOSITIVOS
#############################################################

##  La función toma dos parámetros <USUARIO_ID> y <NOMBRE> (a tráves de POST)
##  Con éxito la función retorna la instancia de dispositivo creada, con error la función retorna mensaje de error.
@csrf_exempt
def create_dispositivo(request):
    if request.method == "POST":
        body = utils.request_todict(request)
        dispositivo = Dispositivo().create(body)
        if dispositivo:
            return JsonResponse({
                'STATUS' : 'OK',
                'RESPUESTA' : model_to_dict(dispositivo)
            })  
    return JsonResponse({
        'STATUS' : 'ERROR',
        'RESPUESTA' : 'Error de solicitud'
    })


##  La función solo toma un parámetro a la vez (a tráves de GET):
##  1) Sí se envía el parámetro <DISPOSITIVO_ID> se retornará el dispositivo correspondiente a ese ID.
##  2) Sí se envía el parámetro <USUARIO_ID> se retornará los dispositivos que pertenezcan a dicho usuario.
##  Con éxito la función retorna una o varias instancias de dispositivo según solicitada, 
##  con error la función retorna mensaje de error.
def read_dispositivo(request):
    if request.method == "GET":
        body = request.GET
        respuesta = Dispositivo().read(body)
        if respuesta:
            return JsonResponse({
                'STATUS' : 'OK',
                'RESPUESTA' : respuesta
            })
    return JsonResponse({
        'STATUS' : 'ERROR',
        'RESPUESTA' : 'Error de solicitud'
    })

##  La función primordialmente necesita el parámetro <DISPOSITIVO_ID> (a tráves de POST)
##  la función puede aceptar a la vez los parámetros <NOMBRE> y <ESTADO>.
##  Con éxito la función retorna la instacia de dispositivo actualizada, con error la función retorna mensaje de error.
##  Parámetro <ESTADO> acepta "True" o "False"
@csrf_exempt
def update_dispositivo(request):
    if request.method == "POST":
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

##  La función toma como único parámetro <DISPOSITIVO_ID> (a tráves de POST)
##  Con éxito la función retorna mensaje de éxito, con error la función retorna mensaje de error.
@csrf_exempt
def delete_dispositivo(request):
    if request.method == "POST":
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

##  La función toma cuatro parámetros <USUARIO_ID>, <DISPOSITIVO_ID>, <FECHA_INICIO> y <FECHA_EXPIRACION> (a tráves de POST)
##  Con éxito la función retorna la instancia de llave creada, con error la función retorna mensaje de error.
##  Parámetro <FECHA_INICIO> y <FECHA_EXPIRACION> aceptan formato ej. "2019-07-23T05:40:27Z"
@csrf_exempt
def create_llave(request):
    if request.method == "POST":
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

##  La función solo toma un parámetro a la vez (a tráves de GET):
##  1) Sí se envía el parámetro <DISPOSITIVO_ID> se retornará las llaves correspondiente a ese dispositivo.
##  2) Sí se envía el parámetro <USUARIO_ID> se retornará las llaves que pertenezcan a dicho usuario.
##  3) Sí se envía el parámetro <LLAVE_ID> se retornará la llave correspondiente a ese ID.
##  Con éxito la función retorna una o varias instancias de la o las llaves según solicitada, 
##  con error la función retorna mensaje de error.
def read_llave(request):
    if request.method == "GET":
        body = request.GET
        respuesta = Llave().read(body)
        if respuesta:
            return JsonResponse({
                'STATUS' : 'OK',
                'RESPUESTA' : respuesta
            })
    return JsonResponse({
        'STATUS' : 'ERROR',
        'RESPUESTA' : 'Error de solicitud'
    })

##  La función primordialmente necesita el parámetro <LLAVE_ID> (a tráves de POST)
##  la función puede aceptar a la vez los parámetros <FECHA_EXPIRACION> y <REVOCADA>.
##  Con éxito la función retorna la instacia de dispositivo actualizada, con error la función retorna mensaje de error.
##  Parámetro <FECHA_INICIO> y <FECHA_EXPIRACION> aceptan formato ej. "2019-07-23T05:40:27Z"
##  Parámetro <REVOCADA> acepta "True" o "False"
@csrf_exempt
def update_llave(request):
    if request.method == "POST":
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



#############################################################
                    ## REGISTROS
#############################################################

##  La función toma un parámetro <LLAVE_ID> (a tráves de POST)
##  Con éxito la función retorna la instancia de registro creado, con error la función retorna mensaje de error.
@csrf_exempt
def create_registro(request):
    if request.method == "POST":
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

##  La función solo toma un parámetro a la vez (a tráves de GET):
##  1) Sí se envía el parámetro <DISPOSITIVO_ID> se retornará los registros correspondientes a ese dispositivo.
##  2) Sí se envía el parámetro <USUARIO_ID> se retornará los registros correspondientes a ese usuario.
##  3) Sí se envía el parámetro <LLAVE_ID> se retornará los registros correspondientes a esa llave.
##  4) Sí se envía el parámetro <REGISTRO_ID> se retornará el registro correspondiente a ese ID.
##  Con éxito la función retorna una o varias instancias de el o los registros según solicitado, 
##  con error la función retorna mensaje de error.
def read_registro(request):
    if request.method == "GET":
        body = request.GET
        respuesta = Registro().read(body)
        if respuesta:
            return JsonResponse({
                'STATUS' : 'OK',
                'RESPUESTA' : respuesta
            })
    return JsonResponse({
        'STATUS' : 'ERROR',
        'RESPUESTA' : 'Error de solicitud'
    })