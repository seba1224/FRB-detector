from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack as fftpack
import ipdb


"""valores de prueba"""
# np.random.seed(10)
duracion = 800
N = 50000
DM_index = 2.0
frec_i = 1.5   # ojo q si f_i y f_fin no son floats no funca
frec_fin = 1.2
width_i = 0.03
width_fin = 3
index_width = 4


def chirp(duracion, N, DM_index, frec_i, frec_fin, desfase, desfase2):
    """"Entrega un (t,x) deonde t y x son de un  chirp que varia su frecuencia
    en el tiempo, suponiendo que los FRB siguen t=a/(frec**DM)+b"""
    a = duracion/(1.0/frec_fin**DM_index-1.0/frec_i**DM_index)
    b = -a/(frec_i**2)
    t = np.linspace(0, duracion, N)
    frec = (a/(t-b))**(1/DM_index)
    """para hacer el chirp se usa q phi = phi_0 + int_0^t (2*pi*f(t)), ya que
    f =1/(2pi) * dphi/dt
    Si se quiere ver hay que usar 1/(2*np.pi)*np.gradient(phi, duracion/N)"""
    phi = 2*np.pi*np.cumsum(frec*duracion/N)
    # plt.plot(1/(2*np.pi)*np.gradient(phi, duracion/N)) # mustra la variacion de frec
    # del chirp
    x = np.sin(phi + desfase*t+desfase2)
    return (a, b, t, x)


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


def gaussian(sigma, t, mu):
    out = np.exp(-(t-mu)**2/(2*sigma**2))
    return out


prueba = chirp(duracion, N, DM_index, frec_i, frec_fin, 0, 2*np.pi*np.random.random())
a = prueba[0]
b = prueba[1]
t = prueba[2]
x = prueba[3]
f_sample = (t[2]-t[1])**-1


ancho = evol_width(a, b, width_i, width_fin, index_width)

"""Testing de la evolucion del ancho (dps hay q convertirlo en una funcion)
La idea es concatenar chirps desfasados talque cumplan los requerimientos del
ancho, esto depende fuertemente de la velocidad de adquisiscion del ADC
y esta dado por el delta_f(q depende del numero de puntos de la ventana en que
se haga la fft) con que se esta trabajando en el script...(OJO PIOJO
que sino puede darse que el ADC cache que hay zonas espaciadas y no lo mida como
continuo)...Importante: los coeficientes q acompanan a los chirps estan sacados
de una distribucion gaussiana centrada en el peak y con
sigma= ancho/(2sqrt(2ln(2)))
"""
# Para plot_frec(x,t,0,'asd')  w=0.021 aprox, y delta_f=0.015


delta_t = duracion*1.0/N
delta_f = 0.015  # esto debiese ser una variable
sigma = ancho/(2*np.sqrt(2*np.log(2)))
chirps_a_agregar = int(np.around(np.max(ancho)/delta_f))
cant_chirps_usada = len(t[np.int(len(t)/2)-np.int(chirps_a_agregar/2):
                          np.int(len(t)/2)+np.int(chirps_a_agregar/2)])
coeficientes = np.zeros([len(t), cant_chirps_usada])

chirps = np.zeros([cant_chirps_usada, len(t)])
desfase_min = -delta_f * cant_chirps_usada/2
final = np.zeros(len(t))
intento2 = np.zeros([cant_chirps_usada, len(t)])
# iteracion para crear los chirps desfasados, 1er indice desfase, 2do indice
# el valor temporal
test = np.zeros(len(t))


# iteracion para encontrar coeficientes
# el 1er index es el tiempo en que se calculan los coef, el 2do es el valor del
# coef del chirp desfasado.
for i in range(0, len(t), 1):
    coeficientes[i, :] = gaussian(sigma[i], t[np.int(len(t)/2)-np.int(chirps_a_agregar/2):
                                              np.int(len(t)/2)+np.int(chirps_a_agregar/2)],
                                  t[np.int(len(t)/2)])

for i in range(0, cant_chirps_usada):
    chirps[i, :] = chirp(duracion, N, DM_index, frec_i, frec_fin, desfase_min +
                         delta_f*i, np.random.random()*2*np.pi)[3]
    intento2[i, :] = chirps[i, :]*coeficientes[:, i]

    # calculo de cada valor temporal
#    for j in range(0, cant_chirps_usada, 1):
#        final[i] = final[i] + coeficientes[i, j] * chirps[j, i] #parece q esto no esta funcando







#    dist_normal = gaussian(sigma[i], t, t[np.int(len(t)/2)])
#    coeficientes[i, :] = dist_normal[np.int(len(t)/2)-np.int(chirps_a_agregar/2):
#                                     np.int(len(t)/2)+np.int(chirps_a_agregar/2)]









"""for i in range(0, 10, 1):
    chirps_a_sumar = int(ancho[1000:i]/delta_t)
    if (chirps_a_sumar == 0):
        continue
    else:
        if cant_chirp_anterior == chirps_a_sumar:
            continue
        else:
            for i in range(chirps_a_sumar, 0, -1):
                chirp_final[i] =

        cant_chirp_anterior = chirps_a_sumar
"""


# prueba del ancho
prueba_ancho = np.zeros([5000, 5000])
for i in range(0, 4999, 1):
    prueba_ancho[i, :] = gaussian(ancho[i*10], t[0:5000], 40)
plt.plot(t[0:5000], prueba_ancho[4999, :])





def plot_frec(x, t, index, label):
    """index es un parametro de la evolucion del chirp en el tiempo"""
    asd = x[5000*index:5000*index+4096]
    zxc = fftpack.fft(asd)
    n = len(asd)
    xf = np.linspace(0.0, int(1.0/2.0*f_sample), int(n/2))
    plt.plot(xf, 2.0/n * np.abs(zxc[:int(n//2)]), label=label)



def rapido(desfase, index):
    """plot rapido del chirp con desfase"""
    temp = chirp(duracion, N, DM_index, frec_i, frec_fin, desfase)
    xi = temp[3]
    ti = temp[2]
    plot_frec(xi, ti, index, 'rapido %d' % desfase)


"""
i = 0
# variacion temporal peak del chirp
plt.figure()
while(i < 9):
    asd = x[5000*i:5000*i+4096]
    zxc = fftpack.fft(asd)
    N = len(asd)
    xf = np.linspace(0.0, 1.0/2.0*f_sample, N/2)
    plt.plot(xf, 2.0/N * np.abs(zxc[:N//2]), label="%d" % (i))
    i = i + 1
plt.show()
plt.legend

"""
# espectrograma hechizo, falta ver a que tiempo corresponde cada iteracion


def espectrograma(input):
    i = 0
    matrix = np.zeros([460, 2048])
    while(i < 460):
        # asd = x[100*i:100*i+4096]
        print i
        asd = input[50, 100*i:100*i+4096]
        zxc = fftpack.fft(asd)
        n = len(asd)
        matrix[i, :] = 2.0/n * np.abs(zxc[:n//2])
        i = i + 1
    plt.figure()
    plt.imshow(np.transpose(matrix[:, :150]), origin='lower')
    plt.show()


"""
# prueba evolucion temporal
sigma_test = np.zeros(98)
for i in range(0, 98, 1):
    sigma_test[i] = evol_width(a, b, 0.5, 3, t[500*i], index_width)
"""
