import numpy as np
import matplotlib.pyplot as plt
from function import correlacion_especial, correlate_frb


frb_clean = np.loadtxt('data_75_clean_onefrb')
frb_noisy = np.loadtxt('data_08_noise_onefrb')
chirp = np.loadtxt('chirp_lineal')
seno_noisy = np.loadtxt('sin_sucio.txt')
seno_clean = np.loadtxt('sin_clean')

one_frb_clean = frb_clean[1:-1, 60:839]   #elimino la componente DC
one_frb_noisy = frb_noisy[1:-1, 755:1505]

#renormalize 

max_chirp = np.amax(chirp, axis=0)
for i in range(len(max_chirp)):
    chirp[:,i] = chirp[:,i]/max_chirp[i]

max_seno_noisy = np.amax(seno_noisy, axis=0)
for i in range(len(max_seno_noisy)):
    seno_noisy[:,i] =  seno_noisy[:,i]/max_seno_noisy[i]

max_seno_clean = np.amax(seno_clean, axis=0)
for i in range(len(max_seno_clean)):
    seno_clean[:,i] = seno_clean[:,i]/max_seno_clean[i]

max_frb_clean = np.amax(one_frb_clean, axis=0)
for i in range(len(max_frb_clean)):
    one_frb_clean[:,i] = one_frb_clean[:,i]/max_frb_clean[i]

max_frb_noisy = np.amax(one_frb_noisy, axis=0)
for i in range(len(max_frb_noisy)):
    one_frb_noisy[:,i] = one_frb_noisy[:,i]/max_frb_noisy[i]




# setting threshold
desfase = 5
largo_corr =20
threshold_detection = 10


[det_chirp, val_chirp, spect_chirp] = correlate_frb(chirp, threshold_detection, desfase, largo_corr)
[det_seno_noisy, val_seno_noisy, spect_seno_noisy] = correlate_frb(seno_noisy, threshold_detection, desfase, largo_corr)
[det_seno_clean, val_seno_clean, spect_seno_clean] = correlate_frb(seno_clean, threshold_detection, desfase, largo_corr)
[det_frb_clean, val_frb_clean, spect_frb_clean] = correlate_frb(one_frb_clean, threshold_detection, desfase, largo_corr)
[det_frb_noisy, val_frb_noisy, spect_frb_noisy] = correlate_frb(one_frb_noisy, threshold_detection, desfase, largo_corr)



#plots
plt.figure()
plt.plot(np.sum(spect_chirp/spect_chirp.shape[0], axis=1))
plt.title('linear chirp')
plt.ylabel('voltage[au]')
plt.xlabel('spectral channels')
plt.figure()
plt.plot(np.sum(spect_seno_clean/spect_seno_clean.shape[0], axis=1))
plt.title('sin without noise')
plt.xlabel('spectral channels')
plt.ylabel('voltage[au]')
plt.figure()
plt.plot(np.sum(spect_seno_noisy/spect_seno_noisy.shape[0], axis=1))
plt.title('sin + noise')
plt.xlabel('spectral channels')
plt.ylabel('votage[au]')
plt.figure()
plt.plot(np.sum(spect_frb_clean/spect_frb_clean.shape[0], axis=1))
plt.title('frb clean')
plt.xlabel('spectral channels')
plt.ylabel('voltage[au]')
plt.figure()
plt.plot(np.sum(spect_frb_noisy/spect_frb_noisy.shape[0], axis=1))
plt.title('frb noisy')
plt.ylabel('voltage[au]')
plt.xlabel('spectral channels')
plt.show()

print('ponderacion con intervalos de tiempo integrados: \n')
print('chirp: %f') % (val_chirp/spect_chirp.shape[1])
print('seno clean:%f')  % (val_seno_clean/spect_seno_clean.shape[1])
print('seno noisy:%f') % (val_seno_noisy/spect_seno_noisy.shape[1])
print('frb clean: %f') % (val_frb_clean/spect_frb_clean.shape[1])
print('frb noise: %f') % (val_frb_noisy/spect_frb_noisy.shape[1])



