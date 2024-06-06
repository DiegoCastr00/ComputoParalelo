from socket import *
import joblib
import json
import numpy as np
direccion_servidor = "localhost"
puerto_servidor = 9090

# Generar el socket
socket_servidor = socket(AF_INET, SOCK_STREAM)
# Enlazar el socket con la dirección y puerto
socket_servidor.bind((direccion_servidor, puerto_servidor))
# Escuchar conexiones
socket_servidor.listen()

print(f"Servidor escuchando en {direccion_servidor}:{puerto_servidor}...")

while True: 
    #establecemos conexion
    conexion, direccion_cliente = socket_servidor.accept()
    print("Conexión establecida con", direccion_cliente)

    #recibimos mensaje
    mensaje_recibido = conexion.recv(4096).decode()
    data = json.loads(mensaje_recibido)

    X_test = np.array(data['X_test'])
    y_test = np.array(data['y_test'])
    
    clf = joblib.load('knn.pkl')

    etiquetas = clf.predict(X_test)

    etiquetas_str = ','.join(map(str, etiquetas))

    conexion.send(etiquetas_str.encode())

    print("Conexión cerrada con", direccion_cliente)
    # Cerramos la conexión
    conexion.close()
        
# /bin/python3 /home/dante/Documentos/6toSemestre/ComputoParalelo/Sockets/Knn/servidor_knn.py