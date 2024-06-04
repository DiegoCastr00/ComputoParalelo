from socket import *
import sys
from sklearn import datasets
from sklearn.model_selection import train_test_split
import json

direccion_servidor = "localhost"
puerto_servidor = 9099

# Generar el socket
socket_cliente = socket(AF_INET, SOCK_STREAM)
socket_cliente.connect((direccion_servidor, puerto_servidor))

print("Servidor escuchando en {}:{}...".format(direccion_servidor, puerto_servidor))

iris = datasets.load_iris()
X = iris.data
y = iris.target

_, X_test, _, y_test = train_test_split(X, y, test_size=0.8, stratify=y)

data = {
'X_test': X_test.tolist(),  
'y_test': y_test.tolist()
}  

# Convertir el diccionario a una cadena JSON
data_json = json.dumps(data)

socket_cliente.send(data_json.encode())

respuesta = socket_cliente.recv(4096).decode()
print(respuesta)

socket_cliente.close()
sys.exit()
        
# /bin/python3 /home/dante/Documentos/6toSemestre/ComputoParalelo/Sockets/Knn/cliente_knn.py
