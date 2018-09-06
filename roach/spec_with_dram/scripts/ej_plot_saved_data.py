from dram_functs import plot_data
nAddr = 2**23
channels = 4096
raw_data_filename = "raw_dram_data_75MSa_acclen4"
bof = 'spec_dram_2.bof'
IP = '192.168.0.11'
Fs = 30 
plot_data(raw_data_filename, nAddr, channels, Fs)   #esto tiene un problema... no considera la acumulacion q se hace al final(acc_len)..
						    #los tiempos del plot estan malos
