from vpython import sphere,color,rate,vector
from numpy import empty,zeros,array,exp,pi
from random import random,randrange

N = 20
S = array([array([randrange(-1,2,2) for i in range(N)]) for j in range(N)]) 
J = 1
T = 1
steps = 1000000

def total_energy(S):
    E_total = 0
    # We define the total energy as the sum of interaction energy
    # between adjacent nodes
    for i in range(N-1):
        E_total -= J*sum(S[i,:]*S[i+1,:])
        E_total -= J*sum(S[:,i]*S[:,i+1])
    E_total -= J*sum(S[N-1,:]*S[0,:])
    E_total -= J*sum(S[:,N-1]*S[:,0])
    return E_total

E = total_energy(S)
spins = empty([N,N],sphere)
# If spin up: red. If spin down: blue
colors = [0,color.red,color.blue]
for i in range(N):
    for j in range(N):
        spins[i,j] = sphere(pos=vector(i-N/2,j-N/2,0),radius=0.5,color=colors[S[i,j]])

for k in range(steps):
    # Choose the particle and the move
    i = randrange(N)
    j = randrange(N)
    S[i,j] = -S[i,j]
    E_prime = total_energy(S)
    dE = E_prime-E
    rate(200)
    # Decide whether to accept the move
    if random()<exp(-dE/T):
        E += dE
        # Changes color because S[i,j] became its negative
        spins[i,j].color = colors[S[i,j]]
    else:
        S[i,j] = -S[i,j]

