
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


def sum_parcial(arr, rank):
    suma = 0
    for n in arr:
        denominador = 2*n + 1
        suma += 1/denominador
    print(f"Rank: {rank} Resultado: -> {suma}")
    return suma

def gather(data, rank, size):
    result = sum_parcial(data, rank)
    comm.send(result, dest=0)

    if rank == 0:
        results = [result]  # Incluimos el resultado del proceso raíz
        for i in range(1, size):
            result_i = comm.recv(source=i)
            results.append(result_i)

        results = np.array(results)
        print(f"resultado: {sum(results)}")

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

data = np.arange(100000)

if rank == 0:
    split = scatter(data)
else:
    split = comm.recv(source=0)

gather(split , rank, size)

#  mpiexec -n 4 "/usr/bin/python3" suma.py