import rasterio
import pyopencl as cl
import pyopencl.tools as cltools
import pyopencl.array as cl_array
import numpy as np
import time

ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)

# Import bands as separate images; in /project2/macs30123 on Midway2
band4 = rasterio.open('/project2/macs30123/landsat8/LC08_B4.tif') #red
band5 = rasterio.open('/project2/macs30123/landsat8/LC08_B5.tif') #nir
# Convert nir and red objects to float64 arrays
red = band4.read(1).astype('float64')
nir = band5.read(1).astype('float64')

# Tile arrays to simulate additional data (10x)
red = np.tile(red, 10)
nir = np.tile(nir, 10)

# NDVI calculation - seriel
t0 = time.time()
ndvi_s = (nir - red) / (nir + red)
t_s = time.time() - t0

# NDVI calculation - Opencl
t0 = time.time()
red_p = cl_array.to_device(queue,red)
nir_p = cl_array.to_device(queue,nir)
ndvi = (red_p - nir_p)/(red_p + nir_p)
ndvi_p = ndvi.get()
t_p = time.time() - t0

print ('seriel code took', t_s, 'seconds', 'Opencl code took', t_p, 'seconds')
