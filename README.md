#dibas upgrade memo

To get the power data for FRBs detection when Dibas run in SETI observation mode, we made a slight firmware revise based on the original version. The FFT block signal was split to a new streamline, which include correlator, accumulator, packetizer and Ethernet. Due to the whole 8 ten-GbE ports were occupied by SETI data output, the FRB data will be sent through an one-GbE port. The diagram of this upgrade see Figure 1. 

![arch](arch.png)

* Some new registers added as follows:
	* rst_cpoge, reset correlator, packetizer and one Gb Ethernet
	* sw_pps, software synchronization
	* tvg_cmult_en, test vector generator enable
	* vacc_acc_len, length of accumulation
	* vacc_shift, barrel shift, least 6-bits effective, 0~63
	* one_GbE_dest_ip, one Gb Ethernet destination IP address
	* one_GbE_dest_port, one Gb Ethernet destination port
	* one_GbE_oge_en, one Gb Ethernet enable

We plan to lower the serendip6 valon synthesizer ADC clock from 1500 down to 960 MHz. The interleaved ADC5G board will then sample at twice that rate, at 1.92 GSps. we'll sample the L-band receiver in the second nyquist band, between 0.96 and 1.92 GHz, with a 0.19 MHz guard band on each end.  
For easier pass the routing and compiling, the original 12-taps PFB was changed to 4-taps, if you need more taps I will try more effort to fix it.
The packet format see figure 2. Each spectrum has 16 packets, and each packet has 768 bytes of data(256 bytes header, 256 bytes power of x and 256 bytes power of y), totally 4096 channels of power x and y. Each channel of power x and y have 8 bits, and each header has 64-bits. To transmit 64 header data through a 8-bit width Ethernet, we split it to 8 parts, you need shift each bytes header data after packets receiving. You just need the first 8 bytes of header, please discard the other 248 bytes header data(we do that just because it's easier to design). If you feel confused I can send you the python code. 

![packets-format](packets-format.png)

each spectrum has 12288 Bytes data, if we accumulate at 200¦Ì, the data rate from one GbE port would be: 12288 bytes x 8 bit x 5 KHz = 0.5Gbps
time_samp = acc_len x 8192/clock, acc_len = time_samp x clock/8192 = 200¦Ì x 1920MHz /8192 = 46.875

How to extract header information? If we received the header information and put them in a 8bit array header_8bit, shift them and add them together to header_64bit, we just need the first 8 bytes data.
header_64bit = header_8bit[0] + (header_8bit[1] << 8) + (header_8bit[2] << 16) + (header_8bit[3] << 24) + (header_8bit[4] << 32) + (header_8bit[5] << 40) + (header_8bit[6] << 48) + (header_8bit[7] << 56)

And here's some code! :+1:

```javascript
$(function(){
  $('div').html('I am a div.');
});
```

All of ROACH2 firmware and boffile you can find [on GitHub](https://github.com/SparkePei/dibas-upgrade-frb).

Here is a hashpipe code for dibas frb packets receiving and filterbank data writing [dibas-hashpipe](https://github.com/SparkePei/dibas-hashpipe) 
Props to Mr. Doob and his [code editor](http://mrdoob.com/projects/code-editor/), from which
the inspiration to this, and some handy implementation hints, came.

### Stuff used to make this:

 * [markdown-it](https://github.com/markdown-it/markdown-it) for Markdown parsing
 * [CodeMirror](http://codemirror.net/) for the awesome syntax-highlighted editor
 * [highlight.js](http://softwaremaniacs.org/soft/highlight/en/) for syntax highlighting in output code blocks
 * [js-deflate](https://github.com/dankogai/js-deflate) for gzipping of data to make it fit in URLs
		
