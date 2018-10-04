#!/usr/bin/env python
from numpy import *
import numpy as np
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import plotly.plotly as py
import sys

app=sys.argv[1]  #app-name
n=int(sys.argv[2]) #range-count
##############################################################################################
result = [[] for i in range(n)]
time = [[] for i in range(n)]
maxx=[]
minn=[]
ival=[]
for i in range(2,n):

     if app =='skype' :

      input_dir='fakepath/tcpdump/files/skype'
      filename=input_dir+"sk" +str(i) +"/"+"only_skype_skv"+str(i)+"_throughput.txt"

     elif app=='amazon' :

      input_dir='fakepath/tcpdump/files/amazon'
      filename=input_dir+"amz" +str(i) +"/"+"only_amazon_ama"+str(i)+"_throughput.txt"


     elif app=='youtube':

      input_dir='fakepath/tcpdump/files/youtube/'
      filename=input_dir+"utube" +str(i) +"/"+"youtube_only_youtube"+str(i)+"_throughput.txt"

     elif app=='facebook':

      input_dir='fakepath/facebook/'
      filename=input_dir+"fb" +str(i) +"/"+"only_facebook_fb"+str(i)+"_throughput.txt"


     elif app=='browsing':

      input_dir='fakepath/tcpdump/files/browser/'
      filename=input_dir+"web" +str(i) +"/"+"only_web_wb"+str(i)+"_throughput.txt"

     elif app=='gmaps':

      input_dir='fakepath/gmaps/'
      filename=input_dir+"map" +str(i) +"/"+"only_gmap_map"+str(i)+"_throughput.txt"

     else:
       pass

     with open(filename,'r') as f:
       #lines=f.readlines()[1:10]
       lines=f.readlines()
       for line in lines:
         result[i].append(line.rstrip().split(',')[1])
         time[i].append(line.rstrip().split(',')[0])

     #maxx.append(max(result[i]))
     #minn.append(min(result[i]))
     maxx.append(max([float(j) for j in result[i]]))
     minn.append(min([float(j) for j in result[i]]))
     ival.append(i)

print (result)
print (time)

############################################################################################
maxx=array(maxx)
print (maxx)


###############################################################################################
#plt.plot(time[1],result[1],time[2],result[2],time[3],result[3],time[4],result[4],time[5],result[5],time[6],result[6],time[7],result[7],time[8],result[8],time[9],result[9],time[10],result[10])
plt.plot(time[1],result[1],time[2],result[2],time[3],result[3],time[4],result[4])
#,time[5],result[5],time[6],result[6])
#fig1 = plt.gcf()
#fig1.savefig(path)
plt.ylabel('Throughput (Kbps)') # save figure before you show figure
plt.xlabel('Time (sec)') # save figure before you show figure
plt.title(' Throughput' + app.title())

plt.savefig(input_dir+'kbps.png') # save figure before you show figure
plt.show()
plt.close()


width = 0.65       # the width of the bars
#######################################################################
fig, ax = plt.subplots()
rects1 = ax.bar(ival, maxx, width, color='b')
ax.set_ylabel('Max Throughput (Kbps) ')
ax.set_xlabel(app.title()+ ' Session ')
ax.set_title('Max Throughput' + app.title())
#ax.legend((rects1[0]),'amazon' )

#########################################################################
def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % int(height),
                ha='center', va='bottom')


#######################################################################
autolabel(rects1)
plt.savefig(input_dir+'max_throughput.png')
plt.show()
plt.close()
#######################################################################




#######################################################################
fig, ax = plt.subplots()
rects1 = ax.bar(ival, minn, width, color='b')
ax.set_ylabel('Min Throughput (Kbps) ')
ax.set_xlabel(app.title()+' Session')
ax.set_title('Min Throughput '+app.title())
#ax.legend((rects1[0]),'amazon' )

#########################################################################
def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % int(height),
                ha='center', va='bottom')


#######################################################################
autolabel(rects1)
plt.savefig(input_dir+'min_throughput.png')
plt.show()
plt.close()
#######################################################################
