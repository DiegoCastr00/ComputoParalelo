from mpi4py import MPI
import numpy as np

def nivelacion_cargas(D, n_p):
    s=len(D)%n_p
    t=int((len(D)-s)/n_p)
    l_i=0
    l_s=0
    out=[]
    for i in range(n_p):
        if i<s:
            l_i=i*t+i
            l_s=l_i+t+1
        else:
            l_i=i*t+s
            l_s=l_i+t
        out.append(D[l_i:l_s])
    return out

def scatter(data):
    data = nivelacion_cargas(data, size)
    for i in range(1,size):
        comm.send(data[i], dest=i)
    return data[0]

def gather(matrizA, matrizB, rank, size):
    # Aqui se realiza cualquer procedimiento de cada proceso
    result = matrizA - matrizB
    comm.send(result, dest=0)

    if rank == 0:
        # El proceso raíz recibe los resultados de todos los demás procesos
        results = [result]  # Incluimos el resultado del proceso raíz
        for i in range(1, size):
            result_i = comm.recv(source=i)
            results.append(result_i)

        # Convertir la lista de matrices en una matriz 3D
        results = np.array(results)

        # El proceso raíz imprime los resultados
        print(f"resultado \n {results}")

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

A = np.random.random((3, 3))
B = np.random.random((3, 3))

if rank == 0:
    matrizA = scatter(A.flatten())
    matrizB = scatter(B.flatten())

else:
    matrizA = comm.recv(source=0)
    matrizB = comm.recv(source=0)

gather(matrizA, matrizB , rank, size)