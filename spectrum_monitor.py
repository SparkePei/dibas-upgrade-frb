#! /usr/bin/python
import socket,pylab,matplotlib,math,corr,array
import struct
import time
import numpy as np

frame_len = 768
n_frame_per_spec = 16
spec_len = 4096
data_size_per_frame = spec_len/n_frame_per_spec
xx = spec_len*[0]
yy = spec_len*[0]
acclen=0
gain=0

HOST = 'specdemo'
#yy_tmp=data_size_per_frame*[0]
#data_tmp=data_size_per_frame*2*[0]
#header_tmp=(frame_len-data_size_per_frame)*[0]

def get_data():
	gain=fpga.read_int('vacc_shift')

	acclen=fpga.read_int('vacc_acc_len')/256
	n_bytes_per_spec = 0
	# each spectrum has multi packets, receive data and reorder it
	for i in range(0,n_frame_per_spec):
		#print "grab number",i,"packet done!"
		data, addr = sock.recvfrom(frame_len)
		frame_tmp = struct.unpack('<'+str(len(data))+'B',data)
		n_bytes_per_spec += len(data)
		# packets format is (header,power of x, power of y), each has 1 Byte
		header_tmp = frame_tmp[0::3]
		xx_tmp = frame_tmp[1::3]
		yy_tmp = frame_tmp[2::3]
		#print xx_tmp
		#print yy_tmp
		# use 8 bytes header
		header = header_tmp[0]+(header_tmp[1]<<8)+(header_tmp[2]<<16)+(header_tmp[3]<<24)+(header_tmp[4]<<32)+(header_tmp[5]<<40)+(header_tmp[6]<<48)+(header_tmp[7]<<56)
		SEQ = (header) >> 10 # number of packets
		CHANNEL = (header) & 0x3fff #each spectrum has 2^14 clock
                #print int(CHANNEL)
		#reoder data
		for j in range(0,frame_len/3):
                        xx[j+int(CHANNEL/4)] = xx_tmp[j]
                        yy[j+int(CHANNEL/4)] = yy_tmp[j]
		#save header to file
		#f_header.write(str(header)+'\n')
	print "grab number",SEQ/16,"spectrum done!"
	print 'received %d Bytes' % n_bytes_per_spec,
	print 'from',addr
	print 'the max value is at CHl',yy.index(max(yy)),', and the frequency is',yy.index(max(yy))/4096.0*960,'MHz'
	return SEQ,xx,yy


def plot_spectrum():
	pp=2
	p2=1 #subplot parameter

	matplotlib.pyplot.clf()
	seq,paa,pbb = get_data()
	# print power of xx
	pylab.subplot(211)
	#pylab.title('SEQ is '+str(seq),bbox=dict(facecolor='red', alpha=0.5))
	pylab.title('SEQ is '+str(seq))
    	#pylab.title('xx')	
	pylab.plot(paa,color="g")
    	pylab.xlim(0,4096)
	pylab.ylabel('xx')
	#pylab.ylabel('Power(dBm)')

	# print power of yy
	pylab.subplot(212)
    	#pylab.title('yy')	
	pylab.plot(pbb,color="b")
    	pylab.xlim(0,4096)
    	#pylab.ylim(-120,0)
    	pylab.ylabel('yy')
	#pylab.ylabel('Power(dBm)')

	fig.canvas.draw()	
	fig.canvas.manager.window.after(200,plot_spectrum)     
	return True

if __name__ == '__main__':

	#fpga=corr.katcp_wrapper.FpgaClient('r2d021403.casper.pvt')
	fpga=corr.katcp_wrapper.FpgaClient(HOST)
	time.sleep(0.1)
	if (fpga.is_connected()==True):
		print "roach2 connected, done!"

	IP = "10.0.1.12" #bind on all IP addresses
	PORT = 10000

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind((IP, PORT))
	#fpga.write_int('tvg_cmult_en',1) # set ramp check mode
	fpga.write_int('tvg_cmult_en',0) # unset ramp check mode
	fpga.write_int('vacc_shift',30) # for a input -10dBm signal
	#fpga.write_int('vacc_shift',52) # for ramp
	#f_header = open("header.txt","w") # write header to a file 
	if PORT != -1:
		print "1GbE port connect done!"
		fig = matplotlib.pyplot.figure()
		#gobject.timeout_add(1000,plot_spectrum)
		fig.canvas.manager.window.after(200,plot_spectrum)
		matplotlib.pyplot.show()
	#f_header.close()
