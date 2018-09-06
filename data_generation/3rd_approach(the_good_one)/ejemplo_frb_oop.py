import frb_oop_2


frb = FRB()
frb.evol_peak(1.5)
frb.plot(frb.t, frb.peak) #la idea es ir revisando q onda el grafico..pa q no de cualquier cosa
frb.set_width_extreme_values(frb.width_i, 0.03)
frb.set_noise(0.2)
frb.generar_datos()
frb.plot()
frb.add_noise()
frb.export_sdg('frb_data')

##tmb hay otras posibilidades como cambiar el nptos, fs, duracion, etc..pero
##estan seteados para usar todos los puntos del generador de fotonica
