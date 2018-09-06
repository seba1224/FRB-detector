import sys, corr, logging, time, struct
from optparse import OptionParser
from itertools import chain, izip
import ipdb


katcp_port = 7147

def parse_roach_args(bof, default_IP):
    p = OptionParser()
    p.set_usage('spectrometer.py <ROACH_HOSTNAME_or_IP>[options]')
    p.set_description(__doc__) #aca deberia ir referenciado al doc..creo
    p.add_option('-l', '--acc_len', dest='acc_len', type='int', default=2**5,
        help='Set the number of vectors to accumulate between dumps.')
    p.add_option('-s', '--skip', dest='skip', action='store_true', help='skip re-programming FPGA and configuring EQ')
    p.add_option('-b', '--bof', dest='boffile', type='string', default=bof, help='specify the bof file to load')
    opts, args = p.parse_args(sys.argv[1:])
    if args==[]:
        print 'Using default IP'+ default_IP + '.'
        args.append(default_IP)
    return opts, args[0]

def init_roach(opts, roach):
    lh = corr.log_handlers.DebugLogHandler()
    logger = logging.getLogger(roach)
    logger.addHandler(lh)
    logger.setLevel(10)
    print('connecting to server %s on port %i..'%(roach, katcp_port)),
    fpga = corr.katcp_wrapper.FpgaClient(roach, katcp_port, timeout=10, logger=logger)
    time.sleep(1)
    try:
        if fpga.is_connected():
            print 'ok \n'
        else:
            print 'Error connecting to the server %s on port %i\n' %(roach, katcp_port)
        print '--------\n'
        print 'Programming Fpga with %s..'%opts.boffile,
        if not opts.skip:
            fpga.progdev(opts.boffile)
            print 'done'
        else:
            print 'skipped'
        print 'Configurating accumulation period...'
	#ipdb.set_trace()
        fpga.write_int('acc_len', opts.acc_len)
        print 'done\n'
        
        print 'Reseting counters and freeze_cntr'
        fpga.write_int('reset_counter', 1)
        fpga.write_int('cnt_rst', 1)
        fpga.write_int('reset_counter', 0)
        fpga.write_int('cnt_rst', 0)
	print 'done\n'

    except KeyboardInterrupt:
        exit_clean()
    except:
        exit_fail()
    return fpga, lh


def exit_clean():
    try:
        fpga.stop()
    except: pass
    sys.exit()

def exit_fail():
    print 'Failure detected. Log entries: \n', lh.printMessages()
    try:
        fpga.stop()
    except: pass
    raise
    sys.exit()
        
