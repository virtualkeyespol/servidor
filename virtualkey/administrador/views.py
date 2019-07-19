from django.shortcuts import redirect, render
from django.forms.models import model_to_dict
from administrador import utils
from rest.models import *

## PANEL DE CONTROL
def panel_control(request):
	paquete = {
		'OPCION' : 'panel_control',
		'PANEL_CONTROL_ACTIVE' : 'active'
	}
	return render(request, "General/index.html", paquete)

## MIS DISPOSITIVOS
def dispositivos(request):
	dispositivos = Dispositivo.objects.all() 					## BUSCAR DISPOSITIVOS
	dispositivos = utils.empaquetar(dispositivos) 				## EMPAQUETAR DISPOSITIVOS
	paquete = {
		'OPCION' : 'dispositivos',
		'DISPOSITIVOS_ACTIVE' : 'active',
		'DISPOSITIVOS_EMPAQUETADOS' : dispositivos
	}
	return render(request, "General/index.html", paquete)
def ver_dispositivo(request, id):
	dispositivo = Dispositivo.objects.get(pk=id) 				## BUSCAR DISPOSITIVO
	llaves = Llave.objects.filter(dispositivo=dispositivo)
	paquete = {
		'OPCION' : 'ver_dispositivo',
		'DISPOSITIVOS_ACTIVE' : 'active',
		'DISPOSITIVO' : dispositivo,
		'LLAVES' : llaves
	}
	return render(request, "General/index.html", paquete)
def cambiarEstadoDispositivo(request):
	if request.method == "POST":
		dispositivo_id = request.POST.get("DISPOSITIVO_ID", None)
		estado = request.POST.get("ESTADO", None)
		if dispositivo_id and estado:
			Dispositivo().cambiarEstado(dispositivo_id, estado)
	return redirect('ver_dispositivo', dispositivo_id)

## MIS LLAVES
def llaves(request):
	llaves = Llave.objects.all()								## BUSCAR LLAVES
	llaves = utils.empaquetar(llaves) 							## EMPAQUETAR DISPOSITIVOS
	paquete = {
		'OPCION' : 'llaves',
		'LLAVES_ACTIVE' : 'active',
		'LLAVES_EMPAQUETADOS' : llaves
	}
	return render(request, "General/index.html", paquete)
def revocarLlave(request):
	if request.method == "POST":
		dispositivo_id = request.POST.get("DISPOSITIVO_ID", None)
		llave_id = request.POST.get("LLAVE_ID", None)
		if llave_id:
			Llave().cambiarEstado(llave_id, True)
	return redirect('ver_dispositivo', dispositivo_id)