import requests
import json

parametros = {'USUARIO':'pdestrad@gmail.com', 'CONTRASENA': 'homoplato1'}

r = requests.post('http://127.0.0.1:8000/rest/login', data=json.dumps(parametros))
respuesta = json.dumps(r.json())
print(respuesta)