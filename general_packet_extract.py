#!/usr/bin/env python
#parameter 1 = file path 
# parameter 2 = name of file {with extension .pcap)

from scapy.all import *
from datetime import datetime
import time
import datetime
import sys
from scapy.layers.dns import DNSRR, DNS, DNSQR
from subprocess import call
import os;
import subprocess
#from __future__ import print_function
##################################################################
#path_to_pcap=str(sys.argv[1])
#input_pcap=str(sys.argv[2])
#output_pcap='only_facebook_'+input_pcap

app=sys.argv[1]  #app-name
n=int(sys.argv[2]) #iteration_count/number_of_pcaps

for z in range (1,n):

  if app=='amazon':
   path_to_pcap='fakepath/amazon/amz'+str(z)+'/'
   input_pcap='amz'+str(z)+'.pcap'
   output_pcap='only_amazon_'+input_pcap
   file = open('filter_+input_pcap', 'w' )

  elif app=='skype' :
   path_to_pcap='fakepath/skype/sk'+str(z)+'/'
   input_pcap='sk'+str(z)+'.pcap'
   output_pcap='only_skype_'+input_pcap  
   filter=path_to_pcap+'filter.txt'
   file = open(filter, 'w' )

  elif app=='youtube' :
   path_to_pcap='fakepath/youtube/utube'+str(z)+'/'
   input_pcap='utube'+str(z)+'.pcap'
   output_pcap='only_youtube_'+input_pcap 
   filter=path_to_pcap+'filter.txt'
   file = open(filter, 'w' )

  elif app=='facebook' :
   path_to_pcap='fakepath/facebook/fb'+str(z)+'/'
   input_pcap='fb'+str(z)+'.pcap'
   output_pcap='only_facebook_'+input_pcap
   f1 = ' "((dns contains facebook || dns contains fbcdn || dns contains akadns) && (not icmp))" '   
   filter=path_to_pcap+'filter.txt'
   file = open(filter, 'w' )

  elif app=='browsing' :
   path_to_pcap='fakepath/browser/web'+str(z)+'/'
   input_pcap='wb'+str(z)+'.pcap'
   output_pcap='only_browsing_'+input_pcap
   filter=path_to_pcap+'filter.txt'
   file = open(filter, 'w' )
  
  elif app=='gmaps' :
   path_to_pcap='fakepath/gmaps/map'+str(z)+'/'
   input_pcap='map'+str(z)+'.pcap'
   output_pcap='only_gmap_'+input_pcap +'.pcap'
   f1 = ' "((dns contains gpstream || dns contains gstatic || dns contains googletagmanager || dns contains measurement || dns contains googleusercontent || dns contains gvt1 || dns contains ggpht || dns contains pgps || dns contains google) && (not icmp))" '
   filter=path_to_pcap+'filter.txt'
   file = open(filter, 'w' )
  
  elif app=='speedtest' :
   path_to_pcap='fakepath/speedtest/st'+str(z)+'/'
   input_pcap='st'+str(z)+'.pcap'
   output_pcap='only_speedtest_'+input_pcap
   file = open('filter_+input_pcap', 'w' )

  else :
   pass


 ##################################################################
  input_file = path_to_pcap + input_pcap
  temp_file = path_to_pcap +'temp.pcap'
  output_file = path_to_pcap + output_pcap

  f2 = ''
 ##################################################################


  command ='tshark -F libpcap -r'+ input_file + ' -Y ' + f1  + ' -w '+ temp_file+ ''
  process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
  process.wait()
  print process.returncode
 #################################################################

  pkts = rdpcap(temp_file)
  #pkts= sniff(offline=input_file,Ifilter=f1, prn=lambda x: x.summary())
  for p in pkts:
    if p.haslayer(DNS):
        #if p.qdcount > 0 and isinstance(p.qd, DNSQR):
        if  DNSQR in p and p.dport == 53:
            if p.qdcount > 0:
            	name = p.qd.qname
            	#print name
        #elif p.ancount > 0 and isinstance(p.an, DNSRR):
        elif DNSRR in p and p.sport == 53:
        	if p.ancount > 0 :
            		name = p.an.rdata
            		file.write("%s................." % name)
            		a_count = p[DNS].ancount
                #a1_count = p.ancount    
                file.write("ancount = %s\n" %(a_count))
                i = a_count + 4
          		
                while i > 4:
            			#print p[0][i].rdata, p[0][i].rrname
                  print p[0][i].rrname + ":" + p[0][i].rdata + ":"+str(p[0][i].type)
                  file.write("%s : %s : %s\n" %(p[0][i].rrname, p[0][i].rdata, p[0][i].type))
                  #if p[0][i].type == 1 :
                  f2= f2+ "ip.addr == " +  p[0][i].rdata + "||"
                  i -= 1

                file.write("\n\n")


        else:
            continue

  f2='"'+f2+"null"+'"'
  file.write(f2)
  file.close()
 #################################################################
  command1 ='tshark -F libpcap -r '+ input_file + ' -Y ' + f2 + ' -w ' + output_file 
  process = subprocess.Popen(command1, shell=True, stdout=subprocess.PIPE)
  process.wait()
  print process.returncode

 #################################################################
  command2 ='rm ' + temp_file
  process = subprocess.Popen(command2, shell=True, stdout=subprocess.PIPE)
  process.wait()
  print process.returncode
