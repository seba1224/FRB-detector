import math, time, struct
import numpy as np
import matplotlib.pyplot as plt
import ipdb

def read_dram(fpga, lh, nAddr, data_filename):
    print 'Reading dram data..'
    open(data_filename, 'w').close() # create a empty doc
    f = file(data_filename, 'a')
    start = time.time()
    for i in range(32):
        raw_data = fpga.read_dram(16*nAddr/32, 16*nAddr*i/32)  ##revisar esto!!!
        f.write(raw_data)
    print 'it takes '+str(time.time()-start)+ 'read the dram'
    f.close()
    print 'done'

def parse_data(raw_data_filename, parse_data_file, nAddr):
    fr = file(raw_data_filename, 'r')
    fw = file(parse_data_filename, 'a')
    for i in range(nAddr):
        fr.read(8)
        parse_data = struct.unpack('>1Q', fr.read(8))
        fw.write(parse_data+'\n')
    
    fr.close()
    fw.close()

def plot_data(raw_data_filename, nAddr, channels, Fs):
    fr = file(raw_data_filename, 'r')
    nSpecs = nAddr/channels
    spec_matrix = np.zeros((channels, nSpecs))
    start=time.time()
    print 'plotting data'
    for i in range(nSpecs):
        for j in range(channels):
            fr.read(8)
            parse_data = (struct.unpack('>1Q', fr.read(8)))
	    #ipdb.set_trace()	
            #print(parse_data)
	    power = 10*math.log(int(parse_data[0])+1,10)
            spec_matrix[j, i] = power
            
    fr.close()
    print 'it takes '+str(time.time()-start)+' plotting the dram-data'
    # ipdb.set_trace()
    plt.imshow(spec_matrix, extent=[0, nSpecs*channels/Fs*1.0, Fs, 0]) #revisar q onda los limites de esto
    plt.xlabel('Time[$\mu$s]')
    plt.ylabel('Frequency[MHz]')
    plt.colorbar()
    plt.axes().set_aspect('auto')
    plt.show()
    plt.savefig('spect_dram.pdf', bbox_inches='tight')
    


        
        
