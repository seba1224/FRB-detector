from roach_functs import parse_roach_args, init_roach
from dram_functs import plot_data, read_dram, parse_data
import corr
from math import trunc

nAddr = 2**23
channels = 4096
raw_data_filename = "raw_dram_data"
bof = 'spec_dram_2.bof'
IP = '192.168.0.11'

opt, IP = parse_roach_args(bof, IP)
fpga, lh = init_roach(opt, IP)

Fs = trunc(fpga.est_brd_clk()*4/16)

read_dram(fpga, lh, nAddr, raw_data_filename)

plot_data(raw_data_filename, nAddr, channels, Fs)



