from socket import *
import sys

direccion_servidor = "localhost"
puerto_servidor = 9099

# Generar el socket
socket_cliente = socket(AF_INET, SOCK_STREAM)
socket_cliente.connect((direccion_servidor, puerto_servidor))

print("Servidor escuchando en {}:{}...".format(direccion_servidor, puerto_servidor))

while True: 

    mensaje = input()
    if mensaje != "adios":
        socket_cliente.send(mensaje.encode())
        respuesta = socket_cliente.recv(4096).decode()
        print(respuesta)
    else:
        socket_cliente.send(mensaje.encode())
        socket_cliente.close()
        sys.exit()
        


