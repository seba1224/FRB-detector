from __future__ import division
from time import time
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import pandas as pd
import ipdb


class FRB(object):
    """Usar los metodos para cambiar los valores de los atributos ptos, duracion, fs, fft_size y ntaps...estan todos relacionados."""
    def __init__(self):
        """Por defecto la duracion es de 1seg, con 8Mptos un sweep de [3.5M-1M]
importante: el ruido es c/r al del maximo de la segnal... ojo!"""
        self.nptos = 8.0*10**6
        self.duracion = 1.0
        self.fs = self.nptos/self.duracion
        self.ntaps = 1001
        self.fft_size = np.floor(np.sqrt(2*(self.nptos+self.ntaps-1)))
        self.DM_index = 2.0
        self.frec_i = 7.0*10**6
        self.frec_fin = 2.0*10**6
        self.width_i = 0.0003
        self.width_fin = 0.003
        self.width_index = 4.0
        self.noise = 0

    def set_nptos(self, ptos_new):
        self.nptos = ptos_new
        self.fs = self.nptos/self.duracion
        self.fft_size = np.floor(np.sqrt(2*(self.nptos+self.ntaps-1)))
        print("your sample frec is %f[Hz] considere change your range of frec" % (self.fs) +
              " sweeping \nif its over the half of this value")

    def set_duracion(self, duracion_new):
        self.duracion = duracion_new
        self.fs = self.nptos/self.duracion
        print("your sample frec is %f[Hz] considere change your range of frec" % (self.fs) +
              " sweeping \nif its over the half of this value")

    def set_fs(self, fs_new):
        self.fs = fs_new
        self.duracion = self.nptos/self.fs
        print("the frb duration is now %f [s]" % self.duracion)

    def set_frec_sweep(self, frec_i_new, frec_fin_new):
        if frec_i_new > self.fs/2 or frec_fin_new > self.fs/2:
            print("Your frec is above the fs/2....")
        else:
            self.frec_i = 2*frec_i_new
            self.frec_fin = 2*frec_fin_new

    def set_width_extreme_values(self, width_i_new, width_fin_new):
        """El width se corresponde con la desviacion de una gaussiana"""
        self.width_i = width_i_new
        self.width_fin = width_fin_new

    def set_noise(self, noise_new):
        self.noise = noise_new

    def evol_peak(self, factor_escala):
        """Suponiendo que los FRB siguen t = a/(frec**DM)+b genera un ajuste
        entrega la posicion de peak en un tiempo dado y tambien entrega los coef
        del ajuste."""
        """Se utiliza ademas un factor de escala, para ver la inclinacion de la
        curva..."""
        duracion = self.duracion*factor_escala
        nptos = int(self.nptos*factor_escala)
        frec_fin = factor_escala*self.frec_fin
        self.__a = duracion/(1.0/frec_fin**self.DM_index -
                             1.0/self.frec_i**self.DM_index)
        self.__b = -self.__a/(self.frec_i**self.DM_index)
        t = np.linspace(0, duracion, nptos)
        peak = (self.__a/(t-self.__b))**(1/self.DM_index)
        self.t = t[0:int(nptos/factor_escala)]
        self.peak = peak[0:int(nptos/factor_escala)]

    
    def DM_real(self):
        """DM en cm**-3 * pc"""
        k_dm = 4140.0
        DM_real = (self.t[0]-self.t[-1])/(k_dm*(((self.peak[0]/(10**6))**-2)-(self.peak[-1]/(10**6))**-2))
        return DM_real       
    
    def evol_width(self):
        """Suponiendo que los FRB siguen w=c/(f**width_index)+d
        calcula la evolucion temporal del width, tmb entrega los coef usados
        ***se necesita haber calculado la evolucion del peak antes***   """
        self.__c = (self.width_i-self.width_fin)/(1/self.frec_i**self.width_index -
                                                  1/self.frec_fin**self.width_index)
        self.__d = self.width_i - self.__c/(self.frec_i**self.width_index)
        self.ancho = self.__c/(self.peak**self.width_index)+self.__d

    def generar_datos(self):
        """Se recomienda revisar todas las variables involucradas, xq se puede
        demorar un buen rato.."""
        rand_signal = np.random.normal(size=int(self.nptos+self.ntaps))  # gaussian: mu=0, sigma=1
        filt_signal = np.zeros(int(self.nptos))
        start_time = time()
        for i, cfreq, width in zip(range(int(self.nptos)), self.peak, self.ancho):
            # ipdb.set_trace()
            # print([round(i/int(self.nptos)*100.0, 2), cfreq, width])
            fir = signal.firwin(self.ntaps, [cfreq - width/2, cfreq+width/2], pass_zero=False, nyq=self.fs)
            aux = np.dot(fir, rand_signal[i:i+self.ntaps])
            filt_signal[i] = aux
        print("Time:" + str(time()-start_time))
        self.signal = filt_signal  # + self.noise*np.max(filt_signal)*np.random.normal(size=int(self.nptos)) ?


    def add_noise(self):
        self.signal = self.signal +  self.noise*np.max(self.signal)*np.random.normal(size=int(self.nptos))

    def plot(self):
        f, t, self.Sxx = signal.spectrogram(self.signal, nperseg=int(self.fft_size), fs=int(self.fs))
        plt.figure()
        plt.pcolormesh(t, f, 10*np.log10(self.Sxx))
        plt.ylabel('Frequency[Hz]')
        plt.xlabel('Time[sec]')
        plt.colorbar()
        plt.show()

    def export_sdg(self, name_file):
        largo_data = ["data length", self.nptos]
        freq = ["frequency", self.fs]  # En vola esto hay q modificarlo xq es con q frec se repite la senal....no se en vdd..
        amplitud = ["amp", 0.020000000]  # Esta seteado en mV
        off = ["offset", 0.000000000]
        pha = ["phase", 0.000000000]
        aux = np.array([largo_data, freq, amplitud, off, pha])
        df = pd.DataFrame(aux)
        df.to_csv(name_file, header=False, index=False, mode='a')
        blank = np.array([None, None, None, None, None, None, None])
        df = pd.DataFrame(blank)
        df.to_csv(name_file, header=False, index=False, mode='a', na_rep=None)  # igual hayq entrar a borrar esto..
        head = ["xpos", "value"]
        df = pd.DataFrame(np.array([head]))
        df.to_csv(name_file, header=False, index=False, mode='a')
        data = np.array([self.t, self.signal])
        df = pd.DataFrame(np.transpose(data))
        df.to_csv(name_file, header=False, index=False, mode='a')
