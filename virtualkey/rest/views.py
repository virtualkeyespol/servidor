from django.shortcuts import render
from django.http import JsonResponse
from django.forms.models import model_to_dict

from rest import utils
from rest.models import *

#############################################################
					## DISPOSITIVOS
#############################################################

#	La función solo toma un parámetro a la vez (a tráves de GET):
#	1) Sí se envía el parámetro <DISPOSITIVO_ID> se retornará el dispositivo correspondiente a ese ID
#	2) Sí se envía el parámetro <USUARIO_ID> se retornará los dispositivos que pertenezcan a dicho usuario
def get_dispositivo(request):
	if request.method == "GET":
		dispositivo_id = request.GET.get("DISPOSITIVO_ID", None)
		usuario_id = request.GET.get("USUARIO_ID", None)
		if dispositivo_id:
			try:
				dispositivo = Dispositivo.objects.get(pk=dispositivo_id)
				return JsonResponse({
			        'STATUS' : 'OK',
			        'RESPUESTA' : model_to_dict(dispositivo)
		        })
			except:
				return JsonResponse({
			        'STATUS' : 'ERROR',
			        'RESPUESTA' : 'Error encontrando dispositivo'
		        })
		elif usuario_id:
			try:
				usuario = Usuario().getUser(usuario_id)
				dispositivos = Dispositivo.objects.filter(usuario=usuario)
				return JsonResponse({
			        'STATUS' : 'OK',
			        'RESPUESTA' : utils.instancias_todic(dispositivos)
		        })
			except:
				return JsonResponse({
			        'STATUS' : 'ERROR',
			        'RESPUESTA' : 'Error encontrando dispositivos'
		        })
	return JsonResponse({
        'STATUS' : 'ERROR',
        'RESPUESTA' : 'Error de solicitud'
	})