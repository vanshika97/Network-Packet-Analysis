#!/usr/bin/env python
from scapy.all import *
from datetime import datetime
import time
import datetime
import sys
from scapy.layers.dns import DNSRR, DNS, DNSQR
from subprocess import call
import os;

############# MODIFY THIS PART IF NECESSARY ###############
interface = 'eth0'
filter_bpf = 'udp and port 53'
#input_file= str(sys.argv[1])
#input_file= '/home/sahil/Dropbox/research/tcpdump/files//skype/sk3/skv3.pcap'
#input_file= '/home/sahil/fb1.pcap'
#temp_file = 'dns_temp.pcap'
f1 = ' "(dns) && (not icmp)" '

app=sys.argv[1]  #app-name
n=int(sys.argv[2])    #no-of-pcap-files



for z in range (1,n) :

 if app=='amazon':

  filename='amz'+str(z)+'.pcap'
  input_path='fakepath/amazon/amz'+str(z)+'/' 
  input_file=input_path + filename
  temp_file=input_path +'dns_temp'+str(z)+'.pcap'

 elif app=='skype' :
  filename='sk'+str(z)+'.pcap'
  input_path='fakepath/skype/sk'+str(z)+'/' 
  input_file=input_path + filename
  temp_file=input_path +'dns_temp'+str(z)+'.pcap'


 elif app=='youtube' :
  filename='utube'+str(z)+'.pcap'
  input_path='fakepath/youtube/utube'+str(z)+'/' 
  input_file=input_path + filename
  temp_file=input_path +'dns_temp'+str(z)+'.pcap'

 elif app=='facebook' :
  filename='fb'+str(z)+'.pcap'
  input_path='fakepath/facebook/fb'+str(z)+'/' 
  input_file=input_path + filename
  temp_file=input_path +'dns_temp'+str(z)+'.pcap'
  dns_file=input_path+'dns_'+'fb'+str(z)+'.txt' #dns-file-ptr
  f= open(dns_file,"w+")
 
 elif app=='browsing' :
  filename='web'+str(z)+'.pcap'
  input_path='fakepath/browser/web'+str(z)+'/' 
  input_file=input_path + filename
  temp_file=input_path +'dns_temp'+str(z)+'.pcap'
 
 elif app=='gmaps' :
  filename='map'+str(z)+'.pcap'
  input_path='fakepath/gmaps/map'+str(z)+'/' 
  input_file=input_path + filename
  temp_file=input_path +'dns_temp'+str(z)+'.pcap'
  dns_file=input_path+'dns_'+'gmap'+str(z)+'.txt' #dns-file-ptr
  f= open(dns_file,"w+")

 elif app=='speedtest' :
  filename='st'+str(z)+'.pcap'
  input_path='fakepath/speedtest/st'+str(z)+'/' 
  input_file=input_path + filename
  temp_file=input_path +'dns_temp'+str(z)+'.pcap'
 else:
    pass 


##########################################################

 command ='tshark -F libpcap -r'+ input_file + ' -Y ' + f1  + ' -w '+ temp_file+ ''
 process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
 process.wait()
 print process.returncode



 # ------ SELECT/FILTER MSGS##################################
 def select_DNS(pkt):
    pkt_time = pkt.time
 # ------ SELECT/FILTER DNS MSGS
    try:
        if DNSQR in pkt and pkt.dport == 53:
        # queries
           print 'Detected DNS QUERY Message at: ' + pkt_time +'........'
           # 
        elif DNSRR in pkt and pkt.sport == 53:
        # responses
           print 'Detected DNS RESPONSE Message at: ' + pkt_time + '........'
 # 
    except:
        pass
 # ------ START SNIFFER 
#sniff(iface=interface, filter=filter_bpf, store=0,  prn=select_DNS)



##############################################################


 pkts = rdpcap(temp_file)

 for p in pkts:
    #select_DNS(p)
    if p.haslayer(DNS):
        #if p.qdcount > 0 and isinstance(p.qd, DNSQR):
        if  DNSQR in p and p.dport == 53:
            if p.qdcount > 0:
            	name = p.qd.qname
                f.write("\n")
            	f.write("Query :: %s" % name)
        #elif p.ancount > 0 and isinstance(p.an, DNSRR):
        elif DNSRR in p and p.sport == 53:
        	if p.ancount > 0 :
            		name = p.an.rdata
                f.write("Response:: %s \n" % name)
            		#print 'Response ::'+name
            		#print 'Response ::'+"\n"
                a_count = p[DNS].ancount
                i = a_count + 4
                while i > 4:
                  f.write("Answer ::%s %s \n" %(p[0][i].rdata, p[0][i].rrname))
            			#print 'answer:'+p[0][i].rdata, p[0][i].rrname
                  i -= 1

        else:
            continue



 f.close() #close file
 
# command2 ='rm ' + temp_file
# process = subprocess.Popen(command2, shell=True, stdout=subprocess.PIPE)
# process.wait()
# print process.returncode

