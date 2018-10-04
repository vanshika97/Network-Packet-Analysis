#!/usr/bin/env python
import subprocess
import shlex
import sys
import numpy as np
import os;
import time

##################################################################
#path_to_pcap=str(sys.argv[1])
#input_pcap=str(sys.argv[2])

#input_file=path_to_pcap + '/' +input_pcap+'.pcap'
#output_file=path_to_pcap + '/' +input_pcap+'_th_stats.txti'
##################################################################

app=sys.argv[1]  #app-name
n=int(sys.argv[2]) 
print n
for z in range (1,n) :

 if app=='amazon':

  filename='only_amazon_amz'+str(z)
  input_path='fakepath/amazon/amz'+str(z)+'/' 
  input_file=input_path + filename+'.pcap'
  output_file=input_path + filename + '_throughput.txt'

 elif app=='skype' :
  filename='only_skype_sk'+str(z)
  input_path='fakepath/skype/sk'+str(z)+'/' 
  input_file=input_path + filename+'.pcap'
  output_file=input_path + filename + '_throughput.txt'


 elif app=='youtube' :
  filename='only_youtube_utube'+str(z)
  input_path='fakepath/youtube/utube'+str(z)+'/' 
  input_file=input_path + filename+'.pcap'
  output_file=input_path + filename + '_throughput.txt'

 elif app=='facebook' :
  filename='only_facebook_fb'+str(z)
  input_path='fakepath/facebook/fb'+str(z)+'/' 
  input_file=input_path + filename+'.pcap'
  output_file=input_path + filename + '_throughput.txt'
 
 elif app=='browsing' :
  filename='only_browsing_wb'+str(z)
  input_path='fakepath/browser/web'+str(z)+'/' 
  input_file=input_path + filename+'.pcap'
  output_file=input_path + filename + '_throughput.txt'
 
 elif app=='gmaps' :
  filename='only_gmap_map'+str(z)
  input_path='fakepath/gmaps/map'+str(z)+'/' 
  input_file=input_path + filename+'.pcap'
  output_file=input_path + filename + '_throughput.txt'

 elif app=='speedtest' :
  filename='only_speedtest_st'+str(z)
  input_path='fakepath/speedtest/st'+str(z)+'/' 
  input_file=input_path + filename+'.pcap'
  output_file=input_path + filename + '_throughput.txt'
 else :
  pass
 #tshark -r youtube_only_wifi_tube480_1.pcap "ssl" |awk 'BEGIN{OFS = " "}{print $2,$7}'>file.txt
 #command ='tshark -r  ' + str(sys.argv[1]) + '  "tcp or ssl" ' + " | awk 'BEGIN{OFS = \" \"}{print $2,$7}'>file.txt"
 #command ='tshark -r  ' + input_file + '  "tcp" ' + " | awk 'BEGIN{OFS = \" \"}{print $2,$7}'>file.txt"
 command ='tshark -r  ' + input_file  + " | awk 'BEGIN{OFS = \" \"}{print $2,$7}'>oldfile.txt"
 print command 
 process = subprocess.Popen(command, shell=True)
 process.wait()
 print process.returncode

 
 bad_words = ['with']
 with open('oldfile.txt') as oldfile, open('file.txt', 'w') as newfile:
    for line in oldfile:
        if not any(bad_word in line for bad_word in bad_words):
            newfile.write(line)

 with open("file.txt") as textFile:
    current_array = [line.split() for line in textFile]
    print current_array
    print '\n'
 #current_array.remove('with')
 #print current_array
 ################################################################################
 numrows = len(current_array)
 numcol = 2 #len(current_array[0])

 for row  in range(0, numrows):
	for col in range(0, numcol):
                 current_array[row][col]= float (current_array[row][col] )

#################################################################################


 f = open( output_file, 'w' )
 sec=[]
 kbps=[]
 #split=[0,100,200,300,400,500,600,700,800,900,1000]
 #split=[0,60,120,180,240,300,360,420,480,540,600,660,720,780,840,900,960,1020,1080,1140,1200]
 split=[0,60,120,180,240,300,360,420,480,540,600]

 for s in range(0,len(split)-1) :
 	sumi=0
        #time.sleep(5)
	for row  in range(0, numrows):
		#if ( current_array[row][0]>=split[s] and  current_array[row][0]<=split[s+1] ):
		if ( current_array[row][0]<=split[s+1] ):
             		sumi=sumi+current_array[row][1]
			#print current_array[row][0] , current_array[row][1]
                        
        print sumi
        #avg_throughput=repr(sumi*8/(60*1000))
        avg_throughput=repr(sumi*8/(split[s+1]*1000))
        sec.append(split[s+1])
        kbps.append(avg_throughput)   
        string=str(split[s+1] ) +","+ str(avg_throughput)
	f.write( string + '\n' )
	#f.write( 'th = ' + avg_throughput + '\n' )

 f.close()


 print sec
 print kbps




'''
for i in range(1,numrows ):
	current_array[i][1] += current_array[i-1][1]


current_array = np.array(current_array)
col1=current_array[:,0]
col2=current_array[:,1]


#arr = np.array([])
throughput = [0] *numrows

for i in range(1,numrows ):
	 throughput[i] = float(current_array[i][1]/current_array[i][0])

print throughput
throughput=throughput[1:]
throughput = [x * 8 for x in throughput]
thefile = open('thefile.txt', 'w')
for item in throughput:
  thefile.write("%s\n" % item)
thefile.close()


with open(output_file, 'w+') as f:
	subprocess.call("python calc_avg.py 1", shell=True,stdout=f)
	process.wait()
	print process.returncode


'''
