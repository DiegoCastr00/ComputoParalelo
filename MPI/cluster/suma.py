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


def sum_parcial(arr):
    suma = 0
    for n in arr:
        denominador = 2*n + 1
        suma += 1/denominador
    print(f"Resultado total del set: -> {suma}")
    return suma


comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()


N_THREADS=5
splits = np.array_split(np.arange(1000), N_THREADS)
resutados = []

for split in splits:
    resutados.append(sum_parcial(split))

print(f"Resultado total de la suma: -> {sum(resutados)}")