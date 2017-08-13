#!/usr/bin/env python

'''
Lucas-Kanade tracker
====================

Lucas-Kanade algorithm to track cars on a highway and save output

lk_track2.py [<video_source>]


ESC - exit
'''

from __future__ import print_function

import numpy as np
import cv2
#import video
from common import anorm2, draw_str
from time import clock

if __name__ == '__main__':
    import sys
    video_src='./cabrillo-1.asf'
    count=0
    save=np.ndarray(shape=(1, 5), dtype=np.float)
    c1=np.ndarray(shape=(1, 5), dtype=np.float)
    print(__doc__)
    lk_params = dict( winSize  = (15, 15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    feature_params = dict( maxCorners = 500,
                       qualityLevel = 0.3,
                       minDistance = 25,
                       blockSize = 25 )
    track_len = 50
    detect_interval = 1
    tracks = []
    cam = cv2.VideoCapture(video_src)
    frame_idx = 0
    while True:
            ret, frame = cam.read()
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            vis = frame.copy()
            if len(tracks) > 0:
                img0, img1 = prev_gray, frame_gray
                p0 = np.float32([tr[-1] for tr in tracks]).reshape(-1, 1, 2)
                p1, st, err = cv2.calcOpticalFlowPyrLK(img0, img1, p0, None, **lk_params)
                p0r, st, err = cv2.calcOpticalFlowPyrLK(img1, img0, p1, None, **lk_params)
                d = abs(p0-p0r).reshape(-1, 2).max(-1)
                good = d < 1
                new_tracks = []
                for tr, (x, y), (dx, dy),good_flag in zip(tracks, p1.reshape(-1, 2), (p1-p0).reshape(-1, 2),good):
                    if not good_flag:
                        continue
		    if y>200 and y<350 and x>300 and 500*x-500*y<125000 and np.sqrt(dx**2+dy**2)>.1: #which part of the road to track
                        tr.append((x, y))
			c1[:,0]=x
    			c1[:,1]=y
    			c1[:,2]=dx
    			c1[:,3]=dy
    			c1[:,4]=count
			save=np.r_[save,c1]
			new_tracks.append(tr)
                        cv2.circle(vis, (x, y), 3, (0, 0, 255), -1)
                    if len(tr) > track_len:
                        del tr[0]
                    
                tracks = new_tracks
                cv2.polylines(vis, [np.int32(tr) for tr in tracks], False, (0, 255, 0),2)
		#cv2.line(vis,(750,500),(250,0),(0,255,0),3)
		nc=len(tracks)/6
                draw_str(vis, (20, 20), 'track count: %d' % nc)
		
            if frame_idx % detect_interval == 0:
                mask = np.zeros_like(frame_gray)
                mask[:] = 255
                for x, y in [np.int32(tr[-1]) for tr in tracks]:
                    cv2.circle(mask, (x, y), 50, 0, -1)
                p = cv2.goodFeaturesToTrack(frame_gray, mask = mask, **feature_params)
                if p is not None:
                    for x, y in np.float32(p).reshape(-1, 2):
			
                        tracks.append([(x, y)])


            frame_idx += 1
            prev_gray = frame_gray
            cv2.imshow('lk_track', vis)
	    cv2.imwrite('./output-lk/'+str(count)+'.jpg', vis)
	    print(count)
	    count=count+1
	    ch = 0xFF & cv2.waitKey(1)
	    if count==int(cam.get(cv2.CAP_PROP_FRAME_COUNT))-1:
                np.savetxt('cabrillo-1-lk.txt',save,fmt='%9.3f')
            if ch == 27:
                break

    
    cv2.destroyAllWindows()
