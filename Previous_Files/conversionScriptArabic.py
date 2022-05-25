# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 16:19:28 2019

@author: george
"""

import string
from math import * 
#import serial
import time
import struct
#import win32gui
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import csv
import glob

letter_paths = glob.glob("D:\learning tool project\ltv2\Software\Arabic\Data\*.csv")
#ser = serial.Serial('COM7',9600)
thetaL_old=90
thetaR_old=-90
print(letter_paths)
theta1Change = 0
theta2Change = 0
#ser = serial.Serial('COM7',9600)
time.sleep(0.5)

#dir = 'English_Lower_Case/Data/'
dir2 ="D:\\learning tool project\\ltv2\\Software\\Arabic\\Data_converted\\"
#d = dict.fromkeys(string.ascii_lowercase, [])
for letter in letter_paths:    
    #print ("ok")
    
    x = []
    y = []
    z = []
    
    #print(key)
    delim = ','
    
    with open(letter,'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=delim)
        header = next(plots)
        for row in plots:
            if (float(row[3])>-8 and float(row[3])<7):

                x.append(-1*float(row[1]))
                y.append(-1*float(row[2]))
                #print("ok")
    #print(x)        
    xmin=np.min(x)
    xmax=np.max(x)
    ymin=np.min(y)
    ymax=np.max(y)
    gmax=max((xmax-xmin),(ymax-ymin))
    plt.plot((x-xmin)/gmax,(y-ymin)/gmax, label='Loaded from file!')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim([0,1])
    plt.ylim([0,1])
    #plt.title('Interesting Graph\nCheck it out')
    plt.legend()
    plt.show()
    x=(x-xmin)/gmax
    y=(y-ymin)/gmax
    
    transx = np.max(x)-np.min(x) 
    x=(1-transx)/2.0 +x
    
    transy = np.max(y)-np.min(y) 
    y=(1-transy)/2.0 +y
    print(int(len(x)))
    
    
    xs=[]
    ys=[]
    
    arr=range(len(x))
    #print(arr)
    
    #arr=arr[0:len(x):int(len(x)/100.0)]
    #print(arr)
    #print(dir2+letter[51:-4]+'.csv')
    delim = ' '
    with open(dir2+letter[51:-4]+'.csv','w') as csvfile2:
        wr=csv.writer(csvfile2, delimiter=delim)
        for i in arr:
            wr.writerow([x[i],y[i]])
            xs.append(x[i])
            ys.append(y[i])
        
    plt.plot(xs,ys,'go')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim([0,1])
    plt.ylim([0,1])
    plt.show()
    #write(dir2+key+'.csv')