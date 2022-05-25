# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 17:58:11 2019

@author: george
"""

import glob
import rawpy
import imageio
#import auto_stack as ast
import cv2
import numpy as np

import time


def get_gradient(im) :
    # Calculate the x and y gradients using Sobel operator
    grad_x = cv2.Sobel(im,cv2.CV_32F,1,0,ksize=3)
    grad_y = cv2.Sobel(im,cv2.CV_32F,0,1,ksize=3)
 
    # Combine the two gradients
    grad = cv2.addWeighted(np.absolute(grad_x), 0.5, np.absolute(grad_y), 0.5, 0)
    return grad

def hisEqulColor(img):
    ycrcb=cv2.cvtColor(img,cv2.COLOR_BGR2YCR_CB)
    channels=cv2.split(ycrcb)
    #print( len(channels))
    cv2.equalizeHist(channels[0],channels[0])
    cv2.merge(channels,ycrcb)
    cv2.cvtColor(ycrcb,cv2.COLOR_YCR_CB2BGR,img)
    return img

def hisEqulColor2(img):
    
    ycrcb=img.copy() #cv2.cvtColor(img,cv2.COLOR_BGR2YCR_CB)
    channels=cv2.split(ycrcb)
    #print( len(channels))
    cv2.equalizeHist(channels[0],channels[0])
    ###
    cv2.equalizeHist(channels[1],channels[1])
    cv2.equalizeHist(channels[2],channels[2])
    ##
    cv2.merge(channels,ycrcb)
    #cv2.cvtColor(ycrcb,cv2.COLOR_YCR_CB2BGR,img)
    return ycrcb#img

def hisEqulColor3(img):
    clahe = cv2.createCLAHE(clipLimit=16.0, tileGridSize=(2,2))
    
    ycrcb=img.copy() #cv2.cvtColor(img,cv2.COLOR_BGR2YCR_CB)
    channels=cv2.split(ycrcb)
    #print( len(channels))
    #cv2.equalizeHist(channels[0],channels[0])
    channels[0] = clahe.apply(channels[0])
    ###
    #cv2.equalizeHist(channels[1],channels[1])
    channels[1] = clahe.apply(channels[1])
    #cv2.equalizeHist(channels[2],channels[2])
    channels[2] = clahe.apply(channels[2])
    ##
    cv2.merge(channels,ycrcb)
    return ycrcb#img

def get_histogram(image, bins):
    # array with size of bins, set to zeros
    histogram = np.zeros(bins)
    
    # loop through pixels and sum up counts of pixels
    for pixel in image:
        histogram[pixel] += 1
    
    # return our final result
    return histogram

def cumsum(a):
    a = iter(a)
    b = [next(a)]
    for i in a:
        b.append(b[-1] + i)
    return np.array(b)
    


def hisEqulColor3mono(img):
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(116,116))
    img = clahe.apply(img)
#    
    return img
def stackImagesECC(file_list):
    M = np.eye(3, 3, dtype=np.float32)
    #print(len(file_list))
    first_image = None
    stacked_image = None

    for image_color in file_list:
        image_color = image_color.astype(np.float32)/255
        #image_color = cv2.imread(file,1).astype(np.float32) / 255
        w, h,c = image_color.shape
        #[int(w*(2.0/5.0)):int(w*(3.0/5.0)),int(h*(2.0/5.0)):int(h*(3.0/5.0))]
        image = image_color.copy().astype(np.float32)/255.0
        #print(image_color.shape)
        if first_image is None:
            # convert to gray scale floating point image
            first_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            stacked_image = image
        else:
            criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 20,  1e-4)
            # Estimate perspective transform
            s, M = cv2.findTransformECC(cv2.cvtColor(image_color,cv2.COLOR_BGR2GRAY), first_image, M, cv2.MOTION_HOMOGRAPHY,criteria,None,1)
            #print(s)
            w, h,c = image.shape
            # Align image to first image
           
            #print(s)
            image = cv2.warpPerspective(image_color, M, (h, w))
            stacked_image += image

    stacked_image /= len(file_list)
    stacked_image = (stacked_image*255).astype(np.uint8)
    return stacked_image



img = cv2.imread('D:/astro/IMG_0702.png',-1)
print(img.shape)
print(img.dtype) 
img =  hisEqulColor3(img)
#img = LabEqual(img)
cv2.imwrite('D:/astro/xmmm.png',img)