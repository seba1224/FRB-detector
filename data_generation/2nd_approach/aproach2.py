import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
import scipy.fftpack as fftpack
import ipdb

np.random.seed(10)
duracion = 800
delta_t = 50000
DM_index = 2.0
frec_i = 1.5   # ojo q si f_i y f_fin no son floats no funca
frec_fin = 1.2
"""tomo t=a*f**-2 + b , la idea es dps hacerlo mas gral"""
a = duracion/(1/frec_fin**DM_index-1/frec_i**DM_index)
b = -a/(frec_i**2)
t = np.linspace(0, duracion, delta_t)


def peak_de_frec(a, b, t):
    """Entrega el valor del peak de frec para un t dado"""
    out = np.sqrt(a/(t-b))
    return out


"""para hacer el chirp se usa q phi = phi_0 + int_0^t (2*pi*f(t)), ya que
f =1/(2pi) * dphi/dt
Si se quiere ver hay que usar 1/(2*np.pi)*np.gradient(phi, duracion/delta_t)"""
phi = 2*np.pi*np.cumsum(peak_de_frec(a, b, t))*duracion/delta_t
x = np.sin(phi)
# plt.plot(t, x)
# plt.show()

f_sample = (t[2]-t[1])**-1


"""
Hay que revisar como usar la funcion spectrogram, xq la resolucion espectral esta pesima
f, tiempo, sxx = signal.spectrogram(x, f_sample)
plt.pcolormesh(tiempo, f, sxx)

"""
"""
# Prueba chirp
i = 0

while(i < 9):
    asd = x[5000*i:5000*i+4096]
    zxc = fftpack.fft(asd)
    N = len(asd)
    xf = np.linspace(0.0, 1.0/2.0*f_sample, N/2)
    plt.plot(xf, 2.0/N * np.abs(zxc[:N//2]), label="%d" % (i))
    i = i + 1
plt.show()
"""
# Espectrograma hechizo
i = 0
matrix = np.zeros([460, 2048])
while(i < 460):
    asd = x[100*i:100*i+4096]
    zxc = fftpack.fft(asd)
    N = len(asd)
    matrix[i, :] = 2.0/N * np.abs(zxc[:N//2])
    i = i + 1
    # print(len(asd))
    # print(i)
plt.imshow(np.transpose(matrix[:, :150]), origin='lower')
plt.show()

asd = plt.figure()
plt.plot(peak_de_frec(a, b, t))


# evolucion de width


def evol_width(width_i, width_f, t, index_width):
    """Entrega distintos valores de width dependiendo del tiempo que se le
    ingrese. Usa que w = c((a/(t-b))**(1/DM_ind))**index_wifth + d
     Antes de usar esta funcion se debe haber sacado a,b de la
    dependencia del DM"""
    # ipdb.set_trace()

    c_var = (width_i - width_f)/((((a/-b)**(1/DM_index))**(-index_width)) -
                                 ((a/(duracion-b))**(1/DM_index))**(-index_width))
    d_var = width_i - c_var*(((a/-b)**(1/DM_index))**(-index_width))
    ancho = c_var*(((a/(t-b))**(1/DM_index))**(-index_width)) + d_var
    return ancho


def gaussian(sigma, t, mu):
    out = np.exp(-(t-mu)**2/(2*sigma**2))
    return out


"""
# prueba evolucion temporal
for i in range(0, 100, 2):
    sigma_test = evol_width(0.5, 3, t[5000*i], index_width)
    gaussian(sigma_test, t, 0)/max(sigma_test, t, 0)
"""
