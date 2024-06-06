from socket import *
import sys
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

import json

direccion_servidor = "localhost"
puerto_servidor = 9090

socket_cliente = socket(AF_INET, SOCK_STREAM)
socket_cliente.connect((direccion_servidor, puerto_servidor))
print(f"Servidor escuchando en {direccion_servidor}:{puerto_servidor}...")


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

etiquetas_predichas = list(map(int, respuesta.split(',')))
score = accuracy_score(y_test, etiquetas_predichas)

for x_test, etiqueta in zip(X_test, etiquetas_predichas):
    print(f"data:{x_test}, etiqueta predicha: {etiqueta}")

print(f"\n accuaracy obtenido: {score}") 

socket_cliente.close()
sys.exit()
        
# /bin/python3 /home/dante/Documentos/6toSemestre/ComputoParalelo/Sockets/Knn/cliente_knn.py
