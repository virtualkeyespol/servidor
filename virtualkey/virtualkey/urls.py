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

    ##	INDEX
    path('', views.panel_control, name='panel_control'),
    ##	MIS DISPOSITIVOS
    path('dispositivos',                views.dispositivos,                 name='dispositivos'),
    path('dispositivos/ver/<str:id>',   views.ver_dispositivo,              name='ver_dispositivo'),
    path('dispositivos/cambiarEstado',  views.cambiarEstadoDispositivo,     name='cambiarEstadoDispositivo'),
    
    ##	MIS LLAVES
    path('llaves',                      views.llaves,                       name='llaves'),
    path('llaves/revocar',              views.revocarLlave,                 name='revocarLlave'),

    #############################################################
                        ## REST API 
    #############################################################
    ##  DISPOSITIVO
    path('rest/dispositivo/create',     rest_views.create_dispositivo,      name='create_dispositivo'),
    path('rest/dispositivo/read',       rest_views.read_dispositivo,        name='read_dispositivo'),
    path('rest/dispositivo/update',     rest_views.update_dispositivo,      name='update_dispositivo'),
    path('rest/dispositivo/delete',     rest_views.delete_dispositivo,      name='delete_dispositivo'),

    ##  LLAVE
    path('rest/llave/create',           rest_views.create_llave,            name='create_llave'),
    path('rest/llave/read',             rest_views.read_llave,              name='read_llave'),
    path('rest/llave/update',           rest_views.update_llave,            name='update_llave'),

    ## REGISTRO
    path('rest/registro/create',        rest_views.create_registro,         name='create_registro'),
    path('rest/registro/read',          rest_views.read_registro,           name='read_registro'),
]






