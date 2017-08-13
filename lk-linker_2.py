#takes the original tracks from lk_track2 and finds 'IDs' to get tracks


from __future__ import print_function

import numpy as np
import cv2
#import video
from common import anorm2, draw_str
from time import clock
from scipy.spatial import cKDTree

c=0
if __name__ == '__main__':
    import sys
    data =np.loadtxt('cabrillo-1-lk.txt')
    save=np.zeros(shape=(1, 6), dtype=np.float)
    for i in range(0,int(np.max(data[:,4]))):
	if (i==0):
	    a1=np.where(data[:,4]==1)[0]
	    var=np.ndarray(shape=(len(a1), 6), dtype=np.float)
	    var[:,0:5]=data[a1,:]
	    ids=a1
	    var[:,5]=ids
	    save=np.r_[save,var]
	if (i>0):
	    #print(i)
	    a2=np.where(data[:,4]==i+1)[0]
	    a1=np.where(data[:,4]==i)[0]
	    data1=data[a1,:]
	    data2=data[a2,:]
	    print(i)
	    d1=np.zeros(shape=(len(a1),2), dtype=np.float)
	    d2=np.zeros(shape=(len(a2),2), dtype=np.float)
	    #if(len(a2)>len(a1)):
	    d1[:,0]=data1[:,0]+data1[:,2]
	    d1[:,1]=data1[:,1]+data1[:,3]
	    d2[:,0]=data2[:,0]
	    d2[:,1]=data2[:,1]
	    kdt1 = cKDTree(d1)
	    dist2, indices2 = kdt1.query(d2)
	    #kdt2 = cKDTree(d2)
	    #dist1, indices1 = kdt2.query(d1)
	    #l2=np.sqrt((d1[:,0]+d1[:,2]-data2[:,0])**2+(d1[:,1]+d1[:,3]-data2[:,1])**2)
	    wl2=np.where(dist2<1.)
	    wg2=np.where(dist2>1.)
	    #wl1=np.where(dist1<1.)
	    #print(len(wg)/len(wl))
	    var=np.ndarray(shape=(len(a2), 6), dtype=np.float)
	    var[:,0:5]=data2
	    var[:,5]=ids[indices2]
	        #print(np.shape(ids[wl]))
	        
	        #print(np.shape(var[wg,5]))
	        #print(np.shape(np.arange(0,len(wg[0]), 1).reshape(1,len(wg[0]))))
	    if (len(wg2[0])>0):
		var[wg2,5]=max(np.max(save[:,5]),np.max(var[:,5]))+1+np.arange(0,len(wg2[0]), 1)
		#var[wg2,0:5]=data2[wg2,:]
	    save=np.r_[save,var]
	    ids=var[:,5].reshape(len(var))
	if (i==int(np.max(data[:,4]))-1):	
	    #print(i)    
            np.savetxt('cabrillo-1-lk-tracked.txt',save,fmt='%9.3f')

		    
	    		
