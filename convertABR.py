from os import listdir, chdir
#import os
from os.path import isfile, join
from optparse import OptionParser
import pandas as pd
import numpy as np

#current 12/08/2015
def Pullfiles():
	#create the header
	mypath = "/Users/tjropp/Desktop/data/ABR_DATA/11-23-2015_ABR_P96_M_Noise_Exposed"
	onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
	singlefile = onlyfiles[8]
	filebase = singlefile[:14]
	striptxt=[]
	filetypes = ['p', 'n']
	#print filebase
	
	datadate = filebase[:8]
	
	for f in onlyfiles:
		striptxt.append(f[16:-4])
	print striptxt
	#ABRfiles = onlyfiles
	ABRfiles = combinepolarity(mypath,onlyfiles,striptxt)
	#print range(len(ABRfiles))

	for i in range(len(ABRfiles)):
		#if any(ABRfiles[i][14] in s for s in filetypes) & (ABRfiles[i][:14]==filebase):
		header1 = ":RUN-3	LEVEL SWEEP	TEMP:207.44 20120427 8:03 AM	-3852.21HR: \n"
		header2 = ":SW EAR: R	SW FREQ: " + striptxt[i][:-7] + ".00	# AVERAGES: 512	REP RATE (/sec): 40	DRIVER: Starship	SAMPLE (usec): 10 \n"
		header3 = ":NOTES- \n"
		header4 = ":CHAMBER-412 \n"
		header5 = ":LEVELS:20;25;30;35;40;45;50;55;60;65;70;75;80;85;90; \n"
		header6 = ":DATA \n"
		# header1 = ":RUN-3  LEVEL SWEEP   TEMP:207.44   4/6/2007  8:03 AM  -3852.21HR: \n"
		# header2 = ":SW EAR:R    SW FREQ:" + striptxt[i] + "  #AVERAGES: 400   REP RATE(/sec): 40  DRIVER: Starship  SAMPLE(usec): 10 \n" 
		# header3 = ":NOTES- \n"
		# header4 = ":CHAMBER-412 \n"
		# header5 = "LEVELS: 20;25;30;35;40;45;50;55;60;65;70;75;80;85;90; \n"
		# header6 = ":DATA \n"

		header = header1 + header2 + header3 + header4 + header5 + header6
		chdir(mypath)
		WriteHeader(ABRfiles[i],header)
		#print(ABRfiles[i])



	# #list of ABR frequencies
	# fl1 = [2, 4, 8, 12, 16, 32, 48]

	# if any("kHz" in s for s in onlyfiles):
	# 	freqlist = [s for s in onlyfiles if "kHz" in s]
	# 	fr = mypath + freqlist[0]
	# 	freqfile = open(fr,'r')
	# 	freqs = [line for line in freqfile]
	# #	intfreqs = [int(i) for i in freqs]
	# 	#check that the frequencies in freqs match those in fl1 (the default) list
	# #	set(intfreqs) & set(fl1)

	# #list of ABR SPLs
	# sl1=[20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90]

	# if any("SPL" in s for s in onlyfiles):
	# 	levellist = [s for s in onlyfiles if "SPL" in s]
	# 	lvl = mypath + levellist[0]
	# 	levelfile = open(lvl,'r')
	# 	levels = [line for line in levelfile]
		
	# open the levels file and read the levels into a variable

	#open the frequencies file and read the frequencies into a variable

	#read the date from the folder/first file name

	#write the new header to the text file

	#filename = "/Users/tessajonneropp/Desktop/data/10-29-2015_ABR_P74_M_Noise_Exposed/20151029-1100-n-16000.000.txt"
	return
def combinepolarity(mypath,onlyfiles,striptxt):
	nf = []
	pf = []
	ABRfiles=[]
	for f in onlyfiles:
		if 'n' in f:
			nf.append(f)
		elif 'p' in f:
			pf.append(f)
	#list of ABR frequencies
	fl1 = ['02000.000', '4000.000', '8000.000', '12000.000', '16000.000', '24000.000', '32000.000', '48000.000']
	for ABRfreq in fl1:
		if any((ABRfreq in nff for nff in nf) and (ABRfreq in pff for pff in pf)):
		# nindex = nf.find(ABRfreq)
		# pindex = pf.find(ABRfreq)
		# if nindex != -1:
			nff = [genfile for genfile in nf if ABRfreq in genfile]
			print 'negative file:', nff
			pff = [genfile for genfile in pf if ABRfreq in genfile]
			print 'positive file:', pff
			chdir(mypath)
			negf = pd.io.parsers.read_csv(nff[0],delim_whitespace=True, lineterminator='\r', skip_blank_lines=True, header=0)
			posf = pd.io.parsers.read_csv(pff[0],delim_whitespace=True, lineterminator='\r', skip_blank_lines=True, header=0)
			negseries=[]
			posseries=[]
			for col in negf.columns:
				print col
				for i in range(len(negf)):
					negseries.append(negf[col][i])
					
			print 'lenght of negf:', len(negf[col])
				#negseries.append(negf[col])
			for col in posf.columns:
				for i in range(len(posf)):
					posseries.append(posf[col][i])

				#posseries.append(posf[col])
		
			wvfmdata = [(x + y)/2 for x, y in zip(negseries, posseries)]
			
			print 'lenght of wvfmdata:', len(wvfmdata)
			print 'lenght of posf:', len(posf[col])
			print 'length of posseries:', len(posseries)
			
			print 'length of negseries:', len(negseries)
			waves=np.reshape(wvfmdata,(15,len(posf[col])))
			twaves=waves.T
			denote = 'ABR-' + ABRfreq[:-7] + '-3'

			np.savetxt(denote,twaves,delimiter='\t ',newline='\r\n')
		else:
			print 'No file with this frequency', ABRfreq
		ABRfiles.append(denote)
	return	ABRfiles
def WriteHeader(filename, header):
	

	ABRfile = open(filename, 'r')
	
	# remove any matching 'header' from the file, in case ther are duplicate header rows in the wrong places

	lines = [line for line in ABRfile if not line == header]
	ABRfile.close()

	# rewrite the file, appending the header to row 1
	ABRfile = open(filename, 'w')
	ABRfile.write(''.join(header))
	ABRfile.write('\n' .join(lines))
	ABRfile.write(''.join('\r\r'))
	ABRfile.close()
	return True

if __name__ == '__main__':
	Pullfiles()
    # if WriteHeader(filename, header):
    #     file = open(filename, 'a')
    # # 	file.write()
    #     file.close()
    # else:
    #     print 'there was a problem...'