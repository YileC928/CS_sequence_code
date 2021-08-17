import numpy as np
import scipy.stats as sts
from numba.pycc import CC
import numba as nb
import time
from mpi4py import MPI
import matplotlib.pyplot as plt

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

#pre-complie loops
cc = CC('compile_loop')

@nb.njit
@cc.export('sum_', 'f8(f8[:])')
def sum_(a):
    s = 0
    for i in a:
        s += i
    return s

@cc.export('get_rho_t_pairs', 'f8[:, :](f8[:,:], f8[:,:], i4, i4, f8[:], f8, f8, f8)')
def get_rho_t_pairs(z_mat, eps_mat, S, T, rho_all, mu, sigma, z_0):
    rho_t_pairs = []
    for rho in rho_all:
        t_neg = []
        for s_ind in range(S):
            z_tm1 = z_0
            for t_ind in range(T):
                e_t = eps_mat[t_ind, s_ind]
                z_t = rho * z_tm1 + (1 - rho) * mu + e_t
                if z_t <= 0:
                    t_neg.append(t_ind)
                    break
                else:
                    z_mat[t_ind, s_ind] = z_t
                    z_tm1 = z_t
        avg_t_neg = sum_(t_neg)/len(t_neg)
        pair = (rho, avg_t_neg)
        rho_t_pairs.append(pair)
    
    return np.array(rho_t_pairs)

cc.compile()

#start timing
t0 = time.time()

rho_all = np.linspace(-0.95, 0.95, 200)
mu = 3.0
sigma = 1.0
z_0 = mu - 3*sigma
N = int(200/size)
rho_used = rho_all[range(N*rank,N*(rank+1))]

# Set simulation parameters, draw all idiosyncratic random shocks, # and create empty containers
S = 1000 # Set the number of lives to simulate
T = int(4160) # Set the number of periods for each simulation np.random.seed(25)
eps_mat = sts.norm.rvs(loc=0, scale=sigma, size=(T, S))
z_mat = np.zeros((T, S))

import compile_loop
rho_t_pairs = compile_loop.get_rho_t_pairs(z_mat, eps_mat, S, T, rho_used, mu, sigma, z_0)

pairs_all = None
if rank == 0:
    pairs_all = np.empty([200, 2], dtype = 'float')

comm.Gather(sendbuf = rho_t_pairs, recvbuf = pairs_all, root = 0)

if rank == 0:
    x = pairs_all[:,0]
    y = pairs_all[:,1]

    print("maximum avg t for a first negative zt:", np.max(y))
    print("corresponding rho", pairs_all[pairs_all[:, 1] == np.max(y)][0,0])
    print("it takes", time.time() - t0, "seconds")
    plt.plot(x, y)
    plt.savefig("plot_a1_2b")
