#! /usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import corr,time,numpy,struct,sys,logging,pylab
import matplotlib.mlab as mlab

#roach="10.0.1.170"#roach2
HOST = "specdemo"

def exit_fail():
	print 'FAILURE DETECTED. Log entries:\n',lh.printMessages()
	try:
		fpga.stop()
	except: pass
	raise
	exit()

def exit_clean():
	try:
		fpga.stop()
	except: pass
	exit()



def myplot():
	plt.clf()
	# capture data from snapshot
	fpga.write_int('adcsnap0_ctrl',1)
	chl_a=fpga.snapshot_get('adcsnap0',man_trig=True,man_valid=True)
	fpga.write_int('adcsnap1_ctrl',1)
	chl_b=fpga.snapshot_get('adcsnap1',man_trig=True,man_valid=True)
	# put data in a list
	value_a=numpy.fromstring(chl_a['data'], dtype = numpy.int8)
	value_b=numpy.fromstring(chl_b['data'], dtype = numpy.int8)

	# print time domain data

	plt.subplot(3,2,1)
	plt.title('IF0 Time-domain ')
	plt.ylabel('ADC value')
	plt.xlabel('ADC sample bins')
	#plt.set_yticks(range(-130, 131, 10))
	plt.ylim(-128,127)
	#plt.xlim(0,len(value_a))
	plt.xlim(0,1000)
	plt.plot(value_a,'b')
	power_a = value_a*value_a
	rms = np.sqrt(np.mean(power_a))
        print 'rms of value_a is :',rms


	plt.subplot(3,2,2)
	plt.title('IF1 Time-domain ')
	plt.xlabel('ADC sample bins')
	#plt.set_yticks(range(-130, 131, 10))
	plt.ylim(-128,127)
	#plt.xlim(0,len(value_a))
	plt.xlim(0,1000)
	plt.plot(value_b,'g')
        power_b = value_b*value_b
        rms = np.sqrt(np.mean(power_b))
        print 'rms of value_b is :',rms

	# create ideal gaussian shape for 8 bits
	th_id = 64 # ideal thresh
	bins8=np.arange(-128.5,128.5,1)
	g =mlab.normpdf(bins8,0,th_id)
	plt.subplot(3,2,3)
	plt.xticks(range(-130, 131, 40))
	#histData, bins, patches=plt.hist(b, bins = 256, range = (-128,128))
	plt.ylabel('Probability')
	#plt.ylim(0,1000)
	plt.xlabel('ADC value')
	plt.title('IF0 Histogram')
	#plt.hist(inter_analog, bins = 256, range = (-128,128))
	plt.hist(value_a, bins8,normed=1,facecolor='blue',alpha=0.9,histtype='stepfilled')
	plt.plot(bins8,g,'red',linewidth=1)

	plt.subplot(3,2,4)
	plt.xticks(range(-130, 131, 40))
	#plt.ylim(0,1000)
	plt.xlabel('ADC value')
	plt.title('IF1 Histogram')
	#plt.hist(inter_analog, bins = 256, range = (-128,128))
	plt.hist(value_b, bins8,normed=1,facecolor='green',alpha=0.9,histtype='stepfilled')
	plt.plot(bins8,g,'red',linewidth=1)
 

	inter_mv_a=[]
	k=0
	for k in range(len(value_a)):
		inter_mv_a.append(value_a[k]*250/128)

	inter_mv_b=[]
	k=0
	for k in range(len(value_b)):
		inter_mv_b.append(value_b[k]*250/128)

	n_chans=256
	n_accs=len(inter_mv_a)/n_chans/2
	freqs=numpy.arange(n_chans)*float(960000000)/n_chans #channel center freqs in Hz.
	window=numpy.hamming(n_chans*2)
	spectrum_a=numpy.zeros(n_chans)
	for acc in range(n_accs):
		spectrum_a += numpy.abs((numpy.fft.rfft(inter_mv_a[n_chans*2*acc:n_chans*2*(acc+1)]*window)[0:n_chans])) 
	#print spectrum.shape
	#print spectrum
	spectrum_a  = 20*numpy.log10(spectrum_a/n_accs/n_chans*4.91)-60
	spectrum_a = spectrum_a[::-1]
	#print spectrum.shape
	#print spectrum
	#print 'plotting from %i to %i'%(t_start,max_pos-1)
	pylab.hold(True)
	plt.subplot(3,2,5)
	plt.plot(freqs/1e6,spectrum_a,'b')
	#plt.legend()
	plt.title('IF0 Spectrum')
	plt.ylabel('Power (dBm)')
	plt.xlabel('Frequency (MHz)')


	spectrum_b=numpy.zeros(n_chans)
	for acc in range(n_accs):
		spectrum_b += numpy.abs((numpy.fft.rfft(inter_mv_b[n_chans*2*acc:n_chans*2*(acc+1)]*window)[0:n_chans])) 
	#print spectrum.shape
	#print spectrum
	spectrum_b  = 20*numpy.log10(spectrum_b/n_accs/n_chans*4.91+0.0000001)-60
	spectrum_b  = spectrum_b[::-1]
	#print spectrum.shape
	#print spectrum
	#print 'plotting from %i to %i'%(t_start,max_pos-1)
	pylab.hold(True)
	plt.subplot(3,2,6)
	plt.plot(freqs/1e6,spectrum_b,'g')
	#plt.legend()
	plt.title('IF1 Spectrum')
	plt.xlabel('Frequency (MHz)')

	fig.canvas.draw()
	fig.canvas.manager.window.after(1000, myplot)

if __name__ == '__main__':
	loggers = []
	lh=corr.log_handlers.DebugLogHandler()
	logger = logging.getLogger(HOST)
	logger.addHandler(lh)
	logger.setLevel(10)
	sys.stdout.flush()
	fpga = corr.katcp_wrapper.FpgaClient(HOST, 7147, timeout=10,logger=logger)
	time.sleep(1)
	if fpga.is_connected():
		print 'DONE'
	else:
		print 'ERROR: Failed to connect to server %s!' %(roach)
		sys.exit(0);



	# set up the figure with a subplot for each polarisation to be plotted
	fig = plt.figure()

	# create the subplots
	subplots = []
	for p in range(3):
		subPlot = fig.add_subplot(3, 1, p + 1)
		subplots.append(subPlot)

	# start the process
	print 'Starting plots...'
	fig.subplots_adjust(hspace=0.8)
	fig.canvas.manager.window.after(100, myplot)
	#plt.set_title('Histogram as at')
	plt.show()
