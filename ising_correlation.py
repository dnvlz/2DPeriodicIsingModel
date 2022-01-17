import numpy as np
from random import random,randrange
from pylab import plot,ylabel,show,xlabel

N = 20
J = 1
steps = 500000
T = 2

def total_energy(S):
    E_total = 0
    # Definimos la energía total como la suma de las interacciones
    # entre nodos vecinos
    for i in range(N-1):
        E_total -= J*np.sum(S[i,:]*S[i+1,:])
        E_total -= J*np.sum(S[:,i]*S[:,i+1])
    # Condiciones de borde periódicas
    E_total -= J*np.sum(S[N-1,:]*S[0,:])
    E_total -= J*np.sum(S[:,N-1]*S[:,0])
    return E_total

# Termalización: 1000 pasos de Montecarlo
# Definimos nuestro lattice con valores aleatorios entre -1 y 1
S = np.array([np.array([randrange(-1,2,2) for i in range(N)]) for j in range(N)])
# Definimos una lista vacía para almacenar nuestras mediciones de la correlación
corr = np.zeros([N,int(steps/500)-2])
# Calculamos su energía
E = total_energy(S)

# ALGORITMO DE METROPOLIS
# Se escoge un espín aleatorio y se invierte
for k in range(steps):
    i = randrange(N)
    j = randrange(N)
    S[i,j] = -S[i,j]
    E_prime = total_energy(S)
    # Se calcula la modificación en la energía debida al cambio
    dE = E_prime-E
    # Se decide si el movimiento se acepta o no
    # (Este es el corazón de Metropolis)
    if random()<np.exp(-dE/T):
        E += dE
    else:
        S[i,j] = -S[i,j]
    # Termalización: 1000 pasos de Montecarlo
    if (k%500==0) and (k>1000):
        for m in range(N):
            for n in range(N):
                # Implementación de condiciones de frontera
                if (n-m)>=0 and (n+m)<N:
                    corr[m,int(k/500)-2] += S[n,n]*(S[n,n-m]+S[n-m,n]+S[n,n+m]+S[n+m,n])
                elif (n-m)<0 and (n+m)<N:
                    corr[m,int(k/500)-2] += S[n,n]*(S[n,N+(n-m)]+S[N+(n-m),n]+S[n,n+m]+S[n+m,n])
                elif (n-m)>=0 and (n+m)>=N:
                    corr[m,int(k/500)-2] += S[n,n]*(S[n,n-m]+S[n-m,n]+S[n,(n+m)-N]+S[(n+m)-N,n])
                elif (n-m)<0 and (n+m)>=N:
                    corr[m,int(k/500)-2] += S[n,n]*(S[n,N+(n-m)]+S[N+(n-m),n]+S[n,(n+m)-N]+S[(n+m)-N,n])

# Sumamos los valores que obtuvimos para la correlación
# (ya incluyen el factor 1/N^2 con el que se promedia)
correlation = corr.sum(axis=1)/(4*N**2)

#Gráficas
plot(range(1,N),correlation[1:],'.')
ylabel("Correlation")
xlabel("Distance |i-j|")
show()

print(correlation)