import json
from django.forms.models import model_to_dict

## TRANSFORMA REQUEST EN DICCIONARIO
def request_todict(request):
    try: 
        body = request.body.decode('utf-8')
        body = json.loads(body)
        return body
    except:
        return {}

## TRANSFORMA INSTANCIAS DE UN MODELO EN DICCIONARIO
def instancias_todic(instancias):
        paquete = []
        for instancia in instancias:
            paquete.append(model_to_dict(instancia))
        return paquete