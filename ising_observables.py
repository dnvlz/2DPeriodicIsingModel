import numpy as np
from random import random,randrange
from pylab import plot,ylabel,show,xlabel

# Número de espines en cada dirección
N = 20
J = 1
# Número de pasos de la simulación
steps = 1000000
# Temperatura inicial
T0 = 1


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
# Calculamos su energía
E = total_energy(S)
for k in range(1000):
    # ALGORITMO DE METROPOLIS
    # Se escoge un espín aleatorio y se invierte
    i = randrange(N)
    j = randrange(N)
    S[i,j] = -S[i,j]
    E_prime = total_energy(S)
    # Se calcula la modificación en la energía debida al cambio
    dE = E_prime-E
    # Se decide si el movimiento se acepta o no
    # (Este es el corazón de Metropolis)
    if random()<np.exp(-dE/T0):
        E += dE
    else:
        S[i,j] = -S[i,j]


def observables(T,steps,S): 
    # Aquí guardaremos nuestras configuraciones doradas
    energy,energy_squared = [],[]
    magnetization = []
    E = total_energy(S)
    for k in range(steps):
        # ALGORITMO DE METROPOLIS
        # Se escoge un espín aleatorio y se invierte
        i = randrange(N)
        j = randrange(N)
        S[i,j] = -S[i,j]
        E_prime = total_energy(S)
        dE = E_prime-E
        # Se decide si el movimiento se acepta o no
        # Este es el corazón de Metropolis
        if random()<np.exp(-dE/T):
            E += dE
        else:
            S[i,j] = -S[i,j]
        # Para evitar correlación medimos cada 500 pasos
        if (k%500==0) and (k>1000):
            energy.append(E)
            energy_squared.append(E**2)
            magnetization.append(sum(sum(S)))
    # promediamos los valores obtenidos para definir observables
    cv = (np.average(energy_squared)-np.average(energy)**2)/(T*N**2)
    magnetization_avg = np.average(magnetization)/N**2
    return cv,magnetization_avg


# Magnetización y calor específico a distintas temperaturas
T_axis = np.arange(T0,4.6,0.2)
cv_axis,magnetization_axis = [],[]
for T in T_axis:
    cv,magnetization_avg=observables(T,steps,S)
    cv_axis.append(cv)
    magnetization_axis.append(magnetization_avg)


# Gráficas
plot(T_axis,cv_axis,'.')
ylabel("Specific heat")
xlabel("Temperature")
show()

plot(T_axis,magnetization_axis,'.')
ylabel("Magnetization")
xlabel("Temperature")
show()

print(cv_axis)
print(T_axis)