import numpy as np
import matplotlib.pyplot as plt
import ipdb

def correlacion_especial(data1, data2, desfase, largo_corr):
    resultado = np.zeros(len(data2))
    for i in range(largo_corr):
	#ipdb.set_trace()
        data1_shift = np.roll(data1,-(desfase+i)) #suponemos q el pulso se mueve en una direccion
        data1_shift[len(data1_shift)-(desfase+i+1):len(data1_shift)-1]=0
        resultado = resultado+data1_shift*data2
    return resultado

def correlate_frb(frb, max_threshold, delta_sweep, search_window):
    """frb=frb[tiempo, frec], max_threshold valor q desencadena una deteccion,
    delta_sweep es cuanto me muevo cr al peak anterior, search_window es el tamano
    de la correlacion que se esta realizando"""
    correlaciones = np.zeros(frb.shape)
    for i in range(1, frb.shape[1]):
        #ipdb.set_trace()
        correlaciones[:,i] = correlacion_especial(frb[:, i-1], frb[:,i],delta_sweep, search_window )
    #ipdb.set_trace()
    suma_corr = np.sum(correlaciones, axis=1)
    valor_corr = np.sum(suma_corr)
    print(valor_corr)
    if valor_corr > max_threshold:
        return [1, valor_corr, correlaciones]
    else:
        return [0, valor_corr, correlaciones]

