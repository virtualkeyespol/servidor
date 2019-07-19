import math

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