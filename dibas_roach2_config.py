#! /usr/bin/python

import corr
import time

#HOST = 'r2d021403.casper.pvt' # 10.0.1.170
HOST = "specdemo" #
#DEST_IP   = (10<<24) + (0<<16) + (1<<8) + (1<<0) #c0a8290a,acme1
DEST_IP   = (10<<24) + (0<<16) + (1<<8) + (12<<0) #peix-RAL
#DEST_MAC  = 0x0cc47aaa8afb #0c:c4:7a:aa:8a:fb, for acme1 eth1
DEST_MAC  = 0x180373e8a68a #18:03:73:e8:a6:8a, for peix-RAL eth0
DEST_PORT = 10000 #4321
ACC_LEN   = 2**12
BOFFILE = 'c960x4096_x14_7_r2013b_frb.bof'

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

# disable test mode
fpga.write_int('tvg_cmult_en',0)

# set barrel shift, shift toward left
fpga.write_int('vacc_shift',30)





