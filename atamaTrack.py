# atamaTrack.py

import sys
import cv2
import numpy
import getXY
import piv

dt = 0.1 # [s]; time step

cap = cv2.cv.CreateFileCapture(sys.argv[1]) # load a movie file
cv2.cv.NamedWindow('Head Tracking', cv2.cv.CV_WINDOW_AUTOSIZE)

## click heads' positions on the first frame.
cv2.cv.SetCaptureProperty(cap, cv2.cv.CV_CAP_PROP_POS_MSEC, 0)
img = cv2.cv.QueryFrame(cap)
jjii0 = getXY.getXY(img).astype(numpy.int)

ii = jjii0[:, 1]
jj = jjii0[:, 0]
for iPerson in xrange(len(ii)):
    print 0.0, iPerson, ii[iPerson], jj[iPerson] # dump t, iPerson, ii, jj

## MAIN LOOP
for tSec in numpy.arange(20)*dt:
    # load the present frame
    cv2.cv.SetCaptureProperty(cap, cv2.cv.CV_CAP_PROP_POS_MSEC, tSec*1000)
    img1 = cv2.cv.QueryFrame(cap)
    img1gray = (numpy.asarray(cv2.cv.GetMat(img1))).astype(numpy.double)[:, :, 0]

    # load the next frame
    cv2.cv.SetCaptureProperty(cap, cv2.cv.CV_CAP_PROP_POS_MSEC, (tSec+dt)*1000)
    img2 = cv2.cv.QueryFrame(cap)
    img2gray = (numpy.asarray(cv2.cv.GetMat(img2))).astype(numpy.double)[:, :, 0]

    # find similar patterns around clicked points of the present frame from the next frame
    di, dj, ccmax = piv.find_flow(img1gray, img2gray, ii, jj, \
        kernel_size=(25, 25), di_range=(-15, 15), dj_range=(-15, 15))
    ii = ii+di # renew the positions
    jj = jj+dj

    for iPerson in xrange(len(ii)):
        cv2.cv.Circle(img1, (int(jj[iPerson]), int(ii[iPerson])), 10, (255, 0, 0), 2)
        print tSec+dt, iPerson, ii[iPerson], jj[iPerson] # dump t, iPerson, ii, jj

    cv2.cv.ShowImage('Head Tracking', img1)
    cv2.waitKey(0)

cv2.destroyAllWindows()
