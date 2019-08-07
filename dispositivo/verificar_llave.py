def verificar_llave_localmente(llave):
    f = open("llaves.txt", "r")
    llaves = f.read()
    llaves = json.loads(llaves)
    if llave in llaves:
        ## MANEJO DE LLAVE VALIDA
		print("LLAVE VALIDA")
		return True
    ##	MANEJO DE LLAVE INVALIDA
	print("LLAVE INVALIDA")
	return False

def verificar_llave_en_servidor(llave):
	parametros = {"CODIGO" : llave}
	r = requests.get('http://127.0.0.1:8000/rest/llave/verificar_llave', params=parametros)
	if r.status_code == 200:
		## VERIFICANDO RESPUESTA DEL SERVIDOR
		respuesta = json.loads(r.text)
		if respuesta["STATUS"] == "OK" and not respuesta["RESPUESTA"] == "INVALIDA":
			## MANEJO DE LLAVE VALIDA
			print("LLAVE VALIDA")
			return True
		else:
			##	MANEJO DE LLAVE INVALIDA
			print("LLAVE INVALIDA")
			return False
	else:
		## MANEJO DE ERROR DE REQUEST
		print("ERROR DE REQUEST")
		return False