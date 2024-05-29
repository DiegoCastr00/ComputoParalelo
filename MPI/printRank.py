from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

print('Hi I am rank number:', rank)
print('Size:', size)

# para correrlo usamos lo siguiente: 
#  mpiexec -n 6 "/usr/bin/python3" printRank.py