from socket import *

direccion_servidor = "localhost"
puerto_servidor = 9099

# Generar el socket
socket_servidor = socket(AF_INET, SOCK_STREAM)
# Enlazar el socket con la dirección y puerto
socket_servidor.bind((direccion_servidor, puerto_servidor))
# Escuchar conexiones
socket_servidor.listen()

print("Servidor escuchando en {}:{}...".format(direccion_servidor, puerto_servidor))

while True: 
    #establecemos conexion
    conexion, direccion_cliente = socket_servidor.accept()
    print("Conexión establecida con", direccion_cliente)

    while True: 
        #recibimos mensaje
        mensaje_recibido = conexion.recv(4096).decode()
        print(mensaje_recibido)

        if mensaje_recibido == "adios":
            break
        
        conexion.send(input().encode())
    
    print("Conexión cerrada con", direccion_cliente)
    # Cerramos la conexión
    conexion.close()
        