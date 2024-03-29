import json
import math
from django.forms.models import model_to_dict

## TRANSFORMA REQUEST EN DICCIONARIO
def request_todict(request):
    try: 
        body = request.body.decode('utf-8')
        print(body)
        body = json.loads(body)
        return body
    except:
        return {}

##  COMBINA REQUEST.USER.ID + REQUEST.POST EN NUEVO DICCIONARIO
def combinar_request(key, value, request):
    paquete = {}
    paquete[key] = value
    for key, value in request.items():
        paquete[key] = value
    return paquete



## TRANSFORMA INSTANCIAS DE UN MODELO EN DICCIONARIO
def instancias_todic(instancias):
        paquete = []
        for instancia in instancias:
            paquete.append(model_to_dict(instancia))
        return paquete

##  EMPAQUETA OBJETOS EN ARRAY DE 3 ELEMENTOS
def empaquetar(objetos):
    total = len(objetos)
    total_paquetes = math.ceil(total/3)
    vuelta = 0
    paquete_padre = [] 
    for i in range(0,total_paquetes):
        paquete_hijo = []
        for j in range(0,3):
            if vuelta + j < total:
                paquete_hijo.append(objetos[vuelta + j])
            else:
                paquete_hijo.append(None)
        paquete_padre.append(paquete_hijo)
        vuelta += 3
    return paquete_padre

# def generarReportes(dispositivos):
#     reportes_paquete = []
#     for d in dispositivos:
#         reportes = Registro.objetos.filter(dispositivo=d)
#         reportes_paquete.append({
#             "dispositivo" : d.nombre,
#             "reportes" : reportes
#             })
#     return reportes_paquete 









    





