#! /usr/bin/python

import corr
import time

#HOST = 'r2d021403.casper.pvt' # 10.0.1.170
HOST = "specdemo" # roach2 at green bank
#HOST = 'r2d021403.s6.pvt' # (10.0.1.169) mounted on asa2
#DEST_IP   = (10<<24) + (0<<16) + (1<<8) + (1<<0) #c0a8290a,acme1
#DEST_IP   = (10<<24) + (0<<16) + (1<<8) + (12<<0) #peix-RAL
#DEST_IP   = (10<<24) + (0<<16) + (1<<8) + (63<<0) #snb11
DEST_IP   = (10<<24) + (0<<16) + (1<<8) + (38<<0) #greenburst
#DEST_IP_X0 = (10<<24) + (10<<16) + (12<<8) + 2 # snb11-eth4:10.10.10.4
#DEST_IP_X1 = (10<<24) + (10<<16) + (13<<8) + 3 # snb11-eth4:10.10.10.4
#DEST_IP_X2 = (10<<24) + (10<<16) + (14<<8) + 4 # snb11-eth4:10.10.10.4
#DEST_IP_X3 = (10<<24) + (10<<16) + (15<<8) + 5 # snb11-eth4:10.10.10.4
#DEST_IP_X0 = (10<<24) + (10<<16) + (10<<8) + 2 #
DEST_IP_X1 = (10<<24) + (10<<16) + (10<<8) + 66 # for s6c1 eth3
DEST_IP_X2 = (10<<24) + (10<<16) + (10<<8) + 194 # for s6c1 eth5
DEST_IP_X3 = (10<<24) + (10<<16) + (10<<8) + 67 # for s6c2 eth3
DEST_IP_X4 = (10<<24) + (10<<16) + (10<<8) + 195 # for s6c2 eth5
DEST_IP_X5 = (10<<24) + (10<<16) + (10<<8) + 68 #for s6c3 eth3 
DEST_IP_X6 = (10<<24) + (10<<16) + (10<<8) + 196 # for s6c3 eth5
#DEST_MAC  = 0x0cc47aaa8afb #0c:c4:7a:aa:8a:fb, for acme1 eth1
#DEST_MAC  = 0x180373e8a68a #18:03:73:e8:a6:8a, for peix-RAL eth0
#DEST_MAC  = 0x002590e26904 #00:25:90:e2:69:04, for snb11 eth0
DEST_MAC  = 0x02020a000126 #02:02:0a:00:01:26, for greenburst enp5s0

#DEST_MAC_X0 = 0x02020a0a0a02 #02:02:0a:0a:0a:02, for snb11 eth2
#DEST_MAC_X1 = 0x02020a0a0a03 #02:02:0a:0a:0a:03, for snb11 eth3
#DEST_MAC_X2 = 0x02020a0a0a04 #02:02:0a:0a:0a:04, for snb11 eth4
#DEST_MAC_X3 = 0x02020a0a0a05 #02:02:0a:0a:0a:05, for snb11 eth5
DEST_MAC_X1 = 0x02020a0a0a42 #02:02:0a:0a:0a:42, for s6c1 eth3
DEST_MAC_X2 = 0x02020a0a0ac2 #02:02:0a:0a:0a:c2, for s6c1 eth5
DEST_MAC_X3 = 0x02020a0a0a43 #02:02:0a:0a:0a:43, for s6c2 eth3
DEST_MAC_X4 = 0x02020a0a0ac3 #02:02:0a:0a:0a:c3, for s6c2 eth5
DEST_MAC_X5 = 0x02020a0a0a44 #02:02:0a:0a:0a:44, for s6c3 eth3
DEST_MAC_X6 = 0x02020a0a0ac4 #02:02:0a:0a:0a:c4, for s6c3 eth5
DEST_PORT = 10000 #4321
DEST_PORT_X = 60000 #ten gbe destination port
ACC_LEN   = 60
BOFFILE = 'c960x4096_x14_7_r2013b_frb.bof'
#BOFFILE = 'c1500x4096_x14_7_2018_Jun_04_1652.bof.gz'
#fabric MAC: hex2dec('123456789abc'), IP adress:167772453, UDP Port:60000
SRC_IP   = (10<<24) + (0<<16) + (1<<8) + (37<<0) # fabric IP adress:167772453
#SRC_IP_X0 = (10<<24) + (10<<16) + (12<<8) + 201
#SRC_IP_X1 = (10<<24) + (10<<16) + (13<<8) + 202
#SRC_IP_X2 = (10<<24) + (10<<16) + (14<<8) + 203
#SRC_IP_X3 = (10<<24) + (10<<16) + (15<<8) + 204
SRC_IP_X1 = (10<<24) + (10<<16) + (12<<8) + 201
SRC_IP_X2 = (10<<24) + (10<<16) + (10<<8) + 202
SRC_IP_X3 = (10<<24) + (10<<16) + (10<<8) + 203
SRC_IP_X4 = (10<<24) + (10<<16) + (10<<8) + 204
SRC_IP_X5 = (10<<24) + (10<<16) + (10<<8) + 205
SRC_IP_X6 = (10<<24) + (10<<16) + (10<<8) + 206
SRC_MAC = 0x123456789abc
#SRC_MAC_X0 = 0x0202000010c9
SRC_MAC_X1 = 0x0202000010ca
SRC_MAC_X2 = 0x0202000010cb
SRC_MAC_X3 = 0x0202000010cc
SRC_MAC_X4 = 0x0202000010cd
SRC_MAC_X5 = 0x0202000010ce
SRC_MAC_X6 = 0x0202000010cf
SRC_PORT = 60000 # one GbE source port
SRC_PORT_X = 10000 # ten GbE source port
SRC_PORT_X1 = 10001 # ten GbE source port 1
SRC_PORT_X2 = 10002 # ten GbE source port 2
SRC_PORT_X3 = 10003 # ten GbE source port 3
SRC_PORT_X4 = 10004 # ten GbE source port 4
SRC_PORT_X5 = 10005 # ten GbE source port 5
SRC_PORT_X6 = 10006 # ten GbE source port 6

gbe0 = 'one_GbE_one_GbE'
#gbe_x0 = 'gbe0'
gbe_x1 = 'gbe1'
gbe_x2 = 'gbe2'
gbe_x3 = 'gbe3'
gbe_x4 = 'gbe4'
gbe_x5 = 'gbe5'
gbe_x6 = 'gbe6'
#gbe_x7 = 'gbe7'
print 'Connecting to board:', HOST
fpga = corr.katcp_wrapper.FpgaClient(HOST)
time.sleep(0.1)

print 'Programming!'
fpga.progdev(BOFFILE)
print 'done'

print 'Board clock (in MHz):', fpga.est_brd_clk()

fpga.write_int('reset',1)
try:
	# reset the boards
	fpga.write_int('rst_cpoge', 1)
	
	# config one GbE
	gbe0_link = bool(fpga.read_int(gbe0))
	if not gbe0_link:
		print 'ERROR: There is no cable plugged into port0!'

	fpga.write_int('one_GbE_dest_ip', DEST_IP)
	fpga.write_int('one_GbE_dest_port', DEST_PORT)
	arp_table = [DEST_MAC] * 256
	# Print ARP table
	print '\n===============================\n'
	print '10GbE Transmitter core details:'
	print '\n===============================\n'
	print "Note that for some IP address values, only the lower 8 bits are valid!"
	fpga.print_10gbe_core_details(gbe0, arp=True )
except:
	print "ignore one GbE configuration"
# config xge stuff
#arp_table_x0 = [DEST_MAC_X0] * 256
arp_table_x1 = [DEST_MAC_X1] * 256
arp_table_x2 = [DEST_MAC_X2] * 256
arp_table_x3 = [DEST_MAC_X3] * 256
arp_table_x4 = [DEST_MAC_X4] * 256
arp_table_x5 = [DEST_MAC_X5] * 256
arp_table_x6 = [DEST_MAC_X6] * 256
#arp_table_x7 = [DEST_MAC_X7] * 256
#fpga.write_int('ip_0', DEST_IP_X0)
#fpga.write_int('pt_0', DEST_PORT)
fpga.write_int('ip_1', DEST_IP_X1)
fpga.write_int('pt_1', DEST_PORT_X)
fpga.write_int('ip_2', DEST_IP_X2)
fpga.write_int('pt_2', DEST_PORT_X)
fpga.write_int('ip_3', DEST_IP_X3)
fpga.write_int('pt_3', DEST_PORT_X)
fpga.write_int('ip_4', DEST_IP_X4)
fpga.write_int('pt_4', DEST_PORT_X)
fpga.write_int('ip_5', DEST_IP_X5)
fpga.write_int('pt_5', DEST_PORT_X)
fpga.write_int('ip_6', DEST_IP_X6)
fpga.write_int('pt_6', DEST_PORT_X)

#fpga.config_10gbe_core(gbe_x0, SRC_MAC_X0, SRC_IP_X0, SRC_PORT, arp_table_x0)
#fpga.print_10gbe_core_details(gbe_x0, arp=True )
fpga.config_10gbe_core(gbe_x1, SRC_MAC_X1, SRC_IP_X1, SRC_PORT_X, arp_table_x1)
fpga.print_10gbe_core_details(gbe_x1, arp=True )
fpga.config_10gbe_core(gbe_x2, SRC_MAC_X2, SRC_IP_X2, SRC_PORT_X, arp_table_x2)
fpga.print_10gbe_core_details(gbe_x2, arp=True )
fpga.config_10gbe_core(gbe_x3, SRC_MAC_X3, SRC_IP_X3, SRC_PORT_X, arp_table_x3)
fpga.print_10gbe_core_details(gbe_x3, arp=True )
fpga.config_10gbe_core(gbe_x4, SRC_MAC_X4, SRC_IP_X4, SRC_PORT_X, arp_table_x4)
fpga.print_10gbe_core_details(gbe_x4, arp=True )
fpga.config_10gbe_core(gbe_x5, SRC_MAC_X5, SRC_IP_X5, SRC_PORT_X, arp_table_x5)
fpga.print_10gbe_core_details(gbe_x5, arp=True )
fpga.config_10gbe_core(gbe_x6, SRC_MAC_X6, SRC_IP_X6, SRC_PORT_X, arp_table_x6)
fpga.print_10gbe_core_details(gbe_x6, arp=True )
#fpga.config_10gbe_core(gbe_x7, SRC_MAC_X7, SRC_IP_X7, SRC_PORT_X7, arp_table_x7)
#fpga.print_10gbe_core_details(gbe_x7, arp=True )

# Set fft shift
#fpga.fft_shift = 0b011_011_011_011
#fpga.scale_p0 = 0x00180000
#fpga.scale_p1 = 0x00180000
#fpga.write_int('fftshift', 1755) # same with old design
fpga.write_int('fftshift', 8191)
#fpga.write_int('scale_p0', 0x00180000)
#fpga.write_int('scale_p1', 0x00180000)
fpga.write_int('scale_p0', 0x9000000)
fpga.write_int('scale_p1', 0x9000000)

fpga.write_int('n_chan', 12)

print('Issue reset signal...'),
fpga.write_int('reset', 0)
print('done')
# trigger PPS
fpga.write_int('arm', 0)
fpga.write_int('arm', 1)
fpga.write_int('arm', 0)

# software sync, only need when no PPS signal
fpga.write_int('trig',1)
try:
	# Set accumulation length
	fpga.write_int('vacc_acc_len', ACC_LEN)

	# deassert reset
	fpga.write_int('rst_cpoge', 0)

	fpga.write_int('sw_pps', 0)
	fpga.write_int('sw_pps', 1)
	fpga.write_int('sw_pps', 0)
	
	# enable 1gbe output
	fpga.write_int('one_GbE_oge_en', 1)
	
	# disable test mode
	fpga.write_int('tvg_cmult_en',0)
	
	# set barrel shift, shift toward left
	#fpga.write_int('vacc_shift',41) # 
	#fpga.write_int('vacc_shift',50)
	fpga.write_int('vacc_shift',45) # without Notch filter
except:
	print "launch original version B."





