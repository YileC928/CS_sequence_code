import numpy as np
import scipy.stats as sts
from numba.pycc import CC
import time

#first complie the loop
cc = CC('compile_ar')

@cc.export('loop_ar', 'f8[:,:](f8[:,:], f8[:,:], i4, i4, f8, f8, f8, f8)') 
def loop_ar(z_mat, eps_mat, S, T, rho, mu, sigma, z_0):
    for s_ind in range(S):
        z_tm1 = z_0
        for t_ind in range(T):
            e_t = eps_mat[t_ind, s_ind]
            z_t = rho * z_tm1 + (1 - rho) * mu + e_t
            z_mat[t_ind, s_ind] = z_t
            z_tm1 = z_t
    return z_mat

cc.compile()
import compile_ar

#start timing
t0 = time.time()

rho = 0.5
mu = 3.0
sigma = 1.0
z_0 = mu

S = 1000 # Set the number of lives to simulate
T = int(4160) # Set the number of periods for each simulation np.random.seed(25)
eps_mat = sts.norm.rvs(loc=0, scale=sigma, size=(T, S))
z_mat = np.zeros((T, S))

compile_ar.loop_ar(z_mat, eps_mat, S, T, rho, mu, sigma, z_0)

print(time.time() - t0)
