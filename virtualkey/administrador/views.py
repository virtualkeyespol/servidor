from django.shortcuts import redirect, render
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest.models import *


#############################################################
                    ##  ERROR
#############################################################
def error_page(request):
    return render(request, "General/error.html")


#############################################################
                    ##  AUTENTICACION
#############################################################
def nuevousuario(request):
    if request.method == "POST":
        body = request.POST
        usuario = Usuario().create(body)
        if usuario:
            login(request, usuario)
            return redirect('panel_control')
    return render(request, "General/nuevousuario.html")

def iniciar_sesion(request):
    paquete = {}
    if request.method == "POST":
        username = request.POST.get("USUARIO", None)
        password = request.POST.get("CONTRASENA", None)
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('panel_control')
        else:
            paquete = {"ERROR" : "Error de credenciales."}
    return render(request, "General/login.html", paquete)
def cerrar_sesion(request):
    if request.method == "POST" and request.user.is_authenticated:
        logout(request)
        return redirect('iniciar_sesion')
    return redirect('error_page')



#############################################################
                    ## PANEL DE CONTROL
#############################################################
def panel_control(request):
    if request.user.is_authenticated:
        paquete = {
            'OPCION' : 'panel_control',
            'PANEL_CONTROL_ACTIVE' : 'active'
        }
        return render(request, "General/index.html", paquete)
    return redirect('iniciar_sesion')

## AJAX FUNC
def get_estadistica(request):
    data = generar_estadistica(request);
    return JsonResponse({
        "DATA" : data
    })


#############################################################
                    ## MIS DISPOSITIVOS
#############################################################
def dispositivos(request):
    if request.user.is_authenticated:
        dispositivos = Dispositivo.objects.filter(usuario=request.user)                     ## BUSCAR DISPOSITIVOS
        dispositivos = utils.empaquetar(dispositivos)                                       ## EMPAQUETAR DISPOSITIVOS
        paquete = {
            'OPCION' : 'dispositivos',
            'DISPOSITIVOS_ACTIVE' : 'active',
            'DISPOSITIVOS_EMPAQUETADOS' : dispositivos
        }
        return render(request, "General/index.html", paquete)
    return redirect('iniciar_sesion')

def crear_dispositivo(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            body = utils.combinar_request("USUARIO_ID", request.user.id, request.POST)
            dispositivo = Dispositivo().update(body)
            if dispositivo:
                return redirect('dispositivos')
        paquete = {
            'OPCION' : 'crear_dispositivo',
            'DISPOSITIVOS_ACTIVE' : 'active'
        }
        return render(request, "General/index.html", paquete)
    return redirect('iniciar_sesion')

def ver_dispositivo(request, id):
    if request.user.is_authenticated:
        dispositivo = Dispositivo.objects.get(pk=id)                                        ## BUSCAR DISPOSITIVO
        llaves = Llave.objects.filter(dispositivo=dispositivo).filter(es_dueno=False)
        paquete = {
            'OPCION' : 'ver_dispositivo',
            'DISPOSITIVOS_ACTIVE' : 'active',
            'DISPOSITIVO' : dispositivo,
            'LLAVES' : llaves
        }
        return render(request, "General/index.html", paquete)
    return redirect('iniciar_sesion')

def cambiarEstadoDispositivo(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            dispositivo_id = request.POST.get("DISPOSITIVO_ID", None)
            estado = request.POST.get("ESTADO", None)
            if dispositivo_id and estado:
                Dispositivo().cambiarEstado(dispositivo_id, estado)
        return redirect('ver_dispositivo', dispositivo_id)
    return redirect('iniciar_sesion')

def compartir_acceso(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            body = utils.combinar_request("DISPOSITIVO_ID", id, request.POST)
            print(body)
            llave = Llave().create(body)
            if llave:
                return redirect('ver_dispositivo', id)
        dispositivos = Dispositivo.objects.filter(usuario=request.user)
        dispositivo = Dispositivo.objects.get(pk=id)
        paquete = {
            'OPCION' : 'compartir_llave',
            'DISPOSITIVOS_ACTIVE' : 'active',
            'DISPOSITIVO' : dispositivo,
            'DISPOSITIVOS' : dispositivos
        }
        return render(request, "General/index.html", paquete)
    return redirect('iniciar_sesion')
        

#############################################################
                    ## MIS LLAVES
#############################################################
def llaves(request):
    if request.user.is_authenticated:
        llaves = Llave.objects.filter(usuario=request.user).filter(es_dueno=False)                                 ## BUSCAR LLAVES
        paquete = {
            'OPCION' : 'llaves',
            'LLAVES_ACTIVE' : 'active',
            'LLAVES' : llaves
        }
        return render(request, "General/index.html", paquete)
    return redirect('iniciar_sesion')
    
def revocarLlave(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            dispositivo_id = request.POST.get("DISPOSITIVO_ID", None)
            llave_id = request.POST.get("LLAVE_ID", None)
            if llave_id:
                Llave().cambiarEstado(llave_id, True)
        return redirect('ver_dispositivo', dispositivo_id)
    return redirect('iniciar_sesion')

 
#############################################################
                    ## CUENTAS
############################################################# 
def cuenta(request):
    if request.user.is_authenticated:
        paquete = {
            'OPCION' : 'cuenta',
            'CUENTA_ACTIVE' : 'active',
            'USUARIO' : request.user
        }
        return render(request, "General/index.html", paquete)
    return redirect('iniciar_sesion')
        
def editar_cuenta(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            body = utils.combinar_request("USUARIO_ID", request.user.id, request.POST)
            Usuario().update(body)
            return redirect('cuenta')
        paquete = {
            'OPCION' : 'editar_cuenta',
            'CUENTA_ACTIVE' : 'active',
            'USUARIO' : request.user
        }
        return render(request, "General/index.html", paquete)
    return redirect('iniciar_sesion')


#############################################################
                    ## REPORTES
#############################################################
def reportes(request):
    if request.user.is_authenticated:
        dispositivos = Dispositivo.objects.filter(usuario=request.user)
        reportes_paquete = []
        for d in dispositivos:
            reportes = Registro.objects.filter(dispositivo=d)
            reportes_paquete.append({
                "dispositivo" : d.nombre,
                "reportes" : reportes
                })
        paquete = {
            'OPCION' : 'reportes',
            'REPORTES_ACTIVE' : 'active',
            'REPORTES' : reportes_paquete
        }
        return render(request, "General/index.html", paquete)
    return redirect('iniciar_sesion')



#############################################################
    ## APARTADO // REGISTRO DE DISPOSITIVO AL SISTEMA
#############################################################
def registro_dispositivo(request):
    paquete = {}
    if request.method == "POST":
        dispositivo = Dispositivo().create(request.POST)
        if dispositivo:
            paquete["NUMERO_SERIE"] = dispositivo.numero_serie
    return render(request, "Apartado/registro_dispositivo.html", paquete)



        