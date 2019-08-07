import requests
import json
import os
import time

while True:
	try:
		##	LEER NUMERO DE SERIE DEL DISPOSITIVO
		f=open("numero_serie.txt", "r")
		NUMERO_SERIE = int(f.read())
		f.close()

		## REALIZAR REQUEST
		parametros = {"NUMERO_SERIE" : NUMERO_SERIE}
		r = requests.get('http://127.0.0.1:8000/rest/llave/read_llaves_dispositivo', params=parametros)

		if r.status_code == 200:
			## VERIFICANDO RESPUESTA DEL SERVIDOR
			respuesta = json.loads(r.text)
			if respuesta["STATUS"] == "OK":
				##	GUARDANDO LLAVES
				llaves = {}
				f=open("llaves.txt", "w+")
				respuesta = json.loads(r.text)
				for llave in respuesta["RESPUESTA"]:
					llaves[llave["codigo"]] =  {
						"fecha_expiracion" : llave["fecha_expiracion"],
						"fecha_inicio" : llave["fecha_inicio"]
					}
				f.write(json.dumps(llaves))
				f.close()
				print("LLAVES ACTUALIZADAS CON ÉXITO")
			else:
				print("ERROR")
		else:
			## MANEJO DE ERROR DE REQUEST
			print("ERROR DE REQUEST")

	except:
		## MANEJO DE ERROR EN LECTURA DE NUMERO DE SERIE
		print("ERROR EN LECTURA DE NUMERO DE SERIE")
	import time
	time.sleep(120)
	