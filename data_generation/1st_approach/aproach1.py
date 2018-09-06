import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import ipdb

"""valores de prueba"""
# np.random.seed(10)
duracion = 100
N = 1000
DM_index = 2.0
frec_i = 1.5   # ojo q si f_i y f_fin no son floats no funca
frec_fin = 1.2
width_i = 0.0003
width_fin = 0.003
index_width = 4



def frec_spectrum(x, A, mu, sigma, wn_amp):
    output = A*np.exp(-(x-mu)**2/(2*sigma))+wn_amp*np.random.random_sample(len(x))
    return output


def evol_peak(duracion, N, DM_index, frec_i, frec_fin):
    """"Entrega un (t,x) deonde t y x son de un  chirp que varia su frecuencia
    en el tiempo, suponiendo que los FRB siguen t=a/(frec**DM)+b"""
    a = duracion/(1.0/frec_fin**DM_index-1.0/frec_i**DM_index)
    b = -a/(frec_i**2)
    t = np.linspace(0, duracion, N)
    peak = np.sqrt(a/(t-b))
    return [a, b, t, peak]


def evol_width(a, b, width_i, width_f, index_width):
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


[a, b, t, peak] = evol_peak(duracion, N, DM_index, frec_i, frec_fin)
ancho = evol_width(a, b, width_i, width_fin, index_width)
frec = np.linspace(0.5, 2.4, len(t))   # creo un vector de frecuencias en las que se evalua la gaussiana
matrix = np.zeros([len(frec), len(t)])
for i in range(0, len(t)):
    matrix[:, i] = frec_spectrum(frec, 1, peak[i], ancho[i], 0.1)

plt.imshow(matrix, origin=None)
plt.show()


# fig = plt.subplot()
# fig.imshow(matrix, extent=[np.min(t), np.max(t), np.min(frec)*100, np.max(frec)*100], origin='lower')
# fig.set_aspect(1)
# fig.set_ylabel("frec")
# fig.set_xlabel("t")
# plt.show()









#
