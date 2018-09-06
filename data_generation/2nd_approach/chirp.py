from __future__ import division
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
import scipy.fftpack as fftpack
import ipdb


n_ptos = 10**4
duracion = 1
fs = n_ptos/duracion
tiempo = np.linspace(0, 1, n_ptos)
DM_index = 2.0
frec_i = 4*10**2
frec_fin = 1*10**2
width_i = 0.0003
width_f = 0.003
width_index = 4.0


def evol_peak(duracion, frec_i, frec_fin, DM_index, t):
    # ipdb.set_trace()
    a = duracion/(1.0/frec_fin**DM_index-1.0/frec_i**DM_index)
    print(a)
    b = -a/(frec_i**DM_index)
    print(b)
    peak = (a/(t-b))**(1/DM_index)
    return peak


peak = evol_peak(duracion, frec_i, frec_fin, DM_index, tiempo)
phi = 2*np.pi*np.cumsum(peak)*tiempo
x = np.sin(phi)


f, t, Sxx = signal.spectrogram(x, fs=fs)
plt.figure()
plt.pcolormesh(t, f, 10*np.log10(Sxx))
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.colorbar()
plt.show()
