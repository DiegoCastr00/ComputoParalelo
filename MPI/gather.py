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

def gather(data, rank, size):

    # Aqui se realiza cualquer procedimiento de cada proceso
    # Cada proceso calcula la media de sus propios datos
    mean = np.mean(data)
    print(f"Proceso {rank}: {data}: {mean}")

    # Cada proceso envía su resultado al proceso raíz
    comm.send(mean, dest=0)

    if rank == 0:
        # El proceso raíz recibe los resultados de todos los demás procesos
        means = [mean]  # Incluimos la media del proceso raíz
        for i in range(1, size):
            mean_i = comm.recv(source=i) 
            means.append(mean_i)

        # El proceso raíz calcula la media final
        final_mean = np.mean(means)
        print(f"Media final: {final_mean}")

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

data = np.arange(100000000)

if rank == 0: 
    own_data = scatter(data)
else:
    own_data = comm.recv(source=0)

gather(own_data, rank, size)