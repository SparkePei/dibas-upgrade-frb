#! /usr/bin/python
import socket,array
import matplotlib.pyplot as plt
#import socket,pylab,matplotlib,math,corr,array
import time
import numpy as np

pkt_len = 8224
coarse_ch = 512
head_len = 8
n_pols = 4
n_spec_per_pkt = (pkt_len-head_len)/(coarse_ch*n_pols)
fine_ch = 4
xx_coarse = coarse_ch*[0]
xx_real_fine = fine_ch*[0]
xx_img_fine = fine_ch*[0]
xx_pwr_fine = fine_ch*[0]
xx_complex_fine = fine_ch*[0]
data = fine_ch*[pkt_len*[0]]

if __name__ == '__main__':
       	#fpga=corr.katcp_wrapper.FpgaClient('10.0.1.170')
       	IP = "10.10.10.194" #bind on s6c1 eth5
       	#IP = "10.10.10.68" #bind on s6c3 eth3 if birdie shows at 640MHz
       	#IP = "10.10.14.4" #bind on IP addresses
	#IP = "snb11-5.tenge.pvt"
	#IP = "10.0.1.63"
       	#IP = "snb11-4.tenge.pvt" #bind on IP addresses
       	#IP = "10.10.15.5" #bind on IP addresses
       	#IP = "" #bind on all IP addresses
       	PORT = 60000
	# file_name = "greenburst-test.dat"
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((IP, PORT))
       	if PORT != -1:
               	print "10GbE port connect done!"
	print "start to grab data from xGbE...",
	for i in range(fine_ch/n_spec_per_pkt):
	       	data[i], addr = sock.recvfrom(pkt_len)
	print "done."
	for i in range(fine_ch/n_spec_per_pkt):
		data_out=np.fromstring(data[i],dtype=np.int8)
		header = (data_out[1]<<48) + (data_out[2]<<40) + (data_out[3]<<32) + (data_out[4]<<24) + (data_out[5]<<16) + (data_out[6]<<8) + data_out[7]
		#print "header is:" ,header
		
		for j in range(n_spec_per_pkt):
			data_inv=data_out[8+j*coarse_ch*n_pols:8+(j+1)*coarse_ch*n_pols]
        		p0_real = data_inv[0::4]
        		p0_imag = data_inv[1::4]
        		p0_pwr = p0_real*p0_real+p0_imag*p0_imag
			p0_real_pwr = p0_real**2
			p0_imag_pwr = p0_imag**2
			rms = np.sqrt(np.mean(p0_real_pwr))
			print 'rms of real is :',rms
			rms = np.sqrt(np.mean(p0_imag_pwr))
			print 'rms of imag is :',rms
		plt.title("1/8 spectrum data from ten GbE port")
		plt.plot(p0_real,color='blue')	
		plt.legend("real")
		plt.plot(p0_imag,color='red')	
		plt.legend("imag")
	       	plt.show()

#			if (i==0) & (j==0): 
#				coarse_index = p0_pwr.tolist().index(max(p0_pwr))
#				coarse_value = p0_pwr.tolist().index(max(p0_pwr))/512.0*120+240
#				print 'the max value shows in coarse channel is:#',p0_pwr.tolist().index(max(p0_pwr)),', and the frequency is',p0_pwr.tolist().index(max(p0_pwr))/512.0*120+240,'MHz'
#			xx_real_fine[i*n_spec_per_pkt+j] = p0_real[coarse_index]
#			xx_img_fine[i*n_spec_per_pkt+j] = p0_imag[coarse_index]
#			xx_pwr_fine[i*n_spec_per_pkt+j] = p0_pwr[coarse_index]
#			xx_complex_fine[i*n_spec_per_pkt+j]=complex(p0_real[coarse_index],p0_imag[coarse_index])
#	# Do fine FFT
#        window=np.hamming(fine_ch)
#	sp = np.fft.fft(xx_complex_fine)
#	print 'the max value shows in fine channel is:#',sp.tolist().index(max(sp[1:fine_ch])),', and the frequency is',(sp.tolist().index(max(sp[1:fine_ch])))/4096.0*(960/4096.0)+coarse_value,'MHz'
#	#rms = np.sqrt(np.mean(sp**2))
#	#print 'rms is :',rms
#	freq = np.arange(0,fine_ch)
#	plt.subplot(2,1,1)
#	plt.title("raw voltage data after coarse FFT")
#	plt.plot(freq,xx_real_fine,color='blue')
#	plt.legend("real")
#	plt.plot(freq,xx_img_fine,color='red')
#	plt.legend("image")
#	plt.subplot(2,1,2)
#	plt.title("frequency data after fine FFT")
#	plt.plot(freq,abs(sp[:fine_ch]),color='blue')
#	plt.grid()
#	plt.show()
