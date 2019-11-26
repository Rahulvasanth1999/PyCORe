### test PyCORe

import matplotlib.pyplot as plt
import numpy as np
import sys
#sys.path.append('C:/Users/tikan/Documents/Python Scripts/PyCORe')
sys.path.append('C:/Users/tusnin/Documents/Physics/PhD/epfl/PyCORe')
import PyCORe_main as pcm

Num_of_modes = 512
Tr = 1./18.2e9#2*np.pi*R*c/n0
L = 11.9e-3#c/n0*Tr#
###dispersion
D1 = 2*np.pi*1/Tr
beta2 = -13e-27
D2 = -1*beta2*L/Tr*D1**2 ## From beta2 to D2
D3 = 0
mu = np.arange(-Num_of_modes/2,Num_of_modes/2)
Dint = (mu**2*D2/2 + mu**3*D3/6)

k = 1.75e-5/Tr  #(alpha+theta_ex)/2
alpha = 1.75e-5
gamma = 0.000032 # n2*2*np.pi*f_pump/c/Aeff

dNu_ini = -5e5
dNu_end =5e5
ramp_stop = 0.1
dOm = 2*np.pi*np.concatenate([np.linspace(dNu_ini,dNu_end, int(len(mu)*ramp_stop)),dNu_end*np.ones(int(np.round((1-ramp_stop)*len(mu))))])

PhysicalParameters = {'n0' : 1.37,
                      'n2' : 9e-21,### m^2/W
                      'FSR' : 18.2e9 ,
                      'w0' : 2*np.pi*192e12,
                      'width' : 1.665e-7,
                      'height' : 1.665e-7,
                      'kappa_0' : 1.75e-5/Tr,
                      'kappa_ex' : 1.75e-5/Tr,
                      'Dint' : np.fft.fftshift(Dint)}

simulation_parameters = {'slow_time' : 1e-1,
                         'detuning_array' : dOm,
                         'noise_level' : 1e-7,
                         'output' : 'map',
                         'absolute_tolerance' : 1e-9,
                         'relative_tolerance' : 1e-9,
                         'max_internal_steps' : 20000}

P0 = 55e-3### W
Pump = np.zeros(len(mu),dtype='complex')
Pump[0] = P0
#Pump = np.fft.fftshift(Pump)

Seed = Pump/10000

single_ring = pcm.Resonator(PhysicalParameters, Seed, Pump)

map2d = single_ring.Propagate_SAM(simulation_parameters)
#%%
pcm.Plot_Map(np.fft.fftshift(np.fft.fft(map2d,axis=1),axes=1))