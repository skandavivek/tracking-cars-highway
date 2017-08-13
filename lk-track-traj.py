#to make sure tracking is good

from __future__ import division, unicode_literals, print_function  # for compatibility with Python 2 and 3

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import cv2

#cascade_src = 'cars.xml'
video_src = './cabrillo-1.asf'
#video_src = 'dataset/video2.avi'

cap = cv2.VideoCapture(video_src)
count=0


t1=np.loadtxt('cabrillo-1-lk-tracked.txt')
ids=np.unique(t1[:,5])
co1=(np.random.rand(len(ids))*255).astype(int)
co2=(np.random.rand(len(ids))*255).astype(int)
co3=(np.random.rand(len(ids))*255).astype(int)


while True:
    ret, img = cap.read()
    w=np.where(t1[:,4] == count)[0]
    x=t1[w,0]
    y=t1[w,1]
    c2=0
    t2=t1[w,:]
    while c2 < len(x):
	w3=np.where(t1[:,5] == t2[c2,5])[0]
	a1=t1[w3,:]
	w4=np.where(a1[:,4]==np.min(a1[:,4]))[0]
	x1=a1[w4,0]
	y1=a1[w4,1]
	w=np.where(ids==t1[w3,5][0])
	a=co1[w[0]]
	b=co2[w[0]]
	c=co3[w[0]]
	if(len(a)>0):
	    cv2.circle(img, (x[c2].astype(int),y[c2].astype(int)), 3, (0,0,255), -1)
	    #cv2.circle(img, (x[c2].astype(int),y[c2].astype(int)), 2, (int(a),int(b),int(c)), -1)
        #cv2.circle(img, (0,0,255), -1)
            cv2.line(img,(x1[0].astype(int),y1[0].astype(int)),(x[c2].astype(int),y[c2].astype(int)),(0,255,0),2)   
  
        c2=c2+1
	#print(c2)

    cv2.imshow('video', img)
    string='./lk-tracked/'
    string2=str(count)+'.jpg'
    string=string+string2
    cv2.imwrite(string, img)
    count=count+1
    print(count)
    if cv2.waitKey(33) == 27:
        break

cv2.destroyAllWindows()
