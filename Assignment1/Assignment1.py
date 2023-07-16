import math
import numpy as np

n = 4   #states are labelled 0 to n-1 
M = [[1,0,0,0],[0.5,0,0.5,0],[0,0.2,0,0.8],[0,0,0,1]]
t = 3
i = 1
j = 2

mu = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

mu[i][0] = 1

P = np.identity(n, dtype = float)
for u in range(1,t+1):
    P = np.matmul(P,M)
    print(P)


p_i_j = np.matmul(np.transpose(P),mu)

print(P)
print(mu)
print(p_i_j)
