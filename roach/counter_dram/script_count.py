import corr, struct, time
bof='dram_count2.bof' #ver como se llama...
roachIP='192.168.0.11'   
fpga = corr.katcp_wrapper.FpgaClient('roachIP')
time.sleep(1)
fpga.progdev(bof)
time.sleep(6)


fpga.write_int('enable_count', 1)
fpga.write_int('reset', 0)
fpga.write_int('reset', 1)

while fpga.read_int('done_reg')!=1:
    time.sleep(1)

for i in range(0,10):
    asd = struct.unpack('>2Q',fpga.read_dram(16,16*i)) 
    print(str(i*16) + "+" +str(asd))



"""ej de output
0+(0, 1)
16+(1, 2)
32+(2, 3)
48+(3, 4)
64+(4, 5)
80+(5, 6)
96+(6, 7)
112+(7, 8)
128+(8, 9)
144+(9, 10)

cada 16 bytes estan los datos ;) estoy usando toda la memoria


"""





