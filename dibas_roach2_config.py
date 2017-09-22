#! /usr/bin/python

import corr
import time

HOST = 'r2d021403.casper.pvt' # 10.0.1.170
#DEST_IP   = (10<<24) + (0<<16) + (1<<8) + (1<<0) #c0a8290a,acme1
DEST_IP   = (10<<24) + (0<<16) + (1<<8) + (12<<0) #peix-RAL
#DEST_IP   = (10<<24) + (0<<16) + (1<<8) + (63<<0) #c0a8290a,s6c0
DEST_MAC  = 0x0cc47aaa8afb #0c:c4:7a:aa:8a:fb, for acme1 eth1
DEST_MAC  = 0x180373e8a68a #18:03:73:e8:a6:8a, for peix-RAL eth0
#DEST_MAC  = 0x002590e26905 #00:25:90:e2:69:05, snb11 eno2
DEST_PORT = 10000 #4321
ACC_LEN   = 2**12
#BOFFILE = 'ctrl_1gbe_0810_2017_Aug_25_1056.bof'
#BOFFILE = 'frb_roach2_20170828_2017_Sep_05_0916.bof'
#BOFFILE = 'c1500x4096_x14_7_0828_2017_Sep_01_1433.bof'
#BOFFILE = 'c1500x4096_x14_7_0828_2017_Sep_08_1055.bof'
#BOFFILE = 'frb_1gbe_nodelay_pfb_2017_Sep_15_1124.bof'
#BOFFILE = 'frb_1gbe_nodelay_all_2017_Sep_15_1140.bof'
#BOFFILE = 'frb_1gbe_960_twodelay_2017_Sep_18_0937.bof'
#BOFFILE = 'frb_1gbe_1080_2017_Sep_18_1339.bof'
#BOFFILE = 'c960x4096_x14_7_lessdelay_2017_Sep_20_1234.bof'
BOFFILE = 'c960x4096_x14_7_lessdelay_2017_Sep_20_1648.bof'

#fabric MAC: hex2dec('123456789abc'), IP adress:167772453, UDP Port:60000
SRC_IP   = (10<<24) + (0<<16) + (1<<8) + (37<<0) # fabric IP adress:167772453
SRC_MAC = 0x123456789abc
SRC_PORT = 60000

gbe0 = 'one_GbE_one_GbE'
print 'Connecting to board:', HOST
fpga = corr.katcp_wrapper.FpgaClient(HOST)
time.sleep(0.1)

print 'Programming!'
fpga.progdev(BOFFILE)
print 'done'

print 'Board clock (in MHz):', fpga.est_brd_clk()

# reset the boards
fpga.write_int('rst_cpoge', 1)

gbe0_link = bool(fpga.read_int(gbe0))
if not gbe0_link:
	print 'ERROR: There is no cable plugged into port0!'

# configure tge stuff
fpga.write_int('one_GbE_dest_ip', DEST_IP)
fpga.write_int('one_GbE_dest_port', DEST_PORT)


arp_table = [DEST_MAC] * 256

# Print ARP table
print '\n===============================\n'
print '10GbE Transmitter core details:'
print '\n===============================\n'
print "Note that for some IP address values, only the lower 8 bits are valid!"
fpga.print_10gbe_core_details(gbe0, arp=True )

# fpga.config_10gbe_core('eth_one_Gbe', SRC_PORT, SRC_IP, DEST_PORT, DEST_IP, arp_table) #won't work in here since change to one Gb Ethernet

# Set accumulation length
fpga.write_int('vacc_acc_len', ACC_LEN)

# Set fft shift
fpga.write_int('fftshift',8191)

# deassert reset
fpga.write_int('rst_cpoge', 0)

# trigger PPS
fpga.write_int('arm', 0)
fpga.write_int('arm', 1)
fpga.write_int('arm', 0)

# software sync, only need when no PPS signal
fpga.write_int('trig',1)
fpga.write_int('sw_pps', 0)
fpga.write_int('sw_pps', 1)
fpga.write_int('sw_pps', 0)

# enable 10gbe output
fpga.write_int('one_GbE_oge_en', 1)

# enable test mode
fpga.write_int('tvg_cmult_en',1)

# set barrel shift, shift toward left
fpga.write_int('vacc_shift',52)





