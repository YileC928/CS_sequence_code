import numpy as np
import scipy.stats as sts
from numba.pycc import CC
import time
import numba as nb
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

import compile_ar

#start timing
t0 = time.time()

rho = 0.5
mu = 3.0
sigma = 1.0
z_0 = mu

S = 1000 # Set the number of lives to simulate
T = int(4160) # Set the number of periods for each simulation np.random.seed(25)

N = int(S / size)
eps_mat = sts.norm.rvs(loc=0, scale=sigma, size=(T, N))
z_mat = np.zeros((T, N))
#eps_mat = sts.norm.rvs(loc=0, scale=sigma, size=(T, S))
#z_mat = np.zeros((T, S))

sendbuf = np.array(compile_ar.loop_ar(z_mat, eps_mat, N, T, rho, mu, sigma, z_0))
recvbuf = None
if rank == 0:
    recvbuf = np.empty([N * size, T], dtype='float')

comm.Gather(sendbuf, recvbuf, root=0)

if rank == 0:
    time_elapsed = time.time() - t0
    print("simulated", S, "lives in", time_elapsed, "on", size, "MPI processes")


