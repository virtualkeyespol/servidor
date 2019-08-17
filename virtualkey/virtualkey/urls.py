"""virtualkey URL Configuration

The `urlpatterns` list routes URLs to rest_views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from administrador import views
from rest import views as rest_views
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),

    #############################################################
                        ## ADMINISTRADOR
    #############################################################

    ##  ERROR
    path('error',                                   views.error_page,                       name='error_page'),

    ##  AUTH
    path('nuevousuario',                            views.nuevousuario,                     name='nuevousuario'),
    path('login',                                   views.iniciar_sesion,                   name='iniciar_sesion'),
    path('logout',                                  views.cerrar_sesion,                    name='cerrar_sesion'),

    ##	INDEX
    path('',                                        views.panel_control,                    name='panel_control'),
    path('get_estadistica',                         views.get_estadistica,                  name='get_estadistica'),

    ##	MIS DISPOSITIVOS
    path('dispositivos',                            views.dispositivos,                     name='dispositivos'),
    path('dispositivos/crear',                      views.crear_dispositivo,                name='crear_dispositivo'),
    path('dispositivos/ver/<str:id>',               views.ver_dispositivo,                  name='ver_dispositivo'),
    path('dispositivos/cambiarEstado',              views.cambiarEstadoDispositivo,         name='cambiarEstadoDispositivo'),
    path('dispositivos/compartir/<str:id>',         views.compartir_acceso,                 name='compartir_acceso'),
    
    ##	MIS LLAVES
    path('llaves',                                  views.llaves,                           name='llaves'),
    path('llaves/revocar',                          views.revocarLlave,                     name='revocarLlave'),

    ##  CUENTA
    path('cuenta',                                  views.cuenta,                           name='cuenta'),
    path('cuenta/editar',                           views.editar_cuenta,                    name='editar_cuenta'),

    ##  REPORTES
    path('reportes',                                views.reportes,                         name='reportes'),

    ##  APARTADO // REGISTRO DE DISPOSITIVOS EN EL SISTEMA
    path('registro_dispositivo',                    views.registro_dispositivo,             name='registro_dispositivo'),
    

    #############################################################
                        ## REST API 
    #############################################################
    ##  AUTH
    path('rest/login',                              rest_views.rest_iniciar_sesion,         name='rest_iniciar_sesion'),
    path('rest/logout',                             rest_views.rest_cerrar_sesion,          name='rest_cerrar_sesion'),

    ##  DISPOSITIVO
    path('rest/dispositivo/read',                   rest_views.read_dispositivo,            name='read_dispositivo'),
    path('rest/dispositivo/update',                 rest_views.update_dispositivo,          name='update_dispositivo'),
    path('rest/dispositivo/delete',                 rest_views.delete_dispositivo,          name='delete_dispositivo'),

    ##  LLAVE
    path('rest/llave/create',                       rest_views.create_llave,                name='create_llave'),
    path('rest/llave/read',                         rest_views.read_llave,                  name='read_llave'),
    path('rest/llave/update',                       rest_views.update_llave,                name='update_llave'),
    ##      **PARA DISPOSITIVO**
    path('rest/llave/read_llaves_dispositivo',      rest_views.read_llaves_dispositivo,     name='read_llaves_dispositivo'),
    path('rest/llave/verificar_llave',              rest_views.verificar_llave,             name='verificar_llave'),
    

    ## REGISTRO
    path('rest/registro/create',                    rest_views.create_registro,             name='create_registro'),
    path('rest/registro/read',                      rest_views.read_registro,               name='read_registro'),


    path('rest/abrir',                      rest_views.abrir,               name='abrir'),
]






