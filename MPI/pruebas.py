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

A = np.random.random((3, 3))
B = np.random.random((3, 3))

print(A.flatten())
print(B.flatten())

procesadores = 2 

subA = nivelacion_cargas(A.flatten(), procesadores)
subB = nivelacion_cargas(B.flatten(), procesadores)

print(subA)
print(subB)

# Restar las matrices
for i in range(2):
    subA[i] = subA[i] - subB[i]

print(subA)