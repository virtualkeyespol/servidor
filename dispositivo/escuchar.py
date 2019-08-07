import bluetooth
import verificar_llave

def recibir_mensajes():
    server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

    port = 1
    server_sock.bind(("",port))
    server_sock.listen(1)

    client_sock,address = server_sock.accept()
    print("CONEXION ACEPTADA")

    llave = client_sock.recv(1024)
    ## MANEJANDO LLAVE RECIBIDA
    if verificar_llave_localmente(llave):
        ##ABRIR DISPOSITIVO
        print("LLAVE VALIDA")
    elif verificar_llave_en_servidor(llave):
        ##ABRIR DISPOSITIVO
        print("LLAVE VALIDA")
    else:
        ##ABRIR DISPOSITIVO
        print("LLAVE INVALIDA")
        


    client_sock.close()
    server_sock.close()
